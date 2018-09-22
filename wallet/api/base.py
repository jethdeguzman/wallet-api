from ..exceptions import PermissionDenied
from ..models import Session
from ..utils import decode_session_token

class BaseRequest:
    def __init__(self, **kwargs):
        self.db_session = kwargs.get('session', Session())

    def process(self):
        raise NotImplementedError('Subclass should implement this!')

class LoginRequiredRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_account_id = None
        self._session_token = self.session_token = kwargs.get('session_token')

    @property
    def session_token(self):
        return self._session_token

    @session_token.setter
    def session_token(self, value):
        self._session_token = value
        try:
            payload = decode_session_token(value)
        except:
            raise PermissionDenied()
        
        self.current_account_id = payload['account_id']
