// FORMS
var red = '#f00 solid 1px';
var green = '#0f0 solid 1px';

function length(field, max) {
  if (field.value.length > max) {
    return false;
  } else {
    return true;
  }
}

// PUBLISH
const publish = document.forms['publish-form'];
if (publish) {
  var flags = [false, false, true, false, false];
  const field_val = [['name', 64, /^[a-zA-Z \-\']+$/],
  ['email', 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$/],
  ['affiliation', 256, /^[a-zA-Z0-9 \,\.\-\']*$/]];
  field_val.forEach((fv, i) => {
    var _field = publish[fv[0]];
    _field.addEventListener('change', () => {
      var subflag1 = length(_field, fv[1]);
      var subflag2 = fv[2].test(_field.value);
      if (subflag1 && subflag2) {
        _field.style.border = green;
        document.getElementById(`${_field.name}-error`).innerText = '';
        flags[i] = true;
      } else if (_field.value) {
        _field.style.border = red;
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (subflag2) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
        flags[i] = false;
      } else {
        _field.style.border = red;
        flags[i] = false;
      }
    });
  });

  const file = publish['file-name'];
  document.getElementById('file').addEventListener('change', event => {
    if (event.target.files[0]) {
      var upload = event.target.files[0];
      file.value = upload.name;
      if (upload.name.slice(-4).toLowerCase() != '.pdf') {
        file.style.border = red;
        document.getElementById('file-error').innerText = 'Invalid file type. Please upload a PDF.';
        flags[3] = false;
      } else if (upload.size > 20971520) {
        file.style.border = red;
        document.getElementById('file-error').innerText = 'File size exceeds 20MB.';
        flags[3] = false;
      } else {
        file.style.border = green;
        document.getElementById('file-error').innerText = '';
        flags[3] = true;
      }
    }
  });

  publish['agreement'].addEventListener('change', event => {
    if (event.target.checked) {
      document.getElementById('checkbox').style.border = '#fff solid 1px';
      flags[4] = true;
    } else {
      document.getElementById('checkbox').style.border = red;
      flags[4] = false;
    }
  });

  publish.addEventListener('submit', event => {
    ['name', 'email'].forEach((field, i) => {
      var _field = publish[field];
      if (!_field.value.trim().length) {
        _field.style.border = red;
        flags[i] = false;
      }
    });
    if (!flags[3]) {
      file.style.border = red;
    }
    if (!(publish['agreement'].checked)) {
      document.getElementById('checkbox').style.border = red;
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
  ['email', 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$/],
  ['query', 1024, /^[a-zA-Z0-9 \,\.\-\'\r\n]+$/]];
  field_val.forEach((fv, i) => {
    var _field = contact[fv[0]];
    _field.addEventListener('change', () => {
      var subflag1 = length(_field, fv[1]);
      var subflag2 = fv[2].test(_field.value)
      if (subflag1 && subflag2) {
        _field.style.border = green;
        document.getElementById(`${_field.name}-error`).innerText = '';
        flags[i] = true;
      } else if (_field.value) {
        _field.style.border = red;
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (subflag2) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
        flags[i] = false;
      } else {
        _field.style.border = red;
        flags[i] = false;
      }
    });
  });

  contact.addEventListener('submit', event => {
    field_val.forEach((fv, i) => {
      var _field = contact[fv[0]];
      if (!_field.value.trim().length) {
        _field.style.border = red;
        flags[i] = false;
      }
    });
    if (flags.includes(false)) {
      event.preventDefault();
    } else {
      document.getElementById('spinner').style.visibility = 'visible';
    }
  });
}