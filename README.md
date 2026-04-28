# Blog API 📝

A RESTful Blog API built with FastAPI and PostgreSQL.

## Features
- User registration and login with JWT authentication
- Full CRUD for blog posts
- Comments on posts
- Pagination
- Password hashing with bcrypt
- Protected routes (only authors can edit/delete their content)

## Tech Stack
- **FastAPI** — Python web framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM
- **JWT** — Authentication
- **Passlib** — Password hashing

## Installation

1. Clone the repository
   git clone https://github.com/YOUR_USERNAME/blog-api.git
   cd blog-api

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Run the server
   uvicorn main:app --reload

## API Endpoints

### Auth
- POST /auth/register — Register a new user
- POST /auth/login — Login and get JWT token

### Posts
- GET /posts — Get all posts (with pagination)
- GET /posts/{id} — Get a single post
- POST /posts — Create a post (auth required)
- PUT /posts/{id} — Update a post (auth required)
- DELETE /posts/{id} — Delete a post (auth required)

### Comments
- GET /posts/{post_id}/comments — Get all comments for a post
- POST /posts/{post_id}/comments — Add a comment (auth required)
- DELETE /posts/{post_id}/comments/{comment_id} — Delete a comment (auth required)