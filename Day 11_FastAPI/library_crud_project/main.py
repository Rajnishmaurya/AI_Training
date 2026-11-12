from fastapi import FastAPI
from jupyter_server import DEFAULT_EVENTS_SCHEMA_PATH
from pydantic import BaseModel, ValidationError, Field
import psycopg2

app=FastAPI()

class books(BaseModel):
    book_id:int
    title:str
    author:str
    category:str
    price:float
    stock:int

def get_connection():
    conn=psycopg2.connect(
        host="localhost",
        database="library_store",
        user="postgres",
        password="Admin@123"
    )
    print("Connected to PostgreSQL successfully")
    return conn


@app.get("/books")
def get_books():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * from books")
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.post("/books")
def create_books(book:books):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
    INSERT INTO books (book_id,title,author,category,price,stock) 
    VALUES(%s,%s,%s,%s,%s,%s)""",
                   (book.book_id,book.title,book.author,book.category,book.price,book.stock)

                   )
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "message": "Book added successfully",
        "product": book
    }

@app.get("/books/technology")
def get_technology_books():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "SELECT * FROM books where category=%s",
        ("Technology",)
    )

    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.get("/books/greater_than_600")
def get_greater_than_600_books():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "SELECT * FROM books WHERE price > %s",
        (600,)
    )
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@app.put("/books/update_book_price")
def update_book_price():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        " UPDATE books SET price = %s where book_id=%s",
        (950,202)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {
"message": "Book price updates Successfully"}


@app.put("/books/update_book_stock")
def update_book_stock():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        " UPDATE books SET stock = %s where book_id=%s",
        (14,204)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {
"message": "Book stock updates Successfully"}


@app.delete("/books/delete/{book_id}")
def delete_book(book_id:int):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        " DELETE FROM books WHERE book_id=%s",
        (book_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return{
        "message": f"Book {book_id} deleted successfully",
    }

@app.get("/books/highest_price")
def get_highest_price():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """SELECT * FROM books ORDER by price DESC LIMIT 1"""
    )
    rows=cursor.fetchone()
    cursor.close()
    conn.close()
    return rows

@app.get("/books/total_stock_value")
def get_total_stock_value():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """SELECT sum(stock) FROM books"""
    )
    total=cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "total_stock_value": total
    }

@app.get("/books/books_each_category")
def books_each_category():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """SELECT category , count(1) FROM books GROUP BY category""",
    )
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

conn=get_connection()
conn.close()

