# Biblioteca API ![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

Uma API RESTful desenvolvida com **FastAPI** para gerenciar livros e categorias.  
A API permite o upload de arquivos PDF de livros, criação e gerenciamento de categorias, e atualização de capas dos livros.  
É ideal para sistemas de bibliotecas digitais ou outros cenários que exijam organização e gestão de livros em formato digital.

## Funcionalidades ![Features](https://img.shields.io/badge/Features-Implemented-brightgreen)

- **Gerenciamento de Categorias**:
  - Listar todas as categorias.
  - Criar novas categorias.

- **Gerenciamento de Livros**:
  - Listar todos os livros cadastrados.
  - Buscar livros por categoria.
  - Exibir detalhes completos de um livro.
  - Download de livros em formato PDF.
  - Upload de novos livros (somente arquivos PDF são aceitos).
  - Atualização de informações dos livros (título, descrição e capa).
  - Remover livros, incluindo o arquivo PDF e a capa.

## Tecnologias Utilizadas ![Technologies](https://img.shields.io/badge/Technologies-Utilized-orange)

- **FastAPI**: Framework web para construção de APIs.
- **SQLAlchemy**: ORM utilizado para interação com o banco de dados.
- **SQLite**: Banco de dados leve utilizado para armazenar categorias e livros.
- **Logging**: Implementado para monitoramento e registro de atividades do sistema.

## Requisitos ![Requirements](https://img.shields.io/badge/Requirements-Python%203.9+-blue)

- Python 3.9+
- FastAPI
- SQLAlchemy
- Uvicorn (para executar o servidor)

### Instalação de Dependências ![Install](https://img.shields.io/badge/Install-Dependencies-yellow)

Para instalar as dependências necessárias, execute:

```bash
pip install -r requirements.txt
```
## Como Rodar o Projeto 

![Run](https://img.shields.io/badge/Run-Project-blue)

- Certifique-se de ter o Python instalado.
- Clone este repositório.
- Instale as dependências do projeto utilizando pip install -r requirements.txt.
- Execute o servidor FastAPI com o seguinte comando:
```uvicorn main:app --reload```
- O servidor estará disponível em http://127.0.0.1:8000.
  
### Clone este repositório:
- git clone https://github.com/seu-usuario/biblioteca-api.git

## Endpoints Principais

### Rota Raiz
- GET /: Verifica o status da API.
- GET/docs: Verifica a documentação da API.

### Categorias

- GET /categories/
- Descrição: Lista todas as categorias cadastradas
- Resposta: Um array de objetos JSON contendo o id e o name de cada categoria.
- Exemplo de Resposta:  
```  
[
  {
    "id": 1,
    "name": "Ficção Científica"
  },
  {
    "id": 2,
    "name": "Romance"
  }
]
```
## POST /categories/
- Descrição: Cria uma nova categoria.
- Requer: Um campo name no corpo da requisição contendo o nome da nova categoria.
### Exemplo de Requisição:
```
{
  "name": "Aventura"
}
```
```
- Exemplo de Resposta:
  {
  "id": 3,
  "name": "Aventura"
}
```
### Livros
- GET /books/:
- Descrição: Lista todos os livros cadastrados.
- Resposta: Um array de objetos JSON contendo detalhes sobre cada livro, como id, title, description, category_id e file_url.
- Exemplo de Resposta:
 ``` 
 [
  {
    "id": 1,
    "title": "O Guia do Mochileiro das Galáxias",
    "description": "Uma obra-prima da ficção científica humorística.",
    "category_id": 1,
    "file_url": "http://localhost:8000/books/1/download"
  },
  {
    "id": 2,
    "title": "Orgulho e Preconceito",
    "description": "Um romance clássico de Jane Austen.",
    "category_id": 2,
    "file_url": "http://localhost:8000/books/2/download"
  }
]
```
- GET /categories/{category_id}/books:
- Descrição: Lista todos os livros pertencentes a uma categoria específica.
- Parâmetro: category_id - O ID da categoria.
- Exemplo de Resposta:
```
[
  {
    "id": 1,
    "title": "O Guia do Mochileiro das Galáxias",
    "description": "Uma obra-prima da ficção científica humorística.",
    "category_id": 1,
    "file_url": "http://localhost:8000/books/1/download"
  }
]
```

- GET /books/{book_id}: Faz o download do livro no formato PDF.
- GET /books/{book_id}/info:
- Descrição: Retorna detalhes completos de um livro específico.
- Parâmetro: book_id - O ID do livro.
- Exemplo de Resposta:
```  
{
  "id": 1,
  "title": "O Guia do Mochileiro das Galáxias",
  "description": "Uma obra-prima da ficção científica humorística.",
  "category_id": 1,
  "file_url": "http://localhost:8000/books/1/download",
  "cover_url": "http://localhost:8000/covers/1.jpg"
}
```
- POST /upload/:
- Descrição: Faz o upload de um novo livro em formato PDF.
- Requer:
  - file: Arquivo PDF do livro.
  - title: Título do livro.
  - description: Descrição do livro.
  - category_id (opcional): O ID da categoria associada.
- Exemplo de Requisição (usando curl):
```
curl -X 'POST' \
'http://127.0.0.1:8000/upload/' \
-F 'file=@/caminho/do/arquivo/livro.pdf' \
-F 'title=Título do Livro' \
-F 'description=Descrição do Livro' \
-F 'category_id=1'
```
- PUT /books/{book_id}/update-cover/:
- Descrição: Atualiza a capa de um livro.
- Parâmetro: book_id - O ID do livro.
- Requer:
  - file: Arquivo de imagem da nova capa.

- Exemplo de Requisição:
```
curl -X 'PUT' \
'http://127.0.0.1:8000/books/1/update-cover/' \
-F 'file=@/caminho/da/capa.jpg'
```
- PUT /books/{book_id}:
- Descrição: Atualiza as informações de um livro.
- Parâmetro: book_id - O ID do livro.
Requer:
  - title: Título do livro.
  - description: Descrição do livro.
  - category_id (opcional): ID da nova categoria.
  
- Exemplo de Requisição:
```
{
  "title": "O Guia do Mochileiro das Galáxias - Edição Revisada",
  "description": "Versão atualizada do clássico.",
  "category_id": 1
}
```

- DELETE /books/{book_id}:
- Descrição: Remove um livro, excluindo também o arquivo PDF e a capa.
- Parâmetro: book_id - O ID do livro.
- Exemplo de Requisição (usando curl):
```  
curl -X 'DELETE' \
'http://127.0.0.1:8000/books/1'
```

## Estrutura do Projeto

📁 BibliotecaAPI/
```
│
├── 📁 books/ # Diretório onde os arquivos PDF dos livros são armazenados
├── 📁 covers/ # Diretório onde as capas dos livros são armazenadas
│
├── 📄 main.py # Código principal da aplicação FastAPI, contendo as rotas e lógica principal
├── 📄 models.py # Definições dos modelos de dados (Livros e Categorias) com SQLAlchemy
├── 📄 database.py # Configuração e inicialização do banco de dados SQLite usando SQLAlchemy
├── 📄 README.md # Documentação do projeto (este arquivo)
└── 📄 requirements.txt # Arquivo contendo as dependências necessárias para rodar o projeto

```



## Banco de Dados 
- O projeto utiliza SQLite para armazenamento local dos dados dos livros e categorias. A base de dados é inicializada automaticamente ao rodar a aplicação.

## Exemplos de Uso

### Upload de Livro

- Envie uma requisição POST para o endpoint /upload/ com os seguintes dados:

- file: Arquivo PDF do livro.
- title: Título do livro.
- description: Descrição do livro.
- category_id: (Opcional) ID da categoria associada.
- Exemplo de curl

``` curl -X 'POST' \
  'http://127.0.0.1:8000/upload/' \
  -F 'file=@/caminho/do/arquivo/livro.pdf' \
  -F 'title=Título do Livro' \
  -F 'description=Descrição do Livro' \
  -F 'category_id=1'
```
## Atualizar Capa de Livro
- Envie uma requisição PUT para o endpoint /books/{book_id}/update-cover/ com o arquivo da nova capa.
Exemplo: 
 ``` curl -X 'PUT' \
  'http://127.0.0.1:8000/books/1/update-cover/' \
  -F 'file=@/caminho/da/capa.jpg'
```
## 3. Excluir um Livro
- Para excluir um livro, envie uma requisição DELETE para /books/{book_id}.

```
curl -X 'DELETE' 'http://127.0.0.1:8000/books/1'

```

## Boas Práticas
- Verifique o tipo de arquivo ao fazer upload de livros (somente PDFs são permitidos).
- As capas de livros devem ser imagens (JPEG, PNG).
- Use endpoints apropriados para listar, criar e excluir tanto categorias quanto livros.

## Observações

- A aplicação armazena os arquivos PDF dos livros no diretório books/.
- As imagens de capa são armazenadas no diretório covers/.
- Todas as operações de CRUD utilizam o banco de dados SQLite, podendo ser facilmente adaptado para outros bancos de dados.
  
