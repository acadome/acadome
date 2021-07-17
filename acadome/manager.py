from flask import redirect, url_for, abort

class UserManager:
    def __init__(self, app):
        self._admin = app.config['ADMIN']
        self.reset_user()

    def reset_user(self):
        self.user = {}

    def set_user(self, user):
        user.pop('_id', None)
        user.pop('password', None)
        if user['email'] == self._admin:
            user['role'] = 'admin'
        self.user = user

    def user_required(self, func):
        def wrapper(*args, **kwargs):
            if not self.user:
                return redirect(url_for('users.login'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def user_denied(self, func):
        def wrapper(*args, **kwargs):
            if self.user:
                return redirect(url_for('users.account'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def access(self, role):
        def _access(func):
            def wrapper(*args, **kwargs):
                if self.user['role'] != role:
                    abort(403)
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            return wrapper
        return _access

    def redirect(self, role, route):
        def _redirect(func):
            def wrapper(*args, **kwargs):
                if self.user['role'] == role:
                    return redirect(url_for(route))
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            return wrapper
        return _redirect
