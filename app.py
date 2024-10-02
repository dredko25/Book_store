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
        result = db.session.execute(text("SELECT * FROM Genre"))
        genres = result.fetchall()

        genres_list = [{column: value for column, value in zip(result.keys(), genre)} for genre in genres]

        return render_template('main.html', genres=genres_list)

    except Exception as e:
        return f"Виникла помилка: {e}"
    
    
if __name__ == '__main__':
    app.run(debug=True)


