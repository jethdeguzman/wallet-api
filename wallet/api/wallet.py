from .base import BaseRequest
from ..exceptions import ValidationError
from ..models import create_wallet, get_wallets

class CreateWalletRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.currency = kwargs.get('currency')
    
    def process(self):
        if len(self.currency) > 3:
            raise ValidationError('currency')

        try:
            data = {'account_id': self.current_account_id, 'currency': self.currency}
            wallet = create_wallet(self.db_session, **data)
            return {'id': wallet.id}
        
        except:
            self.db_session.rollback()
            raise
        
        finally:
            self.db_session.close()

class GetWalletsRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process(self):
        try:
            return [{
                'id': wallet[0],
                'account_id': wallet[1],
                'currency': wallet[2],
                'created_date': wallet[3]
            } for wallet in get_wallets({'account_id': self.current_account_id})]
        except:
            raise
        finally:
            self.db_session.close()
