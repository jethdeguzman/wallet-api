from .base import LoginRequiredRequest
from ..models import get_transactions

class GetTransactionsRequest(LoginRequiredRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wallet_id = kwargs.get('wallet_id')

    def process(self):
        try:
            transactions = get_transactions({
                'account_id': self.current_account_id,
                'wallet_id': self.wallet_id
            })
            
            return [{
                'id': transaction[0],
                'type': transaction[1],
                'description': transaction[2],
                'amount': transaction[3],
                'created_date': transaction[4],
            } for transaction in transactions]
       
        except:
            raise
        finally:
            self.db_session.close()

