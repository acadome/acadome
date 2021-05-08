var flag = false;
const publish = document.forms['publish'];
const file = document.querySelector('#file-box label');

function max_length(field, max) {
  var _field = publish[field];
  _field.addEventListener('change', event => {
    if (_field.value.length > max) {
      _field.style.border = '#f00 solid 1px';
    } else {
      if (!_field.value.length) {
        _field.style.border = '#f00 solid 1px';
      } else {
        _field.style.border = '#0f0 solid 1px';
      }
    }
  });
}

if (publish) {
  const field_lengths = [['fname', 'lname', 'email', 'inst'], [20, 20, 40, 60]];
  field_lengths[0].forEach((field, i) => max_length(field, field_lengths[1][i]));

  // regex

  document.getElementById('file').addEventListener('change', event => {
    var filename = event.target.files[0].name;
    if (filename.slice(-4) != '.pdf') {
      file.style.border = '#f00 solid 1px';
      file.innerText = filename + ' is not a PDF';
    } else {
      file.style.border = '#0f0 solid 1px';
      file.innerText = 'Selected file: ' + filename;
      flag = true;
    }
  });

  publish.addEventListener('submit', event => {
    ['fname', 'lname', 'email'].forEach(field => {
      var _field = publish[field];
      if (!_field.value.length) {
        _field.style.border = '#f00 solid 1px';
      }
    });
    publish['inst'].style.border = '#0f0 solid 1px';
    if (!flag) {
      file.style.border = '#f00 solid 1px';
      event.preventDefault();
    }
  });
}
