
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String)
    categories = relationship("Category", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

    def create(self, session):
        if session.query(User).filter_by(username=self.username).first():
            raise ValueError("Username already exists")
        session.add(self)
        session.commit()
        return self

    @classmethod
    def delete(cls, session, user_id):
        user = session.get(cls, user_id)
        if user:
            session.delete(user)
            session.commit()
        return user

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, user_id):
        return session.get(cls, user_id)

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).first()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")

    def create(self, session):
        if session.query(Category).filter_by(name=self.name, user_id=self.user_id).first():
            raise ValueError("Category already exists for this user")
        session.add(self)
        session.commit()
        return self

    @classmethod
    def delete(cls, session, category_id):
        category = session.get(cls, category_id)
        if category:
            session.delete(category)
            session.commit()
        return category

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, category_id):
        return session.get(cls, category_id)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    description = Column(String)
    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")

    def create(self, session):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        session.add(self)
        session.commit()
        return self

    @classmethod
    def delete(cls, session, transaction_id):
        transaction = session.get(cls, transaction_id)
        if transaction:
            session.delete(transaction)
            session.commit()
        return transaction

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, transaction_id):
        return session.get(cls, transaction_id)
