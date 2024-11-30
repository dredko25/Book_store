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
);
 
CREATE TABLE Customer( 
    ID_customer INT IDENTITY(1,1) PRIMARY KEY, 
    user_login VARCHAR(100), 
    user_password VARCHAR(255), 
    C_Surname VARCHAR(20), 
    C_Name VARCHAR(20),
    Phone_number VARCHAR(20), 
    Addres VARCHAR(40),
    Is_admin BIT NOT NULL DEFAULT 0
);

CREATE TABLE Orders( 
	ID_orders INT IDENTITY(1,1) PRIMARY KEY, 
	ID_customer INT FOREIGN KEY REFERENCES Customer(ID_customer) ON DELETE CASCADE, 
	Date_of_orders DATE, 
	Total_sum INT, 
	Comment VARCHAR(300) 
);
 
CREATE TABLE Cart( 
	ID_cart INT IDENTITY(1,1) PRIMARY KEY, 
	ID_orders  INT FOREIGN KEY REFERENCES Orders(ID_orders) ON DELETE CASCADE, 
	ID_book INT FOREIGN KEY REFERENCES Book(ID_book) ON DELETE CASCADE, 
	Number_of_orders INT 
);


-- Вставка даних у таблицю Author
INSERT INTO Author (A_Surname, A_Name, A_Patronymics)
VALUES
('Гемінґвей', 'Ернест', NULL),
('Оруелл', 'Джордж', NULL),
('Остін', 'Джейн', NULL),
('Фіцджеральд', 'Френсіс', 'Скотт'),
('Толкін', 'Джон', 'Рональд Руел'),
('Кінг', 'Стівен', NULL),
('Роулінг', 'Джоан', NULL),
('Мартін', 'Джордж', 'Реймонд Річард'),
('Бредбері', 'Рей', NULL),
('Кафка', 'Франц', NULL),
('Лі', 'Гарпер', NULL),
('Дойл', 'Артур', 'Конан'),
('Воннеґут', 'Курт', NULL),
('Шекспір', 'Вільям', NULL),
('Верн', 'Жуль', NULL);

-- Вставка даних у таблицю Publishing_house
INSERT INTO Publishing_house (Name_book, City)
VALUES
('Penguin Random House', 'Нью-Йорк'),
('HarperCollins', 'Лондон'),
('Macmillan Publishers', 'Лондон'),
('Hachette Livre', 'Париж'),
('Scholastic', 'Нью-Йорк');

-- Вставка даних у таблицю Genre
INSERT INTO Genre (Name_genre)
VALUES
('Роман'),
('Фантастика'),
('Детектив'),
('Драма'),
('Пригоди'),
('Жахи');

INSERT INTO Photos (Photo_data)
SELECT 
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book1.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT 
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book2.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book3.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book4.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book5.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book6.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book7.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book8.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book9.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book10.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book11.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book12.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book13.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book14.jpg', SINGLE_BLOB) AS ImageFile;

INSERT INTO Photos (Photo_data)
SELECT  
    BulkColumn 
FROM OPENROWSET(BULK 'C:\Users\dredk\Desktop\Код\Book_store\static\img\book15.jpg', SINGLE_BLOB) AS ImageFile;

-- Вставка даних у таблицю Book
INSERT INTO Book (ID_publishing_house, ID_author, ID_genre, Book_name, Year_of_publication, Price, ID_photo, Descriptions)
VALUES
(1, 1, 1, 'Старий і море', 2018, 150.00, 1, 'Старий рибалка Сантьяго вирушає далеко у відкрите море. Йому поталанило: він упіймав рибу, але вона настільки велика й дужа, що старому доводиться довго й тяжко змагатися, щоб перемогти її.'),
(1, 2, 2, '1984', 2020, 180.00, 2, '"1984" — один з найголовніших і вже точно найважливіший роман минулого сторіччя. Важко пригадати якийсь інший літературний твір, який би без зайвої манірності, настільки ж чітко, прадиво і жорстоко поставив перед загалом таку ж важливу проблематику. А саме: що таке влада? Яка її природа? Куди прямує сучасне суспільство? Що таке справжня смерть, і яка саме смерть є справжньою — фізична смерть індивіда, а чи смерть його внутрішнього єства, при збереженні фізичного тіла? Що таке свобода, і як вона співвідноситься з владою? Чи можливий бодай найменший прояв свободи, нехай навіть у вигляді можливості мати свої власні глибоко приховані, вільні від примусу думки, в умовах абсолютної тоталітарної влади?'),
(2, 3, 1, 'Гордість і упередження', 2024, 200.00, 3, 'Світ творів англійської письменниці Джейн Остін (1775—1817) — світ звичайних чоловіків і жінок, доволі буденний, розмірений і в той же час не позбавлений драматизму. Тонкий психолог і знавець людського серця, письменниця створила надзвичайно виразні й правдиві образи.' + CHAR(13)+CHAR(10) + 'Перше знайомство героїв роману «Гордість і упередженість» багатого аристократа Дарсі та дочки провінційного поміщика Елізабет не обіцяло серйозних почуттів між ними. Дарсі поставився до сім’ї Елізабет зверхньо, з упередженістю, і дівчина відповіла йому так само. Навіть тоді, коли вони зрозуміли, що не можуть жити один без одного, їм не просто було зламати свою гордість, щоб відкрити серця коханню...'),
(3, 4, 1, 'Великий Гетсбі', 2020, 170.00, 4, 'Френсіс Скотт Фіцджеральд (1896—1940) — американський письменник, автор багатьох романів та оповідань про покоління «епохиджазу», яскравий представник так званого «втраченого покоління». «Великий Гетсбі» — його найвідоміший роман, який став символом «століття джазу».' + CHAR(13)+CHAR(10) + 'Америка, початок 20-х років ХХ сторіччя, час «сухого закону»і гангстерських розбірок, яскравих вогнів і яскравого життя.Тридцятирічний Нік Каррауей приїхав до Нью-Йорка навчатися банківської справи, хоча й плекає у глибині душі мрію про письменництво. Він і розповідає читачеві про пригоду, в яку виявився втягнутим.' + CHAR(13)+CHAR(10) + 'Головним героєм оповіді стає його найближчий сусід, хазяїн великого палацу, нікому не відомий, загадковий та ексцентричний самотній молодик на ім’я Джей Гетсбі — Великий Гетсбі. Це людина, яка створила себе за рецептами американської моралі і яка дуже багата, але попри те — надзвичайно самотня. Кохання Великого Гетсбі до Дейзі стає величезною трагедією не тільки для нього...'),
(4, 5, 2, 'Володар перснів', 2019, 250.00, 5, '«Володаря Перстенів» не можна описати кількома словами. Величний твір Дж. Р. Р. Толкіна має в собі щось від героїчної романтики і класичної наукової фантастики. Однак важко передати сучасному читачеві всі особливості книги, весь спектр її значень. Почергово то комічна й домашня, то епічна, а подекуди навіть страхітлива оповідь переходить через нескінченні зміни сцен і характерів у цьому фантастичному світі, кожен елемент якого виглядає цілком реалістично. Толкін створив нову міфологію вигаданого світу — світу із власним часом і простором.'),
(5, 6, 6, 'Сяйво', 2021, 190.00, 6, 'Коли Торранси найнялися доглядати взимку за розкішним готелем, вони й гадки не мали, який невимовний жах чекає на них… Одного разу там скоїлася страшна трагедія: колишній доглядач зарубав сокирою власну родину. Саме тут п’ятирічний Денні дізнався, що він може бачити справжніх мешканців будинку. І це — привиди. Хлопчику, наділеному даром передбачення, відкривається страшна суть речей. Він уже знає, звідки його родині загрожує смерть…'),
(5, 7, 2, 'Гаррі Поттер і філософський камінь', 2023, 220.00, 7, 'Перша книга про знаменитого маленького чарівника Гаррі Поттера. Читачі познайомляться із непривітною родиною Дурслів, єдиними родичами та опікунами Гаррі, із його товаришами по школі Гоґвортс, зі славними чарівниками-вчителями головної школи чарівників, із лютим ворогом Гаррі, а також дізнаються, як вдалося Гаррі потрапити до школи чарівників, незважаючи на підступні плани Дурслів, про незвичайну сумну історію життя Поттерів, про небезпечні пригоди маленького чарівника зі шрамом на чолі в перший рік навчання та його боротьбу із найсильнішим злим чарівником Волдемортом, який вирішив викрасти філософський камінь Ніколаса Фламеля, отримати безсмертя і вбити малого Поттера. Чи зможе Гаррі та його друзі – маленькі чарівники із першого класу - зруйнувати плани могутнього Волдеморта?'),
(1, 8, 2, 'Гра престолів', 2021, 210.00, 8, 'Перша книга циклу - "Гра престолів" - це захопливий світ Сімох Королівств, де літо й зима тривають по кілька років, з півночі наступають загадкові й моторошні вороги, а вельможні родини ведуть ненастанну війну за престол. Майже за три століття до подій першого роману Сім Королівств Вестеросу було з''єднано при династії Таргарієнів, які встановили владу завдяки повному контролю над драконами. Династія Таргарієнів правила триста років, доки громадянська війна та міжособистісні конфлікти не призвели до гибелі всіх драконів. Події "Гри престолів" розгортаються у мирні часи, але завжди будуть існувати ті, хто прагне захопити владу.'),
(3, 9, 2, '451 градус за Фаренгейтом', 2015, 160.00, 9, 'Що трапилося з нашим світом? Чому пожежники спалюють будинки, а не гасять пожежі? Чому люди не читають книги, не ходять пішки і майже не розмовляють одне з одним? Як виглядатиме наша Земля та якими будуть люди, якщо заборонити їм читати книги? Зі сторінок одного з найкращих творів Рея Бредбері ви дізнаєтеся, як люди навчаться зберігати книги для наступних поколінь, хто повстане проти пануючої системи і як зустріч із “чудною” дівчиною Кларіс змінить життя пожежника Ґая Монтеґа…'),
(4, 10, 1, 'Перетворення', 2021, 140.00, 10, '«Коли Грегор Замза прокинувся одного ранку від тривожних снів, виявилося, що він перетворився на гігантську комаху. Підняв голову і побачив свій коричневий живіт, розділений на жорсткі дугоподібні сегменти, на яких ковдра ледь трималася й збиралася зісковзнути» – із цього вражаючого, дивного, але напрочуд кумедного тексту Кафка починає свій твір «Перетворення». Грегор Замза стає об’єктом ганьби для своєї сім’ї, аутсайдером у власному домі, квінтесенцією відчуженої людини. Його фізичне перетворення стає метафоричним образом, що відображає внутрішній стан та стосунки в родині. У романі підіймаються теми самотності, втрати ідентичності та безперервної боротьби індивіда з соціальними нормами.  Унікальний стиль Кафки, його вміння створювати атмосферу метафізичного страху викликає роздуми щодо природи існування та відносин індивіда зі світом.'),
(1, 11, 1, 'Убити пересмішника', 2017, 175.00, 11, 'Є у людині дещо таке, що не скориться більшості, - це її совість. Унікальність знаменитого роману Гарпер Лі "Вбити пересмішника" полягає в тому, що він однаково цікавий для дітей, підлітків та дорослих. Книга відрізняється тою яскравістю подій, яка буває тільки в дитинстві. Вона поєднує в собі захопливі пригоди в найкращих традиціях Марка Твена та Астрід Ліндгрен, моторошну таємницю будинку з привидом, як у готичних романах, гострі соціальні проблеми, питання виховування дітей та вірності собі. Книга напрочуд яскрава та правдива, як може бути лише погляд дитини.'),
(2, 12, 3, 'Пригоди Шерлока Холмса', 2018, 160.00, 12, 'Понад століття тому ім''я Шерлок Холмс уперше з''явилося з-під пера автора англійського письменника Артура Конан Дойля. Не одне покоління читачів усього світу зацікавлено стежить за дивовижними пригодами  самітника із Бейкер-стрит, спостережливого,  кмітливого, здатного розплутати найхимернішу детективну загадку... Численні шанувальники Дойлевого таланту охоче відвідують Музей-квартиру  Шерлока Холмса в Лондоні, надсилають на його адресу тисячі листів. Чим же так приваблює нас цей герой, створений фантазією письменника? Відповідь на це запитання дістане кожен, хто прочитає невмирущі детективні твори Артура Конан Дойля. Цей том перший із чотиритомного видання, до якого увійшли усі твори англійського класика в українському перекладі про пригоди Шерлока Холмса.'),
(3, 13, 1, 'Бійня номер п''ять', 2023, 180.00, 13, 'Курт Воннеґут (1922–2007) — американський письменник-фантаст. Є одним із найвагоміших американських письменників XX століття. У творчості майстерно поєднує елементи сатири, чорного гумору й наукової фантастики. Книга «Бойня №5, або Дитячий хрестовий похід» належить до переліку 100 найліпших романів усіх часів, це одна з найзначиміших у світі антивоєнних книг. Події твору розгортаються на тлі сумнозвісного бомбардування Дрездена під час Другої світової війни. Одіссея головного героя — Біллі Пілґрима — крізь час відображає безумну міфічну подорож нашого зруйнованого життя, коли ми намагаємося відшукати сенс у тому, чого боїмося найбільше. Чи зможе автор навчити нас ігнорувати жахливі часи й зосереджуватися на гарних?'),
(4, 14, 4, 'Гамлет', 2019, 130.00, 14, 'Це перший у третьому тисячолітті український переклад вершинного твору Шекспіра, п''єси, яка не сходила зі сцени з часу написання — аж до сьогодні. Гамлета можна сприймати як завгодно — у дусі класики чи постмодернізму, проте важко знайти людину, яку б не вразила трагедія про принца данського. Цей твір, в ідеалі, мало б перекладати чи не кожне покоління — з притаманними тільки йому лексикою, акцентами й нюансуванням. Це видання"Гамлета" здійснено двома знаковими постатями сучасного українського культурного простору — письменником Юрієм Андруховичем та ілюстратором Владиславом Єрком. Їхня версія "Гамлета" — це щаслива нагода пережити геніальний твір по-новому, гостро відчути його вічну актуальність і сучасність.'),
(5, 15, 5, 'Двадцять тисяч льє під водою', 2018, 210.00, 15, 'Всесвітньовідомий роман великого французького фантаста Жуля Верна (1828–1905) про сповнену небезпек і пригод навколосвітню подорож капітана Немо та його друзів на підводному човні «Наутілус».');

-- Вставка даних у таблицю Customer
INSERT INTO Customer (user_login, user_password, C_Surname, C_Name, Phone_number, Addres)
VALUES
('john_doe@gmail.com', 'password123', 'Доу', 'Джон', '+380501234567', 'вул. Незалежності, 10, Київ'),
('jane_smith@gmail.com', 'password456', 'Сміт', 'Джейн', '+380931234567', 'вул. Перемоги, 25, Львів');

-- Вставка даних у таблицю Orders
INSERT INTO Orders (ID_customer, Date_of_orders, Total_sum)
VALUES
(1, '2023-09-01', 330),
(2, '2023-09-15', 200);

--Вставка даних у таблицю Cart
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
--WHERE Name_genre = 'Тест';

--DELETE FROM Orders
--WHERE ID_orders = 2;

--UPDATE Cart
--SET ID_orders = 3
--WHERE ID_orders = 2;

--UPDATE Customer
--SET Is_admin = 1
--WHERE ID_customer = 4;
