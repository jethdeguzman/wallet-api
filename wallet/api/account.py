from .base import BaseRequest
from ..exceptions import AccountAlreadyExists, ValidationError
from ..models import create_account
from sqlalchemy.exc import IntegrityError

class CreateAccountRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')

    def process(self):
        if not self.username.isalnum():
            raise ValidationError('username')

        if len(self.password) < 6:
            raise ValidationError('password')

        try:
            data = {'username': self.username, 'password': self.password}
            account = create_account(self.db_session, **data)
            return {'id': account.uuid}
        
        except Exception as e:
            self.db_session.rollback()
            if isinstance(e, IntegrityError):
                raise AccountAlreadyExists(self.username)
            raise e
        
        finally:
            self.db_session.close()
