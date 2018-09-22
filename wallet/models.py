from datetime import datetime
from .exceptions import ValidationError
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates, relationship
from sqlite3 import Connection as SQLite3Connection
from .utils import generate_uuid, encrypt_password, get_wallets_sql_statement, get_transactions_sql_statement

engine = create_engine('sqlite:///wallet.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        cursor.close()

def validate_required_str(key, value):
    if type(value) is str and len(value) > 0:
        return value

    raise ValidationError(key)

def fetch_data(statement, params={}):
    with engine.connect() as connection:
        result = connection.execution_options(stream_results=True).execute(text(statement), **params).fetchall()
        connection.close()
        return result

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
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

    id = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    currency = Column(String(3), nullable=False, default='PHP')
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    account_id = Column(String(64), ForeignKey('accounts.id'))
    account = relationship('Account', backref='wallets')

    def __repr__(self):
        return self.uuid

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    type = Column(String(16), nullable=False, default='CREDIT') #VALUES: CREDIT, DEBIT
    description = Column(String(255), nullable=False, default='RECEIVE_MONEY') #VALUES: SEND_MONEY, RECEIVE_MONEY, DEPOSIT, WITHDRAWAL
    amount = Column(Numeric(28, 4), default='0.0000')
    balance = Column(Numeric(28, 4), default='0.0000')
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    wallet_id = Column(String(64), ForeignKey('wallets.id'))
    wallet = relationship('Wallet', backref='transactions')
    related_transaction_id = Column(String(64), ForeignKey('transactions.id'))
    related_transaction = relationship('Transaction', backref='related_transactions', remote_side='Transaction.id')

    def __repr__(self):
        return self.uuid

Base.metadata.create_all(engine)

def create_account(session, username=None, password=None):
    account = Account(username=username, password=encrypt_password(password))
    session.add(account)
    session.commit()
    return account

def get_account_by_username(session, username):
    account = session.query(Account) \
        .filter_by(username=username) \
        .first()

    return account

def create_wallet(session, account_id=None, currency=None):
    wallet = Wallet(account_id=account_id, currency=currency)
    session.add(wallet)
    session.commit()
    return wallet

def get_wallets(filters):
    statement = get_wallets_sql_statement(filters=filters)
    return fetch_data(statement, params=filters)

def get_transactions(filters):
    statement = get_transactions_sql_statement(filters=filters)
    return fetch_data(statement, params=filters)
