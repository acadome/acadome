from flask import redirect, url_for
import json

class UserManager:
    def __init__(self, app):
        self._path = app.config['PATH_TO_USER_JSON']
        self.reset_user()

    def reset_user(self):
        self.user = {}
        with open(self._path, 'w') as file:
            file.write('{}')

    def set_user(self, user):
        if not self.user:
            user.pop('_id', None)
            user.pop('password', None)
            self.user = user
            with open(self._path, 'w') as file:
                file.write(json.dumps(user, indent=4, default=str))

    def access_required(self, func):
        def wrapper(*args, **kwargs):
            if not self.user:
                return redirect(url_for('users.login'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def access_restricted(self, func):
        def wrapper(*args, **kwargs):
            if self.user:
                return redirect(url_for('users.account'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
