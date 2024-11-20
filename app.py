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
        genre_query = db.session.execute(text("SELECT ID_genre FROM Genre WHERE Name_genre = :genre_name"), {'genre_name': genre_name})
        genre_result = genre_query.fetchone()
        genre_id = genre_result[0]

        b = db.session.execute(
            text("SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, B.Price FROM Book as B JOIN Author as A ON B.ID_author = A.ID_author WHERE B.ID_genre = :genre_id"),
            {'genre_id': genre_id}
        )
        books = b.fetchall()

        books_list = [{column: value for column, value in zip(b.keys(), book)} for book in books]
        
        g = db.session.execute(text("SELECT * FROM Genre"))
        genres = g.fetchall()

        genres_list = [{column: value for column, value in zip(g.keys(), genre)} for genre in genres]

        return render_template('genre_books.html', genres=genres_list, genre=genre_name, books=books_list)

    except Exception as e:
        return f"Виникла помилка: {e}"
    
    
@app.route('/book/<int:book_id>')
def book_details(book_id):
    try:
        g = db.session.execute(text("SELECT * FROM Genre"))
        genres = g.fetchall()

        genres_list = [{column: value for column, value in zip(g.keys(), genre)} for genre in genres]
        
        # Отримання даних про книгу
        book_query = text("""
            SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, 
                   G.Name_genre AS Genre_Name, PH.Name_book AS Publishing_House,
                   B.Year_of_publication, B.Price, G.Descriptions
            FROM Book AS B
            JOIN Author AS A ON B.ID_author = A.ID_author
            JOIN Genre AS G ON B.ID_genre = G.ID_genre
            JOIN Publishing_house AS PH ON B.ID_publishing_house = PH.ID_publishing_house
            WHERE B.ID_book = :book_id
        """)
        book = db.session.execute(book_query, {'book_id': book_id}).fetchone()

        # Отримання відгуків про книгу
        # reviews_query = text("""
        #     SELECT R.user_name, R.content 
        #     FROM Reviews AS R 
        #     WHERE R.ID_book = :book_id
        # """)
        # reviews = db.session.execute(reviews_query, {'book_id': book_id}).fetchall()

        # book_details = {column: value for column, value in zip(book.keys(), book)}
        # print(book_details)
        
        book_details = {
            'ID_book': book.ID_book,
            'Book_name': book.Book_name,
            'A_Name': book.A_Name,
            'A_Patronymics': book.A_Patronymics,
            'A_Surname': book.A_Surname,
            'Genre_Name': book.Genre_Name,
            'Publishing_House': book.Publishing_House,
            'Year_of_publication': book.Year_of_publication,
            'Price': book.Price,
            'Descriptions': book.Descriptions
        }
        
        print(book_details)
        
        # reviews_list = [{'user_name': review.user_name, 'content': review.content} for review in reviews]

        return render_template('book_page.html', book=book_details, genres=genres_list) #, reviews=reviews_list

    except Exception as e:
        return f"Виникла помилка: {e}"


    
    
if __name__ == '__main__':
    app.run(debug=True)


