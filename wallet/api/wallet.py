from .base import BaseRequest
from ..exceptions import ValidationError
from ..models import create_wallet

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

