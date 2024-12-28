import base64
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import gridfs
import os

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb+srv://dredko25:gY7bukFt4hcGxBc4@cluster0.xs1ymu3.mongodb.net/Book_store?retryWrites=true&w=majority"

# mongo = PyMongo(app)

# # Тестування
# try:
#     with app.app_context():
#         mongo.cx.server_info()
#         print("ОК!")
# except Exception as e:
#     print(f"Помилка: {e}")
    
# # Вибір бази даних і колекцій
# db = mongo.db  # Використовуємо PyMongo для доступу до бази даних
# orders_collection = db['Orders']  # Колекція orders

# # Пайплайн агрегації
# pipeline = [
#     {
#         "$lookup": {
#             "from": "Customer",        # Колекція, з якою з'єднуємо
#             "localField": "customer_id", # Поле в колекції orders
#             "foreignField": "_id",       # Поле в колекції customer
#             "as": "customer_info"        # Нове поле для результату злиття
#         }
#     },
#     {
#         "$project": {
#             "_id": 1,
#             "Date_of_orders": 1,
#             "Total_sum": 1,
#             "customer_info.C_Surname": 1,
#             "customer_info.C_Name": 1
#         }
#     }
# ]

# Виконання агрегації
# result = orders_collection.aggregate(pipeline)

# for order in result:
#     print(f"Order ID: {order['_id']}")
#     print(f"Date of Order: {order['Date_of_orders']}")
#     print(f"Total Sum: {order['Total_sum']}")
    
#     if order['customer_info']:
#         # Оскільки customer_info - це масив, беремо перший елемент
#         customer = order['customer_info'][0]
#         print(f"Customer Surname: {customer['C_Surname']}")
#         print(f"Customer Name: {customer['C_Name']}")
#     else:
#         print("No customer information found.")
#     print("-" * 20)
    
from pymongo import MongoClient
from gridfs import GridFSBucket
import base64

# Підключення до бази
client = MongoClient("mongodb+srv://dredko25:gY7bukFt4hcGxBc4@cluster0.xs1ymu3.mongodb.net/Book_store?retryWrites=true&w=majority")
db = client['Book_store']
fs = GridFSBucket(db)

books_query = db['Book'].aggregate([
    {
        '$lookup': {
            'from': 'Author',
            'localField': 'author_id',
            'foreignField': '_id',
            'as': 'Author'
        }
    },
    {
        '$lookup': {
            'from': 'fs.files',
            'localField': 'photo_id',
            'foreignField': '_id',
            'as': 'Photo'
        }
    },
    {
        '$unwind': '$Author'
    },
    {
        '$unwind': {
            'path': '$Photo',
            'preserveNullAndEmptyArrays': True
        }
    }
])

# Формування списку книг
books_list = []
for book in books_query:
    book_item = {
        'ID_book': book['_id'],
        'Book_name': book['Book_name'],
        'A_Name': book['Author']['A_Name'],
        'A_Patronymics': book['Author']['A_Patronymics'],
        'A_Surname': book['Author']['A_Surname'],
        'Price': book['Price'],
        'Year_of_publication': book['Year_of_publication']
    }

    # Завантаження фото через GridFSBucket
    if 'Photo' in book and book['Photo']:
        photo_id = book['Photo']['_id']
        try:
            with fs.open_download_stream(photo_id) as file:
                photo_data = file.read()
                book_item['Photo_data'] = base64.b64encode(photo_data).decode('utf-8')
        except Exception as e:
            print(f"Помилка при завантаженні фото: {e}")
            book_item['Photo_data'] = None
    else:
        book_item['Photo_data'] = None

    books_list.append(book_item)

# Виведення списку
for i in books_list:
    print(i)


# books_query = db['Book'].aggregate([
#     {
#         '$lookup': {
#             'from': 'Author',
#             'localField': 'author_id',
#             'foreignField': '_id',
#             'as': 'Author'
#         }
#     },
#     {
#         '$lookup': {
#             'from': 'fs.files',  # Підключення до GridFS
#             'localField': 'photo_id',
#             'foreignField': '_id',
#             'as': 'Photo'
#         }
#     },
#     {
#         '$unwind': '$Author'
#     },
#     {
#         '$unwind': {
#             'path': '$Photo',
#             'preserveNullAndEmptyArrays': True  # Якщо фото немає, це дозволить уникнути помилок
#         }
#     }
# ])

# # Формування списку книг
# books_list = []
# for book in books_query:
#     book_item = {
#         'ID_book': book['_id'],
#         'Book_name': book['Book_name'],
#         'A_Name': book['Author']['A_Name'],
#         'A_Patronymics': book['Author']['A_Patronymics'],
#         'A_Surname': book['Author']['A_Surname'],
#         'Price': book['Price'],
#         'Year_of_publication': book['Year_of_publication']
#     }
#     # Завантаження фото з GridFS
#     if 'Photo' in book and book['Photo']:
#         photo_id = book['Photo']['_id']
#         photo_data = db.fs.chunks.find_one({'files_id': photo_id})
#         if photo_data:
#             book_item['Photo_data'] = base64.b64encode(photo_data['data']).decode('utf-8')
#         else:
#             book_item['Photo_data'] = None
#     else:
#         book_item['Photo_data'] = None

#     books_list.append(book_item)

# for i in books_list:
#     print(i)


# fs = gridfs.GridFS(db)  # Ініціалізація GridFS

# # Функція для завантаження зображення в GridFS
# def upload_image(image_path):
#     with open(image_path, 'rb') as image_file:
#         file_id = fs.put(image_file, filename=image_path.split('/')[-1])  # Зберігаємо зображення в GridFS
#         print(f"Зображення завантажено з ID: {file_id}")
#     return file_id

# image_path = 'C:/Users/dredk/Desktop/Код/Book_store/static/img/book15.jpg'
# upload_image(image_path)
