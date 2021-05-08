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

const publish = document.forms['publish-form'];
const file = document.getElementById('file-name');
var flag1 = 0;
var flag2 = false;

function length(field, max) {
  if (field.value.length > max) {
    return false
  } else if (field.value.trim() != field.value) {
    return false;
  } else {
    return true;
  }
}

if (publish) {
  const field_val = [['name', 64, /^[a-zA-Z \-\']+$/],
  ['email', 64, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$/], ['inst', 128, /^[a-zA-Z0-9 \-\']+$/]];
  field_val.forEach(field => {
    var _field = publish[field[0]];
    _field.addEventListener('change', () => {
      var subflag1 = length(_field, field[1]);
      var subflag2 = field[2].test(_field.value)
      if (subflag1 && subflag2) {
        _field.style.border = '#0f0 solid 1px';
      } else {
        _field.style.border = '#f00 solid 1px';
        flag1++;
      }
    });
  });

  document.getElementById('file').addEventListener('change', event => {
    if (event.target.files[0]) {
      var filename = event.target.files[0].name;
      file.value = filename;
      if (filename.slice(-4).toLowerCase() == '.pdf') {
        file.style.border = '#0f0 solid 1px';
        flag2 = true;
      } else {
        file.style.border = '#f00 solid 1px';
        flag2 = false;
      }
    }
  });

  publish.addEventListener('submit', event => {
    ['name', 'email'].forEach(field => {
      var _field = publish[field];
      if (!_field.value.trim().length) {
        _field.style.border = '#f00 solid 1px';
        flag1++;
      }
    });
    publish['inst'].style.border = '#0f0 solid 1px';
    if (!flag2) {
      file.style.border = '#f00 solid 1px';
    }
    if (!(!flag1 && flag2)) {
      event.preventDefault();
    }
    flag1 = 0;
  });
}