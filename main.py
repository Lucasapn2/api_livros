import logging
import mimetypes
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import init_db, SessionLocal
from models import Book, Category

# Configuração do logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Inicializa o banco de dados
init_db()

UPLOAD_DIRECTORY = "./books"
COVERS_DIRECTORY = "./covers"

# Cria os diretórios se não existirem
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(COVERS_DIRECTORY, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rota pública
@app.get('/')
def home():
    return 'API funcionando!'

# Rotas GET
@app.get("/categories/")
async def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"categories": [category.__dict__ for category in categories]}

@app.get("/categories/{category_id}/books")
async def get_books_by_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    books = db.query(Book).filter(Book.category_id == category_id).all()
    return {"category": db_category.name, "books": [book.__dict__ for book in books]}

@app.get("/books/")
async def list_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"books": [book.__dict__ for book in books]}

@app.get("/books/{book_id}")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    logging.info(f"Buscando livro com ID: {book_id}")
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book:
        file_path = os.path.join(UPLOAD_DIRECTORY, f"{db_book.id}.pdf")

        logging.info(f"Caminho do arquivo: {file_path}")
        if os.path.exists(file_path):
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.get("/covers/{filename}")
async def get_cover(filename: str):
    cover_path = os.path.join(COVERS_DIRECTORY, filename)
    if os.path.exists(cover_path):
        return FileResponse(cover_path)
    else:
        raise HTTPException(status_code=404, detail="Capa não encontrada")

@app.get("/books/{book_id}/info")
async def get_book_info(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        return {"id": db_book.id, "title": db_book.title, "description": db_book.description, "cover": db_book.cover}
    else:
        raise HTTPException(status_code=404, detail="Informações do livro não encontradas")

# Rotas POST
@app.post("/categories/")
async def create_category(name: str = Form(...), db: Session = Depends(get_db)):
    db_category = Category(name=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return {"id": db_category.id, "name": db_category.name}

@app.post("/upload/")
async def upload_book(
        file: UploadFile = File(...),
        title: str = Form(...),
        description: str = Form(...),
        category_id: int = Form(None),
        db: Session = Depends(get_db)
):
    # Verificar tipo MIME do arquivo
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido. Somente PDFs são aceitos.")

    # Cria o livro no banco de dados
    db_book = Book(title=title, description=description)

    if category_id:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if db_category:
            db_book.category = db_category
        else:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.add(db_book)
    db.commit()
    db.refresh(db_book)  

    # Salva o arquivo PDF
    file_location = os.path.join(UPLOAD_DIRECTORY, f"{db_book.id}.pdf")
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    logging.info(
        f"Livro salvo: ID={db_book.id}, Título={db_book.title}, Descrição={db_book.description}, Capa={db_book.cover}")

    return {"info": f"Arquivo {file.filename} salvo com sucesso", "id": db_book.id}

# Rotas PUT
@app.put("/books/{book_id}/update-cover/")
async def update_cover(book_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):

    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    cover_location = os.path.join(COVERS_DIRECTORY, file.filename)
    with open(cover_location, "wb+") as file_object:
        file_object.write(file.file.read())

    db_book.cover = file.filename
    db.commit()

    logging.info(f"Capa atualizada para o livro ID={book_id}: {file.filename}")
    return {"info": f"Capa {file.filename} salva com sucesso"}

@app.put("/books/{book_id}")
async def update_book(book_id: int, title: str = Form(...), description: str = Form(...), cover: str = Form(None),
                      db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db_book.title = title
        db_book.description = description
        if cover:
            db_book.cover = cover
        db.commit()
        return {"info": "Informações do livro atualizadas com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

# Rota DELETE
@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        file_path = os.path.join(UPLOAD_DIRECTORY, f"{db_book.id}.pdf")
        if os.path.exists(file_path):
            os.remove(file_path)

        cover = db_book.cover
        if cover:
            cover_path = os.path.join(COVERS_DIRECTORY, cover)
            if os.path.exists(cover_path):
                os.remove(cover_path)

        db.delete(db_book)
        db.commit()
        return {"info": "Livro removido com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
