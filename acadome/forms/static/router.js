const getArticle = id =>
  fetch(`/admin/article_json/${id}`, {cache: 'no-cache'})
    .then(response => response.json());

const getUser = () =>
  fetch('/account/user_json', {cache: 'no-cache'})
    .then(response => response.json());

function initArticleVal() {
  const title = new TextVal(
    name='title', required=true, length=[0, 256], regex=/^[\s\S]*$/
  )

  const authors = new TextVal(
    name='authors', required=false, length=[0, 256], regex=/^[\s\S]*$/
  )

  const abstract = new TextVal(
    name='abstract', required=true, length=[0, 2048], regex=/^[\s\S]*$/
  )

  const keywords = new TextVal(
    name='keywords', required=true, length=[0, 256], regex=/^[\s\S]*$/
  )

  const preprint = new FileVal(
    name='preprint', formats=['.pdf'], size=5
  )

  const images = new FileVal(
    name='images', formats=['.jpg', '.png'], size=1
  )

  const reviewers = new TextVal(
    name='reviewers', required=false, length=[0, 256], regex=/^[\s\S]*$/
  )

  return {
    'title': title,
    'authors': authors,
    'abstract': abstract,
    'keywords': keywords,
    'preprint': preprint,
    'images': images,
    'reviewers': reviewers
  }
}

function initUserVal() {
  const name_ = new TextVal(
    name='name', required=true, length=[3, 64], regex=/^[a-zA-Z ]*$/
  )

  const affiliation = new TextVal(
    name='affiliation', required=false, length=[0, 256], regex=/^[\s\S]*$/
  )

  const email = new TextVal(
    name='email', required=true, length=[5, 254], regex=/^\S+@\S+\.\S+$/
  )

  const password = new TextVal(
    name='password', required=true, length=[8, 64], regex=/^\S*$/
  )

  const query = new TextVal(
    name='query', required=true, length=[0, 2048], regex=/^[\s\S]*$/
  )

  return {
    'name_': name_,
    'affiliation': affiliation,
    'email': email,
    'password': password
  }
}

var form = document.querySelector('form');
switch (form.id.split('-form')[0]) {
  case 'search':
    form.addEventListener('submit', event => {
      if (!form.elements['search'].value.trim().length) {
        event.preventDefault();
      }
    });

  case 'field':
    form.addEventListener('submit', event => event.preventDefault());
    const select = form.elements['field'];
    select.addEventListener('change', () => {
      document.querySelectorAll('.article').forEach(article => {
        if (article.className.includes(select.value)) {
          article.style.display = 'block';
        } else {
          article.style.display = 'none';
        }
        if (document.querySelectorAll(`.${select.value}`).length) {
          document.querySelector('.no-results').classList.add('hidden');
        } else {
          document.querySelector('.no-results').classList.remove('hidden');
        }
      });
    });
    break;

  case 'publish':
    var article = initArticleVal();
    form = new ValidateForm(form.id);
    ['title', 'authors', 'abstract', 'keywords', 'reviewers'].forEach(field => form.validateText(article[field]));
    form.validateSelect('field');
    form.validateBoolean('pa');
    form.validateFile(article.preprint);
    form.validateFile(article.images);
    form.submit();
    break;

  case 'edit-article':
    const id = window.location.pathname.split('/')[3];
    getArticle(id).then(article => {
      var article_ = initArticleVal();
      form = new ValidateForm(form.id);
      article_.title.preset = article['title'];
      article_.authors.required = true;
      article_.authors.preset = article['authors'].join(', ');
      article_.abstract.preset = article['abstract'];
      article_.keywords.preset = article['keywords'].join(', ');
      article_.reviewers.preset = article['reviewers'];
      ['title', 'authors', 'abstract', 'keywords', 'reviewers'].forEach(field => form.validateText(article_[field]));
      form.validateSelect('field', article['field']);
      form.submit();
    });
    break;

  case 'update-status':
    function assign_editor(status) {
      const editor = document.getElementById('editor').classList;
      status.value == 'Accepted' ? editor.remove('hidden') : editor.add('hidden');
    }
    const status = form.elements['status'];
    assign_editor(status);
    status.addEventListener('change', () => assign_editor(status));
    break;

  case 'sign-up':
    var user = initUserVal();
    form = new ValidateForm(form.id);
    ['name_', 'affiliation'].forEach(field => form.validateText(user[field]));
    user.email.dbVal = 'unique';
    form.validateEmail(user.email);
    form.validatePassword(user.password);
    form.validateBoolean('ua');
    form.submit();
    break;

  case 'login':
    var user = initUserVal();
    form = new ValidateForm(form.id);
    user.email.border = false;
    user.email.dbVal = 'verified';
    form.validateEmail(user.email);
    user.password.border = false;
    user.password.dbVal = 'check';
    form.validatePassword(user.password);
    form.submit();
    break;

  case 'edit-account':
    getUser().then(user => {
      var user_ = initUserVal();
      form = new ValidateForm(form.id);
      user_.name_.preset = user.name;
      user_.affiliation.preset = user.affiliation;
      ['name_', 'affiliation'].forEach(field => form.validateText(user_[field]));
      user_.email.preset = user.email;
      user_.email.dbVal = 'unique';
      form.validateEmail(user_.email);
      user_.password.border = false;
      user_.password.dbVal = 'check';
      form.validatePassword(user_.password);
      form.submit();
    });
    break;

  case 'request-reset':
    var user = initUserVal();
    form = new ValidateForm(form.id);
    user.email.border = false;
    user.email.dbVal = 'verified';
    form.validateEmail(user.email);
    form.submit();
    break;

  case 'reset-password':
    var user = initUserVal();
    form = new ValidateForm(form.id);
    form.validatePassword(user.password);
    form.submit();
    break;

  case 'delete':
    getUser().then(user => {
      var user_ = initUserVal();
      form = new ValidateForm(form.id);
      user_.email.preset = user['email'];
      form.validateEmail(user_.email);
      user_.password.border = false;
      user_.password.dbVal = 'check';
      form.validatePassword(user_.password);
      form.submit();
    });
    break;

  case 'contact':
    var user = initUserVal();
    var form = new ValidateForm(form.id);
    [name_, query].forEach(field => form.validateText(user[field]));
    form.validateEmail(user.email);
    form.submit()
}
