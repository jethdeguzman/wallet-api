import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta

JWT_SECRET_KEY = 'Bs0PzP3VV5pHtaE4M4nJblvnVphq6oVS'
JWT_ALGO = 'HS256'
JWT_EXPIRATION_HOURS = 1

def generate_uuid():
    return str(uuid.uuid4())

def encrypt_password(password):
    if not isinstance(password, str):
        raise TypeError('password should be string')
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)

    return hashed.decode()

def verify_password(password, hashed):
    if not isinstance(password, str):
        raise TypeError('password should be string')

    if not isinstance(hashed, str):
        raise TypeError('hashed should be string')

    return hashed.encode() == bcrypt.hashpw(password.encode(), hashed.encode())

def generate_session_token(account_id):
    payload = {
        'account_id': account_id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }

    return jwt.encode(payload, JWT_SECRET_KEY,  algorithm=JWT_ALGO).decode()

def get_wallets_sql_statement(filters={}):
    column_map = {'id': 'w.id', 'account_id': 'w.account_id'}
    filter_statement = ' and '.join(["%s = :%s" % (column_map[k], k) for k, v in filters.items()])
    where_clause = 'where %s' % filter_statement if len(filter_statement) > 0 else ''
    
    return (
        "select "
            "w.id, "
            "w.account_id, "
            "w.currency, "
            "coalesce(t1.balance, 0.0000) as balance, "
            "w.created_date "
        "from "
            "wallets w "
        "left join ( "
            "select "
                "t.wallet_id, "
                "t.balance "
            "from "
                "transactions t "
            "order by "
                "t.wallet_id, "
                "t.created_date desc "
            "limit 1 "
        ") t1 on t1.wallet_id = w.id %s "
        "order by w.created_date desc; "
    ) % (where_clause)


def get_transactions_sql_statement(filters={}):
    column_map = {'account_id': 'w.account_id', 'wallet_id': 't.wallet_id', 'type': 't.type'}
    filter_statement = ' and '.join(["%s = :%s" % (column_map[k], k) for k, v in filters.items()])
    where_clause = 'where %s' % filter_statement if len(filter_statement) > 0 else ''
    return (
        "select "
            "t.id, "
            "t.type, "
            "t.description, "
            "t.amount, "
            "t.created_date, "
            "t.balance, "
            "t.wallet_id, "
            "w.currency, "
            "w.account_id "
        "from "
            "transactions t "
        "left join "
            "wallets w "
        "on w.id = t.wallet_id %s "
        "order by t.created_date desc;"
    ) % (where_clause)
