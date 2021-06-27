var red = '#d11a2a';
var green = '#00ab66';

function _length(field, max) {
  if (field.value.length > max) {
    return false;
  } else {
    return true;
  }
}

function _fail(field) {
  field.style.padding = '9px 19px';
  field.style.border = `${red} solid 2px`;
  return false;
}

function _pass(field) {
  field.style.padding = '9px 19px';
  field.style.border = `${green} solid 2px`;
  return true;
}

// PUBLISH
const publish = document.forms['publish-form'];
if (publish) {
  var flags = [false, false, true, false, false];
  const field_val = [['name', 64, /^[a-zA-Z \-\']+$/],
  ['email', 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$/],
  ['affiliation', 256, /^[a-zA-Z0-9 \,\.\-\']*$/]];
  field_val.forEach((fv, i) => {
    var _field = publish[fv[0]];
    _field.addEventListener('change', () => {
      var subflag1 = _length(_field, fv[1]);
      var subflag2 = fv[2].test(_field.value);
      if (subflag1 && subflag2) {
        flags[i] = _pass(_field);
        document.getElementById(`${_field.name}-error`).innerText = '';
      } else if (_field.value) {
        flags[i] = _fail(_field);
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (!subflag1) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
      } else {
        flags[i] = _fail(_field);
      }
    });
  });

  const file = publish['file-name'];
  document.getElementById('file').addEventListener('change', event => {
    if (event.target.files[0]) {
      var upload = event.target.files[0];
      file.value = upload.name;
      if (upload.name.slice(-4).toLowerCase() != '.pdf') {
        flags[3] = _fail(file);
        document.getElementById('file-error').innerText = 'Invalid file type. Please upload a PDF.';
      } else if (upload.size > 20971520) {
        flags[3] = _fail(file);
        document.getElementById('file-error').innerText = 'File size exceeds 20MB.';
      } else {
        flags[3] = _pass(file);
        document.getElementById('file-error').innerText = '';
      }
    }
  });

  publish['agreement'].addEventListener('change', event => {
    if (event.target.checked) {
      publish['agreement'].style.outline = `2px solid ${green}`;
      flags[4] = true;
    } else {
      publish['agreement'].style.outline = `2px solid ${red}`;
      flags[4] = false;
    }
  });

  publish.addEventListener('submit', event => {
    ['name', 'email'].forEach((field, i) => {
      var _field = publish[field];
      if (!_field.value.trim().length) {
        flags[i] = _fail(_field);
      }
    });
    if (!flags[3]) {
      flags[3] = _fail(file);
    }
    if (!publish['agreement'].checked) {
      publish['agreement'].style.outline = `2px solid ${red}`;
      flags[4] = false;
    }
    if (flags.includes(false)) {
      event.preventDefault();
    } else {
      document.getElementById('spinner').style.visibility = 'visible';
    }
  });
}

// CONTACT
const contact = document.forms['contact-form'];
if (contact) {
  var flags = [false, false, false];
  const field_val = [['name', 64, /^[a-zA-Z \-\']+$/],
  ['email', 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$/],
  ['query', 1024, /^[a-zA-Z0-9 \,\.\-\'\r\n]+$/]];
  field_val.forEach((fv, i) => {
    var _field = contact[fv[0]];
    _field.addEventListener('change', () => {
      var subflag1 = _length(_field, fv[1]);
      var subflag2 = fv[2].test(_field.value)
      if (subflag1 && subflag2) {
        flags[i] = _pass(_field);
        document.getElementById(`${_field.name}-error`).innerText = '';
      } else if (_field.value) {
        flags[i] = _fail(_field);
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (!subflag1) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
      } else {
        flags[i] = _fail(_field);
      }
    });
  });

  contact.addEventListener('submit', event => {
    field_val.forEach((fv, i) => {
      var _field = contact[fv[0]];
      if (!_field.value.trim().length) {
        flags[i] = _fail(_field);
      }
    });
    if (flags.includes(false)) {
      event.preventDefault();
    } else {
      document.getElementById('spinner').style.visibility = 'visible';
    }
  });
}