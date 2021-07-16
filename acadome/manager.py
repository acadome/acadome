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
            user['admin'] = True
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

    def admin_access(self, func):
        def wrapper(*args, **kwargs):
            if self.user['email'] != self._admin:
                abort(403)
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def admin_redirect(self, func):
        def wrapper(*args, **kwargs):
            try:
                if self.user['admin']:
                    return redirect(url_for('admin.home'))
            except KeyError:
                return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
