class AccountAlreadyExists(Exception):
    def __init__(self, username):
        self.username = username
        self.message = 'Account with username %s already exists' % self.username

    def __str__(self):
        return self.message

class ValidationError(Exception):
    def __init__(self, field):
        self.field = field
        self.message = 'Validation error on field %s' % self.field

    def __str__(self):
        return self.message

class InvalidLoginCredentials(Exception):
    def __init__(self):
        self.message = 'Invalid username or password'

    def __str__(self):
        return self.message
