import json
import random

import bcrypt
from fastapi import FastAPI, Body, Response, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()

@app.get("/ping")
def ping():
    return 'OK'


# Book Endpoints

@app.get("/book/random")
def get_random_book():
    with open('./data/book.json') as file:
        books = json.load(file)
    book = random.choice(books)
    return book

@app.get("/book/{_id}")
def get_book_by_id(_id: int):
    with open('./data/book.json') as file:
        books = json.load(file)
    for book in books:
        if book['id'] == _id:
            return book
    return Response(status_code=404)

@app.get("/book")
def get_all_book():
    with open('./data/book.json') as file:
        books = json.load(file)
        return books

@app.post("/book")
def create_book(title: str = Body(...), author: str = Body(...), credentials: HTTPBasicCredentials = Depends(security)):
    with open('./data/admin.json') as file:
        admins = json.load(file)

    authenticated = False
    for admin in admins:
        if admin['username'] == credentials.username:
            authenticated = bcrypt.checkpw(credentials.password.encode(), admin['password'].encode())
            break

    if not authenticated:
        return Response(status_code=401)

    with open('./data/book.json') as file:
        books = json.load(file)
    book = {'title': title, 'author': author}
    book['id'] = books[-1]['id'] + 1
    books.append(book)
    with open('./data/book.json', 'w') as file:
        books = json.dump(books, file, indent=4)
    return book

@app.delete("/book/{_id}")
def delete_book_by_id(_id: int):
    with open('./data/book.json') as file:
        books = json.load(file)
    for book in books:
        if book['id'] == _id:
            books.remove(book)
            with open('./data/book.json', 'w') as file:
                books = json.dump(books, file, indent=4)
            return Response(status_code=204)
    return Response(status_code=404)


# Thesis Endpoints

@app.get("/thesis/random")
def get_random_thesis():
    with open('./data/thesis.json') as file:
        theses = json.load(file)
    thesis = random.choice(theses)
    return thesis

@app.get("/thesis/{_id}")
def get_thesis_by_id(_id: int):
    with open('./data/thesis.json') as file:
        theses = json.load(file)
    thesis = next((thesis for thesis in theses if thesis['id'] == id), None)
    for thesis in theses:
        if thesis['id'] == _id:
            return thesis
    return Response(status_code=404)

@app.get("/thesis")
def get_all_thesis():
    with open('./data/thesis.json') as file:
        theses = json.load(file)
        return theses
