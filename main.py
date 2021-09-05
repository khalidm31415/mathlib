import json
import random
from fastapi import FastAPI, HTTPException


app = FastAPI()

with open('./book.json') as file:
    books = json.load(file)

with open('./thesis.json') as file:
    theses = json.load(file)

@app.get("/ping")
def ping():
    return {"msg": "OK"}

@app.get("/book/random")
def get_random_book():
    book = random.choice(books)
    return book

@app.get("/book/{id}")
def get_book_by_id(id: int):
    book = next((book for book in books if book['id'] == id), None)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/thesis/random")
def get_random_thesis():
    thesis = random.choice(theses)
    return thesis

@app.get("/thesis/{id}")
def get_thesis_by_id(id: int):
    thesis = next((thesis for thesis in theses if thesis['id'] == id), None)
    if thesis:
        return thesis
    raise HTTPException(status_code=404, detail="Thesis not found")
