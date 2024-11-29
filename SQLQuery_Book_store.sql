--CREATE DATABASE Book_store

use Book_store
 
CREATE TABLE Author( 
	ID_author INT IDENTITY(1,1) PRIMARY KEY, 
	A_Surname VARCHAR(20), 
	A_Name VARCHAR(20), 
	A_Patronymics VARCHAR(20)
);
 
CREATE TABLE Publishing_house( 
	ID_publishing_house INT IDENTITY(1,1) PRIMARY KEY, 
	Name_book VARCHAR(30), 
	City VARCHAR(30) 
);
 
CREATE TABLE Genre( 
	ID_genre INT IDENTITY(1,1) PRIMARY KEY, 
	Name_genre VARCHAR(30)
);

CREATE TABLE Photos ( 
    ID_photo INT PRIMARY KEY IDENTITY(1,1),  
    Name_photo NVARCHAR(255) NOT NULL,       
    Photo_data VARBINARY(MAX) NOT NULL,      
    Upload_date DATETIME DEFAULT GETDATE()  
); 
 
CREATE TABLE Book( 
	ID_book INT IDENTITY(1,1) PRIMARY KEY, 
	ID_publishing_house INT FOREIGN KEY REFERENCES Publishing_house(ID_publishing_house) ON DELETE CASCADE, 
	ID_author INT FOREIGN KEY REFERENCES Author(ID_author) ON DELETE CASCADE, 
	ID_genre INT FOREIGN KEY REFERENCES Genre(ID_genre) ON DELETE CASCADE, 
	ID_photo INT FOREIGN KEY REFERENCES Photos(ID_photo) ON DELETE CASCADE, 
	Book_name VARCHAR(50), 
	Year_of_publication INT, 
	Descriptions VARCHAR(MAX), 
	Price FLOAT
) 
 
CREATE TABLE Customer( 
    ID_customer INT IDENTITY(1,1) PRIMARY KEY, 
    user_login VARCHAR(100), 
    user_password VARCHAR(255), 
    C_Surname VARCHAR(20), 
    C_Name VARCHAR(20),
    Phone_number VARCHAR(20), 
    Addres VARCHAR(40),
    Is_admin BIT NOT NULL DEFAULT 0
)

CREATE TABLE Orders( 
	ID_orders INT IDENTITY(1,1) PRIMARY KEY, 
	ID_customer INT FOREIGN KEY REFERENCES Customer(ID_customer) ON DELETE CASCADE, 
	Date_of_orders DATE, 
	Total_sum INT, 
	Comment VARCHAR(300) 
) 
 
CREATE TABLE Cart( 
	ID_cart INT IDENTITY(1,1) PRIMARY KEY, 
	ID_orders  INT FOREIGN KEY REFERENCES Orders(ID_orders) ON DELETE CASCADE, 
	ID_book INT FOREIGN KEY REFERENCES Book(ID_book) ON DELETE CASCADE, 
	Number_of_orders INT 
) 


----��������� ����: 
--INSERT INTO Photos  
--SELECT  
--    'example.jpg',  
--    BulkColumn 
--FROM OPENROWSET(BULK 'C:\path_to_image\example.jpg', SINGLE_BLOB) AS ImageFile;



-- ������� ����� � ������� Author
INSERT INTO Author (A_Surname, A_Name, A_Patronymics)
VALUES
('��������', '������', NULL),
('������', '������', NULL),
('����', '�����', NULL),
('Գ���������', '������', '�����'),
('�����', '����', '������� ����'),
('ʳ��', '�����', NULL),
('������', '�����', NULL),
('�����', '������', '������� г����'),
('�������', '���', NULL),
('�����', '�����', NULL),
('˳', '������', NULL),
('����', '�����', '�����'),
('�������', '����', NULL),
('������', '³����', NULL),
('����', '����', NULL);

-- ������� ����� � ������� Publishing_house
INSERT INTO Publishing_house (Name_book, City)
VALUES
('Penguin Random House', '���-����'),
('HarperCollins', '������'),
('Macmillan Publishers', '������'),
('Hachette Livre', '�����'),
('Scholastic', '���-����');

-- ������� ����� � ������� Genre
INSERT INTO Genre (Name_genre)
VALUES
('�����'),
('����������'),
('��������'),
('�����'),
('�������'),
('����');

-- ������� ����� � ������� Book
INSERT INTO Book (ID_publishing_house, ID_author, ID_genre, Book_name, Year_of_publication, Price, Descriptions)
VALUES
(1, 1, 1, '������ � ����', 2018, 150.00, '������ ������� �������� ������ ������ � ������� ����. ���� ����������: �� ������ ����, ��� ���� �������� ������ � ����, �� ������� ���������� ����� � ����� ���������, ��� ��������� ��.'),
(1, 2, 2, '1984', 2020, 180.00, '"1984" � ���� � ������������� � ��� ����� ������������ ����� �������� �������. ����� ��������� ������ ����� ����������� ���, ���� �� ��� ����� ���������, �������� � �����, ������� � �������� �������� ����� ������� ���� � ������� ������������. � ����: �� ���� �����? ��� �� �������? ���� ����� ������� ����������? �� ���� �������� ������, � ��� ���� ������ � ���������� � ������� ������ �������, � �� ������ ���� ����������� �����, ��� ���������� ��������� ���? �� ���� �������, � �� ���� ������������� � ������? �� �������� ����� ��������� ����� �������, ����� ����� � ������ ��������� ���� ��� ������ ������� ���������, ����� �� ������� �����, � ������ ��������� ���������� �����?'),
(2, 3, 1, '������� � �����������', 2024, 200.00, '��� ����� ��������� ����������� ����� ���� (1775�1817) � ��� ��������� ������� � ����, ����� ��������, ��������� � � ��� �� ��� �� ����������� ����������. ������ �������� � ������� ��������� �����, ����������� �������� ����������� ������� � ������� ������.' + CHAR(13)+CHAR(10) + '����� ���������� ����� ������ �������� � �������������� �������� ����������� ���� �� ����� ������������ ������� ������� �� ������ ��������� ������� �� ����. ���� ���������� �� �쒿 ������� ��������, � �������������, � ������ ������� ���� ��� ����. ����� ���, ���� ���� ��������, �� �� ������ ���� ���� ��� ������, �� �� ������ ���� ������� ���� �������, ��� ������� ����� �������...'),
(3, 4, 1, '������� �����', 2020, 170.00, '������ ����� Գ��������� (1896�1940) � ������������� ����������, ����� �������� ������� �� �������� ��� �������� �����������, �������� ����������� ��� ������� ����������� ���������. �������� ����᳻ � ���� ���������� �����, ���� ���� �������� �������� �����.' + CHAR(13)+CHAR(10) + '�������, ������� 20-� ���� �� �������, ��� ������� ������ ������������� �������, �������� ������ � ��������� �����.������������� ͳ� �������� ������ �� ���-����� ��������� ��������� ������, ���� � ����� � ������� ���� ��� ��� �������������. ³� � �������� ������� ��� �������, � ��� �������� ���������.' + CHAR(13)+CHAR(10) + '�������� ����� ����� ��� ���� ���������� ����, ������ �������� ������, ������ �� ������, ���������� �� ������������� �������� ������� �� ��� ���� ����� � ������� �����. �� ������, ��� �������� ���� �� ��������� ������������ ����� � ��� ���� ������, ��� ����� �� � ����������� �������. ������� �������� ����� �� ���� ��� ���������� �����䳺� �� ����� ��� �����...'),
(4, 5, 2, '������� �������', 2019, 250.00, '��������� ��������� �� ����� ������� ������� �������. �������� ��� ��. �. �. ������ �� � ��� ���� �� ������� ��������� � �������� ������� ����������. ����� ����� �������� ��������� ������� �� ���������� �����, ���� ������ �� �������. ��������� �� ������ � �������, �� �����, � �������� ����� ����������� ������ ���������� ����� ���������� ���� ���� � ��������� � ����� ������������� ���, ����� ������� ����� ������� ������ ����������. ����� ������� ���� ������� ���������� ���� � ���� �� ������� ����� � ���������.'),
(5, 6, 6, '�����', 2021, 190.00, '���� �������� ��������� ��������� ������ �� �������� �������, ���� � ����� �� ����, ���� ���������� ��� ���� �� ���� ������ ���� ��� ������� ������� �������: �������� �������� ������� ������� ������ ������. ���� ��� ��������� ����� �������, �� �� ���� ������ ��������� ��������� �������. � �� � �������. ��������, ��������� ����� ������������, ����������� ������� ���� �����. ³� ��� ���, ����� ���� ������ ������� �������'),
(5, 7, 2, '���� ������ � ������������ �����', 2023, 220.00, '����� ����� ��� ����������� ���������� �������� ���� �������. ������ �������������� �� ���������� ������� ������, ������� �������� �� �������� ����, �� ���� ���������� �� ���� �������, � �������� ����������-��������� ������� ����� ��������, �� ����� ������� ����, � ����� ���������, �� ������� ���� ��������� �� ����� ��������, ���������� �� �������� ����� ������, ��� ���������� ����� ������ ����� �������, ��� ���������� ������� ���������� �������� � ������ �� ��� � ������ �� �������� �� ���� �������� �� ������������ ���� ��������� �����������, ���� ������ �������� ������������ ����� ͳ������ �������, �������� ��������� � ����� ������ �������. �� ����� ���� �� ���� ���� � ������� �������� �� ������� ����� - ���������� ����� ���������� ����������?'),
(1, 8, 2, '��� ��������', 2021, 210.00, '����� ����� ����� - "��� ��������" - �� ���������� ��� ѳ��� ���������, �� ��� � ���� �������� �� ����� ����, � ������ ���������� �������� � ��������� ������, � ��������� ������ ������ ���������� ���� �� �������. ����� �� ��� ������� �� ���� ������� ������ ѳ� ��������� ��������� ���� �''������ ��� ������ ���������, �� ���������� ����� ������� ������� �������� ��� ���������. ������� ��������� ������� ������ ����, ���� ������������ ���� �� ������������ �������� �� �������� �� ����� ��� ��������. ��䳿 "��� ��������" ������������� � ����� ����, ��� ������ ������ �������� �, ��� ������ �������� �����.'),
(3, 9, 2, '451 ������ �� �����������', 2015, 160.00, '�� ��������� � ����� �����? ���� ��������� �������� �������, � �� ������ �����? ���� ���� �� ������� �����, �� ������ ���� � ����� �� ����������� ���� � �����? �� ����������� ���� ����� �� ����� ������ ����, ���� ���������� �� ������ �����? ǳ ������� ������ � ��������� ����� ��� ������� �� ��������, �� ���� ��������� �������� ����� ��� ��������� �������, ��� �������� ����� ������� ������� � �� ������ �� �������� ������� ����� ������ ����� ��������� ��� �������'),
(4, 10, 1, '������������', 2021, 140.00, '����� ������ ����� ���������� ������ ����� �� ��������� ����, ���������, �� �� ������������ �� ��������� ������. ϳ���� ������ � ������� ��� ���������� ����, ��������� �� ������ ���������� ��������, �� ���� ������ ���� ��������� � ��������� ���������� � �� ����� ����������, �������, ��� �������� ��������� ������ ����� ������ ��� ��� ��������������. ������ ����� ��� �ᒺ���� ������ ��� �� �쒿, ����������� � �������� ���, ������������ �������� ������. ���� ������� ������������ ��� ������������ �������, �� �������� ��������� ���� �� �������� � ������. � ������ ���������� ���� ���������, ������ ����������� �� ����������� �������� ������� � ����������� �������.  ���������� ����� �����, ���� ����� ���������� ��������� ������������� ������ ������� ������� ���� ������� ��������� �� ������� ������� � �����.'),
(1, 11, 1, '����� �����������', 2017, 175.00, '� � ������ ���� ����, �� �� ��������� �������, - �� �� ������. ������������ ����������� ������ ������ ˳ "����� �����������" ������ � ����, �� �� �������� ������� ��� ����, ������ �� ��������. ����� ����������� ��� ��������� ����, ��� ���� ����� � ��������. ���� ����� � ��� �������� ������� � ��������� ��������� ����� ����� �� ����� ˳������, ��������� ������� ������� � ��������, �� � �������� �������, ����� ��������� ��������, ������� ����������� ���� �� ������ ���. ����� �������� ������� �� ��������, �� ���� ���� ���� ������ ������.'),
(2, 12, 3, '������� ������� ������', 2018, 160.00, '����� ������� ���� ��''� ������ ����� ������ �''������� �-�� ���� ������ ����������� ����������� ������ ����� �����. �� ���� �������� ������� ������ ���� ����������� ������� �� ����������� ���������  �������� �� ������-�����, ���������������,  ���������, �������� ���������� ������������ ���������� �������... �������� ������������ ��������� ������� ����� �������� �����-��������  ������� ������ � �������, ���������� �� ���� ������ ������ �����. ��� �� ��� ��������� ��� ��� �����, ��������� �����糺� �����������? ³������ �� �� ��������� ������ �����, ��� ������� ��������� ���������� ����� ������ ����� �����. ��� ��� ������ �� ������������� �������, �� ����� ������ �� ����� ����������� ������� � ����������� �������� ��� ������� ������� ������.'),
(3, 13, 1, '����� ����� �''���', 2023, 180.00, '���� ������� (1922�2007) � ������������� ����������-�������. � ����� �� ����������� ������������� ����������� XX �������. � �������� ��������� ����� �������� ������, ������� ������ � ������� ����������. ����� ������ �5, ��� ������� ��������� ����� �������� �� ������� 100 �������� ������� ��� ����, �� ���� � ������������ � ��� ���������� ����. ��䳿 ����� ������������� �� �� ������������ ������������� �������� �� ��� ����� ������ ����. ������ ��������� ����� � ���� ϳ����� � ���� ��� �������� ������� ������ ������� ������ ������������ �����, ���� �� ���������� �������� ���� � ����, ���� ������ ��������. �� ����� ����� ������� ��� ���������� ������ ���� � ��������������� �� ������?'),
(4, 14, 4, '������', 2019, 130.00, '�� ������ � �������� ��������� ���������� �������� ���������� ����� �������, �''���, ��� �� ������� � ����� � ���� ��������� � �� �� ��������. ������� ����� ��������� �� �������� � � ��� ������� �� ��������������, ����� ����� ������ ������, ��� � �� ������� ������� ��� ������ ���������. ��� ���, � �����, ���� � ����������� �� �� ����� �������� � � ������������ ����� ���� ��������, ��������� � ������������. �� �������"�������" �������� ����� ��������� ��������� ��������� ����������� ����������� �������� � ������������ ��� ������������ �� ������������ ����������� �����. ���� ����� "�������" � �� ������� ������ �������� ���������� ��� ��-������, ������ ������ ���� ���� ������������ � ����������.'),
(5, 15, 5, '�������� ����� ��� �� �����', 2018, 210.00, '��������������� ����� �������� ������������ �������� ���� ����� (1828�1905) ��� �������� �������� � ������ ������������ ������� ������� ���� �� ���� ����� �� ��������� ����� ��������.');

-- ������� ����� � ������� Customer
INSERT INTO Customer (user_login, user_password, C_Surname, C_Name, Phone_number, Addres)
VALUES
('john_doe@gmail.com', 'password123', '���', '����', '+380501234567', '���. �����������, 10, ���'),
('jane_smith@gmail.com', 'password456', '���', '�����', '+380931234567', '���. ��������, 25, ����');

-- ������� ����� � ������� Orders
INSERT INTO Orders (ID_customer, Date_of_orders, Total_sum)
VALUES
(1, '2023-09-01', 330),
(2, '2023-09-15', 200);

--������� ����� � ������� Cart
INSERT INTO Cart (ID_orders, ID_book, Number_of_orders)
VALUES
(1, 1, 1),
(1, 2, 1),
(2, 3, 1);




--USE Book_store;

--DELETE FROM Customer
--WHERE ID_customer = 1008;

--select * from Customer

--select * from Cart
--select * from Orders

--select * from Author

--DELETE FROM Book
--WHERE ID_book IN (1005);

--DELETE FROM Genre
--WHERE Name_genre = '����';

--DELETE FROM Orders
--WHERE ID_orders = 2;

--UPDATE Cart
--SET ID_orders = 3
--WHERE ID_orders = 2;

--UPDATE Customer
--SET Is_admin = 1
--WHERE ID_customer = 4;
