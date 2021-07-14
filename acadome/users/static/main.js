const getUser = () =>
  fetch('/account/user_json', {cache: 'no-cache'})
    .then(response => response.json());

var name_ = new Validators(
  'name', [3, 64], /^[a-zA-Z \-\']+$/
);

var affiliation = new Validators(
  'affiliation', [256], /^[a-zA-Z0-9 \,\.\-\']*$/, false
);

var email = new Validators(
  'email', [5, 254], /\S+@\S+\.\S+/
);

var password = new Validators(
  'password', [8, 64], /^[a-zA-Z0-9!@#$%^&*_]+$/
);

const route = window.location.pathname.split('/');
switch (route[2]) {
  case 'sign_up':
    var form = new Form('sign-up-form');
    form.validate(
      text=[name_, affiliation, email, password], boolean='ua'
    );
    break;

  case 'login':
    email.border = false;
    password.border = false;
    new Form('login-form').validate(text=[email, password]);
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
        text=[name_, affiliation, email, password]
      );
    });
    break;

  case 'reset_password':
    if (route[3]) {
      new Form('reset-password-form-2').validate(text=[password]);
      break;
    } else {
      email.border = false;
      new Form('reset-password-form-1').validate(text=[email]);
      break;
    }

  case 'delete':
    password.border = false;
    new Form('delete-form').validate(text=[password]);
    break;
}
