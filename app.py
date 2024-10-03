from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Підключення до БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/Book_store?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
db = SQLAlchemy(app)


@app.route('/')
def main():
    try:
        g = db.session.execute(text("SELECT * FROM Genre"))
        genres = g.fetchall()

        genres_list = [{column: value for column, value in zip(g.keys(), genre)} for genre in genres]
        
        b = db.session.execute(text("SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, B.Price FROM Book as B JOIN Author as A ON b.ID_author = A.ID_author"))
        books = b.fetchall()

        books_list = [{column: value for column, value in zip(b.keys(), book)} for book in books]

        return render_template('main.html', genres=genres_list, books=books_list)

    except Exception as e:
        return f"Виникла помилка: {e}"
    
@app.route('/genre/<genre_name>')
def genre_books(genre_name):
    try:
        # Отримати ID жанру за його назвою
        genre_query = db.session.execute(text("SELECT ID_genre FROM Genre WHERE Name_genre = :genre_name"), {'genre_name': genre_name})
        genre_result = genre_query.fetchone()
        genre_id = genre_result[0]

        # Отримати книги за ID жанру
        b = db.session.execute(
            text("SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, B.Price FROM Book as B JOIN Author as A ON B.ID_author = A.ID_author WHERE B.ID_genre = :genre_id"),
            {'genre_id': genre_id}
        )
        books = b.fetchall()

        books_list = [{column: value for column, value in zip(b.keys(), book)} for book in books]
        
        g = db.session.execute(text("SELECT * FROM Genre"))
        genres = g.fetchall()

        genres_list = [{column: value for column, value in zip(g.keys(), genre)} for genre in genres]

        # Повернути шаблон з жанром та списком книг
        return render_template('genre_books.html', genres=genres_list, genre=genre_name, books=books_list)

    except Exception as e:
        return f"Виникла помилка: {e}"

    
    
if __name__ == '__main__':
    app.run(debug=True)


