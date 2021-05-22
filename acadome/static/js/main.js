// SEARCH
const search = document.forms['search-form'];
var flag = 0;
if (search) {
  search.addEventListener('submit', event => {
    _search = search['search'];
    if (_search.value.length > 128 || !_search.value.trim().length) {
      event.preventDefault();
    }
  });
}

// ARTICLES AND PROFILES
const articles = document.querySelectorAll('article');
var t = [];
if (articles) {
  articles.forEach((article, i) => {
    t.push(false);
    article.addEventListener('click', event => {
      if (event.target.nodeName != 'A') {
        if (t[i]) {
          event.currentTarget.querySelector('.expand').style.display = 'none';
          event.currentTarget.className = '';
          event.currentTarget.style.color = '#000';
          event.currentTarget.style.backgroundColor = '#fff';
          t[i] = false;
        } else {
          event.currentTarget.querySelector('.expand').style.display = 'block';
          event.currentTarget.className = 'active';
          event.currentTarget.style.color = '#fff';
          event.currentTarget.style.backgroundColor = '#187890';
          t[i] = true;
        }
      }
    });
  });
}


// FORMS
var red = '#f00 solid 1px';
var green = '#0f0 solid 1px';

function length(field, max) {
  if (field.value.length > max) {
    return false
  } else {
    return true;
  }
}

// PUBLISH
const publish = document.forms['publish-form'];
var flag1 = 0;
var flag2 = false;

if (publish) {
  const field_val = [['name', 64, /^[a-zA-Z \-\']+$/],
  ['email', 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$/],
  ['affiliation', 256, /^[a-zA-Z0-9 \,\.\-\']*$/]];
  field_val.forEach(fv => {
    var _field = publish[fv[0]];
    _field.addEventListener('change', () => {
      var subflag1 = length(_field, fv[1]);
      var subflag2 = fv[2].test(_field.value);
      if (subflag1 && subflag2) {
        _field.style.border = green;
        document.getElementById(`${_field.name}-error`).innerText = '';
      } else if (_field.value) {
        _field.style.border = red;
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (subflag2) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
        flag1++;
      } else {
        _field.style.border = red;
        flag1++;
      }
    });
  });

  const file = publish['file-name'];
  document.getElementById('file').addEventListener('change', event => {
    if (event.target.files[0]) {
      var filename = event.target.files[0].name;
      file.value = filename;
      if (filename.slice(-4).toLowerCase() == '.pdf') {
        file.style.border = green;
        document.getElementById('file-error').innerText = '';
        flag2 = true;
      } else {
        file.style.border = red;
        document.getElementById('file-error').innerText = 'Invalid file type. Please upload a PDF.';
        flag2 = false;
      }
    }
  });

  publish.addEventListener('submit', event => {
    ['name', 'email'].forEach(field => {
      var _field = publish[field];
      if (!_field.value.trim().length) {
        _field.style.border = red;
        flag1++;
      }
    });
    if (!flag2) {
      file.style.border = red;
    }
    if (!(publish['agreement'].checked)) {
      flag1++;
    }
    if (flag1 || !flag2) {
      event.preventDefault();
    } else {
      document.getElementById('loader').style.visibility = 'visible';
    }
    flag1 = 0;
  });
}

// CONTACT
const contact = document.forms['contact-form'];
var flag3 = 0;

if (contact) {
  const field_val = [['name', 64, /^[a-zA-Z \-\']+$/],
  ['email', 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$/],
  ['query', 1024, /^[a-zA-Z0-9 \,\.\-\'\r\n]+$/]];
  field_val.forEach(fv => {
    var _field = contact[fv[0]];
    _field.addEventListener('change', () => {
      var subflag1 = length(_field, fv[1]);
      var subflag2 = fv[2].test(_field.value)
      if (subflag1 && subflag2) {
        _field.style.border = green;
        document.getElementById(`${_field.name}-error`).innerText = '';
      } else if (_field.value) {
        _field.style.border = red;
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (subflag2) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
        flag3++;
      } else {
        _field.style.border = red;
        flag1++;
      }
    });
  });

  contact.addEventListener('submit', event => {
    field_val.forEach(fv => {
      var _field = contact[fv[0]];
      if (!_field.value.trim().length) {
        _field.style.border = red;
        flag3++;
      }
    });
    if (flag3) {
      event.preventDefault();
    } else {
      document.getElementById('loader').style.visibility = 'visible';
    }
    flag3 = 0;
  });
}
