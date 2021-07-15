var name_ = new Validators(
  'name', [3, 64], /^[a-zA-Z \-\']+$/
);

var email = new Validators(
  'email', [5, 254], /\S+@\S+\.\S+/
);

var query = new Validators(
  'query', [1024], /[\s\S]+/
);

if (window.location.pathname == '/contact') {
  new Form('contact-form').validate(
    text=[name_, email, query]
  )
}
