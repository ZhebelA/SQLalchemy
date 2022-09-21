import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

login = 'postgres'
password = 'postgres'
dbname = 'alchemy'
DSN = f'postgresql://{login}:{password}@localhost:5432/{dbname}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Publisher {self.id}:{self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="pub")
    
    def __str__(self):
        return f'Publisher {self.id}: ({self.title}, {self.id_publisher})'

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), nullable=False)
        
    def __str__(self):
        return f'Shop {self.id}: ({self.name})'

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref="book")
    shop = relationship(Shop, backref="shop")
    
    def __str__(self):
        return f'Stock {self.id}: ({self.id_publisher}, {self.id_shop}, {self.count})'

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="stock")
    
    def __str__(self):
        return f'Stock {self.id}: ({self.price}, {self.date_sale}, {self.id_stock}, {self.count})'
    

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

create_tables(engine)

fp1 = Publisher(name = 'WestEagle')
fp2 = Publisher(name = 'OstVogel')

book1 = Book(title = 'Under the Cuckoos Nest', publisher = fp1)
book2 = Book(title = 'lord of the Flies', publisher = fp2)

sh1 = Shop(name = 'Seagull')
sh2 = Shop(name = 'Mowe')

st1 = Stock(count = '3', shop = sh1, book = book1)
st2 = Stock(count = '2', shop = sh2, book = book2)

sale1 = Sale(price = '345', date_sale = '23.11.2022', count = '3', stock = st1)
sale2 = Sale(price = '158', date_sale = '24.11.2022', count = '1', stock = st2)

session.add_all([fp1, fp2, book1, book2, sh1, sh2, st1, st2, sale1, sale2])
session.commit()


def seek():
    publisher = input('Введите название издателя: ')
    subq = session.query(Publisher).filter(Publisher.name.like(f"%{publisher}%")).subquery('pub')
    q = session.query(Book).join(subq, Book.id_publisher == subq.c.id).subquery("bk")
    q2 = session.query(Stock).join(q, Stock.id_shop == q.c.id).subquery("stock")
    q3 = session.query(Shop).join(q2, Shop.id == q2.c.id_shop)
    for s in q3.all():
        print(f'{publisher} is in {s.name}')
    
seek()