import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta

JWT_SECRET_KEY = 'Bs0PzP3VV5pHtaE4M4nJblvnVphq6oVS'
JWT_ALGO = 'HS256'

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
        'exp': datetime.utcnow() + timedelta(hours=1)
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
            "w.created_date, "
            "coalesce(t1.balance, 0.0000) as balance "
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
