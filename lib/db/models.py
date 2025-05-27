from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def create(self, session):
        if session.query(User).filter_by(username=self.username).first():
            raise ValueError("Username already exists")
        session.add(self)
        session.commit()
        return self

    @classmethod
    def delete(cls, session, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
        return user

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).first()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan")

    def create(self, session):
        if session.query(Category).filter_by(name=self.name, user_id=self.user_id).first():
            raise ValueError("Category already exists for this user")
        session.add(self)
        session.commit()
        return self

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # String instead of Enum
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")

    def create(self, session):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if self.type not in ['income', 'expense']:
            raise ValueError("Type must be 'income' or 'expense'")
        session.add(self)
        session.commit()
        return self