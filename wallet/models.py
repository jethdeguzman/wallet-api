from datetime import datetime
from .exceptions import ValidationError
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates, relationship
from .utils import generate_uuid, encrypt_password

engine = create_engine('sqlite:///wallet.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def validate_required_str(key, value):
    if type(value) is str and len(value) > 0:
        return value

    raise ValidationError(key)

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)
    username = Column(String(255), nullable=False, unique=True, default='')
    password = Column(String(255), nullable=False, default='')
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return self.uuid

    @validates('username')
    def validate_username(self, key, username):
        return validate_required_str(key, username)

    @validates('password')
    def validate_password(self, key, password):
        return validate_required_str(key, password)

class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)
    currency = Column(String(3), nullable=False, default='PHP')
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    account_id = Column(String(64), ForeignKey('accounts.id'))
    account = relationship('Account', backref='wallets')

    def __repr__(self):
        return self.uuid

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, default=generate_uuid)
    type = Column(String(16), nullable=False, default='CREDIT')
    description = Column(String(255), nullable=False, default='')
    amount = Column(Numeric(28, 4), default='0.0000')
    balance = Column(Numeric(28, 4), default='0.0000')
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    wallet_id = Column(String(64), ForeignKey('wallets.id'))
    wallet = relationship('Wallet', backref='transactions')

    def __repr__(self):
        return self.uuid

Base.metadata.create_all(engine)

def create_account(session, username=None, password=None):
    account = Account(username=username, password=encrypt_password(password))
    session.add(account)
    session.commit()
    return account
