from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = 'a8e9f8ad6cfd4e1bb5a34b7e8e2c9fd1afbd2c1f12a56d3e7f8a9e'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/Book_store?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
db = SQLAlchemy(app)

@app.context_processor
def inject_genres():
    genres_query = db.session.execute(text("SELECT Name_genre FROM Genre")).mappings().fetchall()
    genres = [{'Name_genre': row['Name_genre']} for row in genres_query]
    return {'genres': genres}

@app.route('/')
def main():
    try:        
        sort = request.args.get('sort', '')
        
        query = """
            SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, 
                   B.Price, B.Year_of_publication
            FROM Book AS B
            JOIN Author AS A ON B.ID_author = A.ID_author
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
            SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, B.Price 
            FROM Book as B 
            JOIN Author as A ON B.ID_author = A.ID_author 
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

        return render_template('genre_books.html', genre=genre_name, books=books_list)

    except Exception as e:
        return f"Виникла помилка: {e}"
    
    
@app.route('/book/<int:book_id>')
def book_details(book_id):
    try:        
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
        
        # print(book_details)
        
        # reviews_list = [{'user_name': review.user_name, 'content': review.content} for review in reviews]

        return render_template('book_page.html', book=book_details) #, reviews=reviews_list

    except Exception as e:
        return f"Виникла помилка: {e}"

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query', '').strip()
        sort = request.args.get('sort', '')

        if query:
            b = db.session.execute(text("""
                SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, 
                    G.Name_genre AS Genre_Name, PH.Name_book AS Publishing_House,
                    B.Year_of_publication, B.Price, G.Descriptions
                FROM Book AS B
                JOIN Author AS A ON B.ID_author = A.ID_author
                JOIN Genre AS G ON B.ID_genre = G.ID_genre
                JOIN Publishing_house AS PH ON B.ID_publishing_house = PH.ID_publishing_house
                WHERE B.Book_name LIKE :query
                OR A.A_Name LIKE :query
                OR A.A_Surname LIKE :query
                OR PH.Name_book LIKE :query
            """), {'query': f"%{query}%"})

        else:
            b = db.session.execute(text("""
                SELECT B.ID_book, B.Book_name, A.A_Name, A.A_Patronymics, A.A_Surname, B.Price 
                FROM Book as B 
                JOIN Author as A ON b.ID_author = A.ID_author
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

        if not books_list:
            message = "Нічого не знайдено за вашим запитом."
        else:
            message = None

        return render_template('search_result.html', books=books_list, message=message, query=query)

    except Exception as e:
        return f"Виникла помилка: {e}"

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

    if not check_password_hash(user[2], password):
        return "Неправильний пароль!"

    session['user_login'] = email
    session['user_name'] = user[4]
    session['user_surname'] = user[3]
    session['user_patronymics'] = user[5]
    session['user_phone'] = user[6]
    session['user_address'] = user[7]

    return redirect(url_for('main'))

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    middle_name = request.form.get('middle_name', None)
    phone = request.form['phone']
    address = request.form['delivery_address']
    email = request.form['email']
    password = request.form['password']

    if not first_name or not last_name or not phone or not address or not email or not password:
        return "Усі поля обов'язкові для заповнення!"

    hashed_password = generate_password_hash(password)

    customer_query = text("""
        INSERT INTO Customer (user_login, user_password, C_Surname, C_Name, C_Patronymics, Phone_number, Addres)
        VALUES (:email, :password, :last_name, :first_name, :middle_name, :phone, :address)
    """)

    try:
        db.session.execute(customer_query, {
            'email': email,
            'password': hashed_password,
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'phone': phone,
            'address': address
        })
        db.session.commit()
        
        session['user_login'] = email
        session['user_name'] = first_name
        session['user_surname'] = last_name
        session['user_patronymics'] = middle_name
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
            SELECT ID_book, Book_name, Price
            FROM Book
            WHERE ID_book = :book_id
        """)
        book = db.session.execute(book_query, {'book_id': book_id}).fetchone()

        if not book:
            return redirect(url_for('main'))

        cart = session.get('cart', [])

        if cart and isinstance(cart[0], int):
            cart = []

        for item in cart:
            if item['id'] == book_id:
                item['quantity'] += 1
                session['cart'] = cart
                return redirect(url_for('cart'))

        cart.append({
            'id': book.ID_book,
            'name': book.Book_name,
            'price': book.Price,
            'quantity': 1,
            'image': '/static/img/book' + str(book.ID_book) + '.jpg'
        })
        session['cart'] = cart
    except Exception as e:
        return f"Сталася помилка: {e}"

    return redirect(url_for('main'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart = session.get('cart', [])
    total_quantity = 0

    for item in cart:
        total_quantity += item['quantity']
    
    total_sum = sum(item['quantity'] * item['price'] for item in cart)

    session['total_sum'] = total_sum
    
    user_data = {
        'email': session.get('user_login', ''),
        'first_name': session.get('user_name', ''),
        'last_name': session.get('user_surname', ''),
        'phone': session.get('user_phone', ''),
        'address': session.get('user_address', ''),
    }

    return render_template('cart.html', cart_items=cart, total_quantity=total_quantity, user_data=user_data)

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




# @app.route('/checkout', methods=['POST'])
# def checkout():
#     cart = session.get('cart', [])
#     if not cart:
#         print("Ваш кошик порожній. Додайте хоча б один товар перед оформленням замовлення.", "danger")
#         return redirect(url_for('cart'))

#     first_name = request.form.get('firstName', '').strip()
#     last_name = request.form.get('lastName', '').strip()
#     phone = request.form.get('phone', '').strip()
#     email = request.form.get('email', '').strip()
#     address = request.form.get('address', '').strip()

#     if not all([first_name, last_name, phone, email, address]):
#         print("Усі поля обов'язкові до заповнення. Перевірте форму та спробуйте ще раз.", "danger")
#         return redirect(url_for('cart'))

#     print("Ваше замовлення прийнято! Дякуємо за покупку.", "success")
#     session.pop('cart', None)
#     session.pop('total_sum', None)
#     return redirect(url_for('cart'))


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

if __name__ == '__main__':
    app.run(debug=True)
