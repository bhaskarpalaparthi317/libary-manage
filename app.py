from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
def get_db():
    conn = sqlite3.connect('library.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT
        )
    """)
    return conn


@app.route('/')
def index():
    return render_template('index.html')


# ADD BOOK
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = get_db()
        conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title, author)
        )
        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('add_book.html')


# VIEW BOOKS
@app.route('/view')
def view_books():
    conn = get_db()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template('view_books.html', books=books)


# SEARCH BOOK
@app.route('/search', methods=['GET', 'POST'])
def search_book():
    books = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        conn = get_db()
        books = conn.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            ('%' + keyword + '%', '%' + keyword + '%')
        ).fetchall()
        conn.close()

    return render_template('search_book.html', books=books)


# EDIT BOOK
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    conn = get_db()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn.execute(
            "UPDATE books SET title=?, author=? WHERE id=?",
            (title, author, id)
        )
        conn.commit()
        conn.close()
        return redirect('/view')

    book = conn.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    ).fetchone()
    conn.close()

    return render_template('edit_book.html', book=book)


# DELETE BOOK
@app.route('/delete/<int:id>')
def delete_book(id):
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/view')


if __name__ == '__main__':
    app.run(debug=True)
