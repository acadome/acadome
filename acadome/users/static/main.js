const getUser = () =>
  fetch('/account/users/static/user.json', {cache: 'no-cache'})
    .then(response => response.json());

class Validators {
  constructor(name, len, re, req=true, def=null, border=true) {
    this.name = name;
    this.length = len;
    this.regex = re;
    this.required = req;
    this.default = def;
    this.border = border;
  }
}

var name_ = new Validators(
  'name', [3, 64], /^[a-zA-Z \-\']+$/
);

var affiliation = new Validators(
  'affiliation', [256], /^[a-zA-Z0-9 \,\.\-\']*$/, false
);

var email = new Validators(
  'email', [4, 254], /\S+@\S+\.\S+/
);

var password = new Validators(
  'password', [8, 64], /\w+/
);

const route = window.location.pathname.split('/');
switch (route[2]) {
  case 'sign_up':
    new Form('sign-up-form').validate(
      [name_, affiliation, email, password]
    );
    break;

  case 'login':
    email.border = false;
    password.border = false;
    new Form('login-form').validate([email, password]);
    break;

  case 'edit':
    getUser().then(user => {
      if (!document.getElementById('password-error').innerText) {
        name_.default = user.name;
        affiliation.default = user.affiliation;
        email.default = user.email;
      }
      password.border = false;
      new Form('edit-account-form').validate(
        [name_, affiliation, email, password]
      );
    });
    break;

  case 'reset_password':
    if (route[3]) {
      new Form('reset-password-form-2').validate([password]);
      break;
    } else {
      email.border = false;
      new Form('reset-password-form-1').validate([email]);
      break;
    }

  case 'delete':
    password.border = false;
    new Form('delete-form').validate([password]);
    break;
}
