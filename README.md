# Biblioteca API

Uma API RESTful desenvolvida com **FastAPI** para gerenciar livros e categorias.
A API permite o upload de arquivos PDF de livros, gerenciamento de categorias e atualização de capas dos livros.
É ideal para sistemas de bibliotecas digitais ou outros cenários que exijam organização e gestão de livros em formato digital.

## Funcionalidades

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

## Tecnologias Utilizadas

- **FastAPI**: Framework web para construção de APIs.
- **SQLAlchemy**: ORM utilizado para interação com o banco de dados.
- **SQLite**: Banco de dados leve utilizado para armazenar categorias e livros.
- **Logging**: Implementado para monitoramento e registro de atividades do sistema.

## Requisitos

- Python 3.9+
- FastAPI
- SQLAlchemy
- Uvicorn (para executar o servidor)

### Instalação de Dependências

Para instalar as dependências necessárias, execute:

```bash
pip install -r requirements.txt
```
--
## Como Rodar o Projeto

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

GET /categories/: Lista todas as categorias cadastradas.
POST /categories/: Cria uma nova categoria. Requer um formulário com o campo name da categoria, exemplo: (Livros Romance).

### Livros
- GET /books/: Lista todos os livros cadastrados.
- GET /categories/{category_id}/books: Lista livros por categoria.
- GET /books/{book_id}: Faz o download do livro no formato PDF.
- GET /books/{book_id}/info: Retorna informações detalhadas sobre um livro específico.
- POST /upload/: Faz o upload de um novo livro em formato PDF. Requer um arquivo file, título title, descrição description e uma categoria opcional category_id.
- PUT /books/{book_id}/update-cover/: Atualiza a capa de um livro. Requer um arquivo file com a nova imagem da capa.
- PUT /books/{book_id}: Atualiza as informações de um livro, como título, descrição e capa.
- DELETE /books/{book_id}: Remove um livro, excluindo também seu arquivo PDF e capa.

## Estrutura do Projeto

📁 BibliotecaAPI/
│
├── 📁 books/              # Diretório onde os arquivos PDF dos livros são armazenados
├── 📁 covers/             # Diretório onde as capas dos livros são armazenadas
│
├── 📄 main.py             # Código principal da aplicação FastAPI
├── 📄 models.py           # Definições dos modelos de dados (Livros e Categorias)
├── 📄 database.py         # Inicialização do banco de dados SQLite e configuração do SQLAlchemy
├── 📄 README.md           # Documentação do projeto
└── 📄 requirements.txt    # Dependências do projeto

## Como Executar




## Banco de Dados 
- O projeto utiliza SQLite para armazenamento local dos dados dos livros e categorias. A base de dados é inicializada automaticamente ao rodar a aplicação.

##Exemplos de Uso
--
### Upload de Livro

- Envie uma requisição POST para o endpoint /upload/ com os seguintes dados:

- file: Arquivo PDF do livro.
- title: Título do livro.
- description: Descrição do livro.
- category_id: (Opcional) ID da categoria associada.
- Exemplo de curl
- 1.
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
 ```curl -X 'DELETE' 'http://127.0.0.1:8000/books/1'  ```

## Boas Práticas
- Verifique o tipo de arquivo ao fazer upload de livros (somente PDFs são permitidos).
- As capas de livros devem ser imagens (JPEG, PNG).
- Use endpoints apropriados para listar, criar e excluir tanto categorias quanto livros.

## Observações

- A aplicação armazena os arquivos PDF dos livros no diretório books/.
- As imagens de capa são armazenadas no diretório covers/.
- Todas as operações de CRUD utilizam o banco de dados SQLite, podendo ser facilmente adaptado para outros bancos de dados.
  
