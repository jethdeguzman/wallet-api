from ..models import Session

class BaseRequest:
    def __init__(self, **kwargs):
        self.db_session = kwargs.get('session', Session())
        self.current_account_id = kwargs.get('current_account_id')

    def process(self):
        raise NotImplementedError('Subclass should implement this!')
