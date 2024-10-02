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
    
    
if __name__ == '__main__':
    app.run(debug=True)


