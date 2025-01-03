import base64
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'a8e9f8ad6cfd4e1bb5a34b7e8e2c9fd1afbd2c1f12a56d3e7f8a9e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/Book_store?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
db = SQLAlchemy(app)

@app.context_processor
def inject_genres():
    genres_query = db.session.execute(text("SELECT Name_genre FROM Genre")).mappings().fetchall()
    genres = [{'Name_genre': row['Name_genre']} for row in genres_query]
    return {'genres': genres}

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Доступ заборонено. Ви повинні бути адміністратором.", "danger")
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def main():
    try:        
        sort = request.args.get('sort', '')
        
        query = """
            SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, 
                   B.Price, B.Year_of_publication, P.Photo_data
            FROM Book AS B
            JOIN Author AS A ON B.ID_author = A.ID_author
            JOIN Photos AS P ON B.ID_photo = P.ID_photo
        """
        
        if sort == 'price_asc':
            query += " ORDER BY B.Price ASC"
        elif sort == 'price_desc':
            query += " ORDER BY B.Price DESC"
        elif sort == 'name_asc':
            query += " ORDER BY B.Book_name ASC"
        elif sort == 'name_desc':
            query += " ORDER BY B.Book_name DESC"

        b = db.session.execute(text(query))
        books = b.fetchall()

        books_list = [{column: value for column, value in zip(b.keys(), book)} for book in books]
        for book in books_list:
            book['Photo_data'] = base64.b64encode(book['Photo_data']).decode('utf-8')

        return render_template('main.html', books=books_list)

    except Exception as e:
        return f"Виникла помилка: {e}"
    
@app.route('/genre/<genre_name>')
def genre_books(genre_name):
    try:
        genre_query = db.session.execute(text("SELECT ID_genre FROM Genre WHERE Name_genre = :genre_name"), {'genre_name': genre_name})
        genre_result = genre_query.fetchone()
        genre_id = genre_result[0]

        sort = request.args.get('sort', '')
        
        query = """
            SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, B.Price, P.Photo_data
            FROM Book as B 
            JOIN Author as A ON B.ID_author = A.ID_author 
            JOIN Photos AS P ON B.ID_photo = P.ID_photo
            WHERE B.ID_genre = :genre_id
        """
        
        if sort == 'price_asc':
            query += " ORDER BY B.Price ASC"
        elif sort == 'price_desc':
            query += " ORDER BY B.Price DESC"
        elif sort == 'name_asc':
            query += " ORDER BY B.Book_name ASC"
        elif sort == 'name_desc':
            query += " ORDER BY B.Book_name DESC"
            
        b = db.session.execute(
            text(query),
            {'genre_id': genre_id}
        )
        
        books = b.fetchall()

        books_list = [{column: value for column, value in zip(b.keys(), book)} for book in books]
        for book in books_list:
            book['Photo_data'] = base64.b64encode(book['Photo_data']).decode('utf-8')

        return render_template('genre_books.html', genre=genre_name, books=books_list)

    except Exception as e:
        return f"Виникла помилка: {e}"
    
    
@app.route('/book/<int:book_id>')
def book_details(book_id):
    try:        
        book_query = text("""
            SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, 
                   G.Name_genre AS Genre_Name, PH.Name_book AS Publishing_House,
                   B.Year_of_publication, B.Price, B.Descriptions, P.Photo_data
            FROM Book AS B
            JOIN Author AS A ON B.ID_author = A.ID_author
            JOIN Genre AS G ON B.ID_genre = G.ID_genre
            JOIN Publishing_house AS PH ON B.ID_publishing_house = PH.ID_publishing_house
            JOIN Photos AS P ON B.ID_photo = P.ID_photo
            WHERE B.ID_book = :book_id
        """)
        
        book = db.session.execute(book_query, {'book_id': book_id}).mappings().fetchone()
        
        book_details = dict(book)
        book_details['Photo_data'] = base64.b64encode(book_details['Photo_data']).decode('utf-8')

        return render_template('book_page.html', book=book_details)

    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query', '').strip()
        sort = request.args.get('sort', '')

        if query:
            b = db.session.execute(text("""
                SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, 
                    G.Name_genre AS Genre_Name, PH.Name_book AS Publishing_House,
                    B.Year_of_publication, B.Price, B.Descriptions, P.Photo_data
                FROM Book AS B
                JOIN Author AS A ON B.ID_author = A.ID_author
                JOIN Genre AS G ON B.ID_genre = G.ID_genre
                JOIN Publishing_house AS PH ON B.ID_publishing_house = PH.ID_publishing_house
                JOIN Photos AS P ON B.ID_photo = P.ID_photo
                WHERE B.Book_name LIKE :query
                OR A.A_Name LIKE :query
                OR A.A_Surname LIKE :query
                OR PH.Name_book LIKE :query
            """), {'query': f"%{query}%"})

        else:
            b = db.session.execute(text("""
                SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, B.Price, P.Photo_data
                FROM Book as B 
                JOIN Author as A ON b.ID_author = A.ID_author
                JOIN Photos AS P ON B.ID_photo = P.ID_photo
            """))
        
        if sort == 'price_asc':
            books = sorted(b.fetchall(), key=lambda x: x.Price)
        elif sort == 'price_desc':
            books = sorted(b.fetchall(), key=lambda x: x.Price, reverse=True)
        elif sort == 'name_asc':
            books = sorted(b.fetchall(), key=lambda x: x.Book_name)
        elif sort == 'name_desc':
            books = sorted(b.fetchall(), key=lambda x: x.Book_name, reverse=True)
        else:
            books = b.fetchall()
            
        books_list = [{column: value for column, value in zip(b.keys(), book)} for book in books]
        for book in books_list:
                book['Photo_data'] = base64.b64encode(book['Photo_data']).decode('utf-8')
                
        if not books_list:
            message = "Нічого не знайдено за вашим запитом."
        else:
            message = None

        return render_template('search_result.html', books=books_list, message=message, query=query)

    except Exception as e:
        return f"Виникла помилка: {e}"
    
@app.route('/search_catalog', methods=['GET'])
@admin_required
def search_catalog():
    query = request.args.get('query', '').strip()
    
    if query:
            res = db.session.execute(text("""
                SELECT b.ID_book, b.Book_name, b.Year_of_publication, b.Price, ph.Name_book, 
                    a.A_Name, a.A_Surname, a.A_Patronymics, g.Name_genre, p.Photo_data
                FROM Book as b
                JOIN Publishing_house as ph ON b.ID_publishing_house = ph.ID_publishing_house
                JOIN Author as a ON b.ID_author = a.ID_author
                JOIN Genre as g ON b.ID_genre = g.ID_genre
                JOIN Photos AS p ON b.ID_photo = p.ID_photo
                WHERE B.Book_name LIKE :query
                OR A.A_Name LIKE :query
                OR A.A_Surname LIKE :query
                OR PH.Name_book LIKE :query
            """), {'query': f"%{query}%"})
            books = res.fetchall()
            books_list = [{column: value for column, value in zip(res.keys(), book)} for book in books]
            for book in books_list:
                book['Photo_data'] = base64.b64encode(book['Photo_data']).decode('utf-8')
    
    return render_template('catalog.html', books=books_list)
    
@app.route('/search_orders', methods=['GET'])
@admin_required
def search_orders():
    query = request.args.get('query', '').strip()
    
    if query:
            res = db.session.execute(text("""
                SELECT o.ID_orders, o.Date_of_orders, o.Total_sum, o.Comment, c.C_Surname, c.C_Name
                FROM Orders AS o
                JOIN Customer AS c ON o.ID_customer = c.ID_customer
                WHERE o.ID_orders LIKE :query
                OR o.Date_of_orders LIKE :query
                OR c.C_Surname LIKE :query
                OR c.C_Name LIKE :query
            """), {'query': f"%{query}%"})
            orders = res.fetchall()
            orders_list = [{column: value for column, value in zip(res.keys(), order)} for order in orders]
    
    return render_template('orders.html', orders=orders_list)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return "Заповніть усі поля!"

    user_query = text("""
        SELECT *
        FROM Customer
        WHERE user_login = :email
    """)
    user = db.session.execute(user_query, {'email': email}).fetchone()

    if not user:
        return "Користувача з таким email не знайдено!"

    if not check_password_hash(user.user_password, password):
        return "Неправильний пароль!"

    session['user_login'] = user.user_login
    session['user_name'] = user.C_Name
    session['user_surname'] = user.C_Surname
    session['user_phone'] = user.Phone_number
    session['user_address'] = user.Addres

    if user.Is_admin:
        session['is_admin'] = True
        return redirect(url_for('catalog'))

    session['is_admin'] = False
    return redirect(url_for('main'))

@app.route('/catalog')
@admin_required
def catalog():
    book_query = text("""
        SELECT b.ID_book, b.Book_name, b.Year_of_publication, b.Price, ph.Name_book, 
            a.A_Name, a.A_Surname, a.A_Patronymics, g.Name_genre, p.Photo_data
        FROM Book as b
        JOIN Publishing_house as ph ON b.ID_publishing_house = ph.ID_publishing_house
        JOIN Author as a ON b.ID_author = a.ID_author
        JOIN Genre as g ON b.ID_genre = g.ID_genre
        JOIN Photos AS p ON b.ID_photo = p.ID_photo
    """)
    
    b = db.session.execute(book_query)
    books = b.fetchall()
    books_list = [{column: value for column, value in zip(b.keys(), book)} for book in books]
    for book in books_list:
        book['Photo_data'] = base64.b64encode(book['Photo_data']).decode('utf-8')
    return render_template('catalog.html', books=books_list)

def process_form_data(form_data, db_session):
    book_title = form_data.get('book_title')
    publication_year = form_data.get('publication_year')
    price = form_data.get('price')
    description = form_data.get('book_description')

    publisher = form_data.get('publisher')
    custom_publisher = form_data.get('custom_publisher') if publisher == 'custom' else publisher

    genre = form_data.get('genre')
    custom_genre = form_data.get('custom_genre') if genre == 'custom' else genre

    author_surname = form_data.get('author_lastname')
    author_name = form_data.get('author_firstname')
    author_patronymic = form_data.get('author_middlename')

    try:
        author_query = text("""
            SELECT ID_author FROM Author
            WHERE A_Surname = :surname AND A_Name = :name AND A_Patronymics = :patronymic
        """)
        author = db_session.execute(author_query, {
            'surname': author_surname,
            'name': author_name,
            'patronymic': author_patronymic
        }).fetchone()

        if not author:
            insert_author_query = text("""
                INSERT INTO Author (A_Surname, A_Name, A_Patronymics)
                OUTPUT INSERTED.ID_author
                VALUES (:surname, :name, :patronymic)
            """)
            author_id = db_session.execute(insert_author_query, {
                'surname': author_surname,
                'name': author_name,
                'patronymic': author_patronymic
            }).fetchone()[0]
        else:
            author_id = author[0]

        genre_to_check = custom_genre if genre == 'custom' else genre
        genre_query = text("SELECT ID_genre FROM Genre WHERE Name_genre = :genre")
        genre = db_session.execute(genre_query, {'genre': genre_to_check}).fetchone()

        if not genre:
            insert_genre_query = text("""
                INSERT INTO Genre (Name_genre)
                OUTPUT INSERTED.ID_genre
                VALUES (:genre)
            """)
            genre_id = db_session.execute(insert_genre_query, {'genre': genre_to_check}).fetchone()[0]
        else:
            genre_id = genre[0]

        publisher_to_check = custom_publisher if publisher == 'custom' else publisher
        publisher_query = text("SELECT ID_publishing_house FROM Publishing_house WHERE Name_book = :publisher")
        publisher = db_session.execute(publisher_query, {'publisher': publisher_to_check}).fetchone()

        if not publisher:
            insert_publisher_query = text("""
                INSERT INTO Publishing_house (Name_book)
                OUTPUT INSERTED.ID_publishing_house
                VALUES (:publisher)
            """)
            publisher_id = db_session.execute(insert_publisher_query, {'publisher': publisher_to_check}).fetchone()[0]
        else:
            publisher_id = publisher[0]

        return {
            'book_title': book_title,
            'publication_year': int(publication_year),
            'price': float(price),
            'description': description,
            'author_id': author_id,
            'genre_id': genre_id,
            'publisher_id': publisher_id
        }

    except Exception as e:
        db_session.rollback()
        raise e

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_item(book_id):
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete':
            try:
                delete_query = text("DELETE FROM Book WHERE ID_book = :book_id")
                db.session.execute(delete_query, {'book_id': book_id})
                db.session.commit()
                print("Товар видалено успішно!", "success")
                return redirect(url_for('catalog'))
            except Exception as e:
                db.session.rollback()
                return f"Сталася помилка при видаленні: {e}"

        elif action == 'edit':
            form_data = request.form
            file_data = request.files.get('book_cover')
            try:
                data = process_form_data(form_data, db.session)

                if file_data and file_data.filename:
                    photo_data = file_data.read()

                    insert_photo_query = text("""
                        INSERT INTO Photos (Photo_data)
                        OUTPUT INSERTED.ID_photo
                        VALUES (:photo)
                    """)
                    photo_id = db.session.execute(insert_photo_query, {'photo': photo_data}).fetchone()[0]

                    update_photo_query = text("""
                        UPDATE Book
                        SET ID_photo = :photo_id
                        WHERE ID_book = :book_id
                    """)
                    db.session.execute(update_photo_query, {'photo_id': photo_id, 'book_id': book_id})

                edit_book_query = text("""
                    UPDATE Book
                    SET 
                        Book_name = :book_name,
                        Year_of_publication = :year,
                        Price = :price,
                        Descriptions = :description,
                        ID_author = :author_id,
                        ID_genre = :genre_id,
                        ID_publishing_house = :publisher_id
                    WHERE ID_book = :book_id
                """)
                db.session.execute(edit_book_query, {
                    'book_name': data['book_title'],
                    'year': data['publication_year'],
                    'price': data['price'],
                    'description': data['description'],
                    'author_id': data['author_id'],
                    'genre_id': data['genre_id'],
                    'publisher_id': data['publisher_id'],
                    'book_id': book_id
                })
                db.session.commit()

                print("Дані книги оновлено успішно!", "success")
                return redirect(url_for('edit_item', book_id=book_id))
            except Exception as e:
                db.session.rollback()
                return f"Сталася помилка: {e}"

    book_query = """
        SELECT b.ID_book, b.Book_name, b.Year_of_publication, b.Price, b.Descriptions, ph.Name_book, 
            a.A_Name, a.A_Surname, a.A_Patronymics, g.Name_genre
        FROM Book as b
        JOIN Publishing_house as ph
        ON b.ID_publishing_house = ph.ID_publishing_house
        JOIN Author as a
        ON b.ID_author = a.ID_author
        JOIN Genre as g
        ON b.ID_genre = g.ID_genre
        WHERE b.ID_book = :book_id
    """
    book = db.session.execute(text(book_query), {'book_id': book_id}).fetchone()

    genres_query = "SELECT g.Name_genre FROM Genre as g"
    publishing_houses_query = "SELECT ph.Name_book FROM Publishing_house as ph"
    genres = [row[0] for row in db.session.execute(text(genres_query)).fetchall()]
    publishing_houses = [row[0] for row in db.session.execute(text(publishing_houses_query)).fetchall()]

    return render_template('edit_item.html', book=book, genres=genres, publishing_houses=publishing_houses)

@app.route('/add-item')
@admin_required
def add_item():
    queries = {
        'genres': "SELECT g.Name_genre FROM Genre as g",
        'publishing_houses': "SELECT ph.Name_book FROM Publishing_house as ph"
    }
    
    data = {}
    for key, query in queries.items():
        result = db.session.execute(text(query))
        data[key] = [row[0] for row in result.fetchall()]
    
    return render_template('add_item.html', genres=data['genres'], publishing_houses=data['publishing_houses'])

@app.route('/add-item-db', methods=['POST'])
@admin_required
def add_item_bd():
    form_data = request.form
    file_data = request.files.get('book_cover')
    try:
        if file_data and file_data.filename:
            photo_data = file_data.read()

            insert_photo_query = text("""
                INSERT INTO Photos (Photo_data)
                OUTPUT INSERTED.ID_photo
                VALUES (:photo)
            """)
            photo_id = db.session.execute(insert_photo_query, {'photo': photo_data}).fetchone()[0]
        else:
            photo_id = None

        data = process_form_data(form_data, db.session)

        insert_book_query = text("""
            INSERT INTO Book (Book_name, Year_of_publication, Price, ID_author, ID_genre, ID_publishing_house, ID_photo, Descriptions)
            VALUES (:book_name, :year, :price, :author_id, :genre_id, :publisher_id, :photo_id, :description)
        """)
        db.session.execute(insert_book_query, {
            'book_name': data['book_title'],
            'year': data['publication_year'],
            'price': data['price'],
            'author_id': data['author_id'],
            'genre_id': data['genre_id'],
            'publisher_id': data['publisher_id'],
            'photo_id': photo_id,
            'description': data['description']
        })
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return f"Сталася помилка: {e}"
    
    return redirect(url_for('catalog'))

@app.route('/orders')
@admin_required
def orders():
    try:
        orders_query = text("SELECT o.ID_orders, o.Date_of_orders, o.Total_sum, o.Comment FROM Orders AS o")
        o = db.session.execute(orders_query)
        orders = o.fetchall()
        orders_list = [{column: value for column, value in zip(o.keys(), order)} for order in orders]
        return render_template('orders.html', orders=orders_list)
    except Exception as e:
        return str(e)

@app.route('/orders/<int:order_id>')
@admin_required
def order_details(order_id):
    try:
        order_details_query = text("""
            SELECT 
                o.ID_orders, 
                o.Date_of_orders, 
                o.Total_sum, 
                o.Comment, 
                c.ID_book, 
                b.Book_name, 
                c.Number_of_orders, 
                (b.Price * c.Number_of_orders) AS Subtotal, 
                cs.C_Surname, 
                cs.C_Name, 
                cs.Phone_number, 
                cs.user_login, 
                cs.Addres 
            FROM 
                Orders AS o 
            JOIN 
                Cart AS c ON o.ID_orders = c.ID_orders 
            JOIN 
                Book AS b ON c.ID_book = b.ID_book 
            JOIN 
                Customer AS cs ON o.ID_customer = cs.ID_customer 
            WHERE 
                o.ID_orders = :order_id
        """)
        o = db.session.execute(order_details_query, {'order_id': order_id})
        orders = o.fetchall()
        order_data = [{column: value for column, value in zip(o.keys(), order)} for order in orders]
        return render_template('order_details.html', order=order_data)
    except Exception as e:
        return str(e)

@app.route('/update_comment/<int:order_id>', methods=['POST'])
@admin_required
def update_comment(order_id):
    try:
        comment = request.form.get('comment')
        update_query = text("""
            UPDATE Orders
            SET Comment = :comment
            WHERE ID_orders = :order_id
        """)
        db.session.execute(update_query, {'comment': comment, 'order_id': order_id})
        db.session.commit()
        return redirect(url_for('orders'))
    except Exception as e:
        return str(e)
    
@app.route('/cancel_order/<int:order_id>', methods=['POST'])
@admin_required
def cancel_order(order_id):
    try:
        cancel_query = text("""
            DELETE FROM Orders
            WHERE ID_orders = :order_id;
        """)
        db.session.execute(cancel_query, {'order_id': order_id})
        db.session.commit()
        return redirect(url_for('orders'))
    except Exception as e:
        print(e)
        return redirect(url_for('order_details', order_id=order_id))

@app.route('/send_newsletter', methods=['POST'])
@admin_required
def send_newsletter():
    subject = request.form['subject']
    message = request.form['message']

    email_query = text("""
            SELECT DISTINCT user_login
            FROM Customer;
        """)
    emails = db.session.execute(email_query).fetchall()

    for email in emails:
        send_email(email[0], subject, message)

    return redirect(url_for('catalog'))

def send_email(to_email, subject, message):
    sender_email = "reddashka@ukr.net"
    password = "uXlaFJqaPkBnIej1"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.ukr.net", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())


@app.route('/mailing')
@admin_required
def mailing():
    return render_template('mailing.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    address = request.form['delivery_address']
    email = request.form['email']
    password = request.form['password']

    if not first_name or not last_name or not phone or not address or not email or not password:
        return "Усі поля обов'язкові для заповнення!"

    hashed_password = generate_password_hash(password)

    check_user_query = text("""
        SELECT COUNT(*) FROM Customer WHERE user_login = :email
    """)
    try:
        result = db.session.execute(check_user_query, {'email': email}).scalar()
        if result > 0:
            return "Користувач із таким логіном уже існує!"

        customer_query = text("""
            INSERT INTO Customer (user_login, user_password, C_Surname, C_Name, Phone_number, Addres)
            VALUES (:email, :password, :last_name, :first_name, :phone, :address)
        """)

        db.session.execute(customer_query, {
            'email': email,
            'password': hashed_password,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'address': address
        })
        db.session.commit()

        session['user_login'] = email
        session['user_name'] = first_name
        session['user_surname'] = last_name
        session['user_phone'] = phone
        session['user_address'] = address

        return redirect(url_for('main'))
    except Exception as e:
        db.session.rollback()
        return f"Сталася помилка: {e}"


@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('main'))

@app.route('/add_to_cart/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    try:
        book_query = text("""
            SELECT B.ID_book, B.Book_name, B.Price
            FROM Book AS B
            WHERE ID_book = :book_id
        """)
        book = db.session.execute(book_query, {'book_id': book_id}).fetchone()

        cart = session.get('cart', [])

        for item in cart:
            if item['id'] == book_id:
                item['quantity'] += 1
                session['cart'] = cart
                return redirect(url_for('cart'))

        cart.append({
            'id': book.ID_book,
            'name': book.Book_name,
            'price': book.Price,
            'quantity': 1
        })
        session['cart'] = cart
    except Exception as e:
        return f"Сталася помилка: {e}"

    return redirect(url_for('main'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart = session.get('cart', [])
    total_quantity = 0
    total_sum = 0
    detailed_cart = []

    for item in cart:
        total_quantity += item['quantity']
        total_sum += item['quantity'] * item['price']
        photo_query = text("""
            SELECT Photo_data
            FROM Photos
            JOIN Book ON Photos.ID_photo = Book.ID_photo
            WHERE Book.ID_book = :book_id
        """)
        photo = db.session.execute(photo_query, {'book_id': item['id']}).fetchone()
        image = base64.b64encode(photo.Photo_data).decode('utf-8') if photo else None
        detailed_cart.append({**item, 'image': image})

    session['total_sum'] = total_sum
    
    user_data = {
        'email': session.get('user_login', ''),
        'first_name': session.get('user_name', ''),
        'last_name': session.get('user_surname', ''),
        'phone': session.get('user_phone', ''),
        'address': session.get('user_address', ''),
    }

    return render_template('cart.html', cart_items=detailed_cart, total_quantity=total_quantity, user_data=user_data)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if item['id'] != item_id]
    session['cart'] = updated_cart
    return redirect(url_for('cart'))

@app.route('/update_quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    cart = session.get('cart', [])
    new_quantity = request.form.get('quantity')

    try:
        new_quantity = int(new_quantity)
        if new_quantity < 1:
            flash("Кількість не може бути менше 1.", "danger")
            return redirect(url_for('cart'))
    except ValueError:
        flash("Некоректне значення кількості.", "danger")
        return redirect(url_for('cart'))

    for item in cart:
        if item['id'] == item_id:
            item['quantity'] = new_quantity
            break

    session['cart'] = cart

    total_sum = sum(item['quantity'] * item['price'] for item in cart)
    session['total_sum'] = total_sum

    flash("Кількість товару оновлено.", "success")
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash("Ваш кошик порожній. Додайте хоча б один товар перед оформленням замовлення.", "danger")
        return redirect(url_for('cart'))

    first_name = request.form.get('firstName', '').strip()
    last_name = request.form.get('lastName', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    address = request.form.get('address', '').strip()

    if not all([first_name, last_name, phone, email, address]):
        flash("Усі поля обов'язкові до заповнення. Перевірте форму та спробуйте ще раз.", "danger")
        return redirect(url_for('cart'))

    try:
        user_login = session.get('user_login')
        print(user_login)
        if user_login:
            customer = db.session.execute(
                text("SELECT * FROM Customer WHERE user_login = :login"),
                {'login': user_login}
            ).fetchone()
        else:
            db.session.execute(
                text("""
                INSERT INTO Customer (user_login, C_Surname, C_Name, Phone_number, Addres)
                VALUES (:login, :surname, :name, :phone, :address)
                """),
                {
                    'login': email,
                    'surname': last_name,
                    'name': first_name,
                    'phone': phone,
                    'address': address
                }
            )
            db.session.commit()
            customer = db.session.execute(
                text("SELECT * FROM Customer WHERE user_login = :login"),
                {'login': email}
            ).fetchone()
            print(customer)

        db.session.execute(
            text("""
            INSERT INTO Orders (ID_customer, Date_of_orders, Total_sum)
            VALUES (:customer_id, :order_date, :total_sum)
            """),
            {
                'customer_id': customer.ID_customer,
                'order_date': datetime.now(),
                'total_sum': session.get('total_sum', 0)
            }
        )
        db.session.commit()

        order = db.session.execute(
            text("SELECT * FROM Orders WHERE ID_customer = :customer_id ORDER BY ID_orders DESC"),
            {'customer_id': customer.ID_customer}
        ).fetchone()

        for item in cart:
            db.session.execute(
                text("""
                INSERT INTO Cart (ID_orders, ID_book, Number_of_orders)
                VALUES (:order_id, :book_id, :quantity)
                """),
                {
                    'order_id': order.ID_orders,
                    'book_id': item['id'],
                    'quantity': item['quantity']
                }
            )
        db.session.commit()

        session.pop('cart', None)
        session.pop('total_sum', None)

        flash("Ваше замовлення прийнято! Дякуємо за покупку.", "success")
        return redirect(url_for('cart'))

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Сталася помилка: {str(e)}", "danger")
        return redirect(url_for('cart'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/guarantee')
def guarantee():
    return render_template('guarantee.html')

import shutil
@app.route('/backup_db')
@admin_required
def backup_db():
    db_path = r"C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\Book_store.mdf"
    backup_path = 'C:/Users/dredk/Desktop/Код/Book_store/backup_db.mdf'

    try:
        shutil.copy(db_path, backup_path)
        return "Резервну копію створено успішно"
    except Exception as e:
        return f"Сталася помилка: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
