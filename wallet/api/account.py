from .base import BaseRequest
from ..exceptions import AccountAlreadyExists, ValidationError, InvalidLoginCredentials
from ..models import create_account, get_account_by_username
from sqlalchemy.exc import IntegrityError
from ..utils import verify_password, generate_session_token

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
            return {'id': account.id}
        
        except Exception as e:
            self.db_session.rollback()
            if isinstance(e, IntegrityError):
                raise AccountAlreadyExists(self.username)
            raise e
        
        finally:
            self.db_session.close()

class LogInAccountRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')

    def process(self):
        try:
            account = get_account_by_username(self.db_session, self.username)

            if not account or not verify_password(self.password, account.password):
                raise InvalidLoginCredentials()

            return {'session_token': generate_session_token(account.id)}
        except:
            raise

        finally:
            self.db_session.close()
