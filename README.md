# Simple Wallet API

An API service that create and list all wallets with their balance and transactions.

## Available API Requests
* CreateAccountRequest
* LogInAccountRequest
* CreateWalletRequest
* GetWalletsRequest
* GetWalletRequest
* GetTransactionsRequest

### CreateAccountRequest
This will create an account. It requires a `username` and `password` and will return an account `id`.
 
```python
from wallet.api import CreateAccountRequest

data = {
    'username': 'sampleuser',
    'password': 'samplepassword'
}

request = CreateAccountRequest(**data)
account = request.process()
#{'id': 'd410761d-d506-48c7-9cfc-4c29e2ed17c4'}
```

### LogInAccountRequest
This will log in an account. It requires a `username` and `password` and will return a `session_token` that will be required to access other resources.

```python
from wallet.api import LogInAccountRequest

data = {
    'username': 'sampleuser',
    'password': 'samplepassword'
}

request = LogInAccountRequest(**data)
login = request.process()
#{'session_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiZDQxMDc2MWQtZDUwNi00OGM3LTljZmMtNGMyOWUyZWQxN2M0IiwiZXhwIjoxNTM3NjIwOTIzfQ.X_A6QgABz0KXJH9dvu2JOO42bUDhhjyBck57iri96cU'}
```

### CreateWalletRequest
This will create a wallet under a specific account. It requires a `session_token` and `currency` and will return an wallet a `id`.
 
```python
from wallet.api import CreateWalletRequest

data = {
    'session_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiZDQxMDc2MWQtZDUwNi00OGM3LTljZmMtNGMyOWUyZWQxN2M0IiwiZXhwIjoxNTM3NjIwOTIzfQ.X_A6QgABz0KXJH9dvu2JOO42bUDhhjyBck57iri96cU',
    'currency': 'PHP'
}

request = CreateWalletRequest(**data)
wallet = request.process()
#{'id': '00da69c1-5dd9-4a99-b7f2-349074e43488'}
```

### GetWalletsRequest
This will list all wallets under a specific account. It requires a `session_token` and will return a list of `wallets`.
```python
from wallet.api import GetWalletsRequest

data = {
    'session_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiZDQxMDc2MWQtZDUwNi00OGM3LTljZmMtNGMyOWUyZWQxN2M0IiwiZXhwIjoxNTM3NjIwOTIzfQ.X_A6QgABz0KXJH9dvu2JOO42bUDhhjyBck57iri96cU',
}

request = GetWalletsRequest(**data)
wallets = request.process()
#[{'id': 'a8c1808e-29a9-4ac7-ab5e-18572363a2d9', 'account_id': '52750ca8-e093-43c7-af63-204cc491fdfd', 'currency': 'BTC', 'balance': 800, 'created_date': '2018-09-22 12:01:34.261539'}, {'id': '00da69c1-5dd9-4a99-b7f2-349074e43488', 'account_id': '52750ca8-e093-43c7-af63-204cc491fdfd', 'currency': 'PHP', 'balance': 0.0, 'created_date': '2018-09-22 11:58:05.516999'}]
```

### GetWalletRequest
This will retrieve a wallet under a specific account. It requires a `session_token` and `wallet_id` and will return a `wallet`.
```python
from wallet.api import GetWalletRequest

data = {
    'session_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiZDQxMDc2MWQtZDUwNi00OGM3LTljZmMtNGMyOWUyZWQxN2M0IiwiZXhwIjoxNTM3NjIwOTIzfQ.X_A6QgABz0KXJH9dvu2JOO42bUDhhjyBck57iri96cU',
    'wallet_id': 'a8c1808e-29a9-4ac7-ab5e-18572363a2d9'
}

request = GetWalletsRequest(**data)
wallets = request.process()
#{'id': 'a8c1808e-29a9-4ac7-ab5e-18572363a2d9', 'account_id': '52750ca8-e093-43c7-af63-204cc491fdfd', 'currency': 'BTC', 'balance': 800, 'created_date': '2018-09-22 12:01:34.261539'}
```

### GetTransactionsRequest
This will retrieve list of transactions under a specific wallet. It requires a `session_token` and `wallet_id` and will return a list of `transactions`.
```python
from wallet.api import GetTransactionsRequest

data = {
    'session_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiZDQxMDc2MWQtZDUwNi00OGM3LTljZmMtNGMyOWUyZWQxN2M0IiwiZXhwIjoxNTM3NjIwOTIzfQ.X_A6QgABz0KXJH9dvu2JOO42bUDhhjyBck57iri96cU',
    'wallet_id': 'a8c1808e-29a9-4ac7-ab5e-18572363a2d9'
}

request = GetTransactionsRequest(**data)
transactions = request.process()
#[{'id': '884a8b3e-74ef-472c-869b-a57269c4d1dc', 'type': 'DEBIT', 'description': 'SEND_MONEY', 'amount': 200, 'related_transaction_id': 'be9b0e8d-fc7f-4ffa-a8c1-75bc8044683a', 'created_date': '2018-09-22 12:30:42.034378'}, {'id': 'adf13f4a-745e-4e06-b887-e6419a9a048b', 'type': 'CREDIT', 'description': 'RECEIVE_MONEY', 'amount': 1000, 'related_transaction_id': '95023d69-25b1-4b2b-9dc5-7fd596261776', 'created_date': '2018-09-22 12:18:42.034378'}]
```
