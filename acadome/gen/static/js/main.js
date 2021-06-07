// FORMS
function fail(e) {
  e.style.border = '#f00 solid 1px';
  e.style.boxShadow = '0 0 2px #f00';
}

function pass(e) {
  e.style.border = '#0f0 solid 1px';
  e.style.boxShadow = '0 0 2px #0f0';
}

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
        pass(_field);
        document.getElementById(`${_field.name}-error`).innerText = '';
        flags[i] = true;
      } else if (_field.value) {
        fail(_field);
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (subflag2) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
        flags[i] = false;
      } else {
        fail(_field);
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
        fail(file);
        document.getElementById('file-error').innerText = 'Invalid file type. Please upload a PDF.';
        flags[3] = false;
      } else if (upload.size > 20971520) {
        fail(file);
        document.getElementById('file-error').innerText = 'File size exceeds 20MB.';
        flags[3] = false;
      } else {
        pass(file);
        document.getElementById('file-error').innerText = '';
        flags[3] = true;
      }
    }
  });

  publish['agreement'].addEventListener('change', event => {
    if (event.target.checked) {
      document.getElementById('checkbox').style.border = '#fff solid 1px';
      document.getElementById('checkbox').style.boxShadow = 'none';
      flags[4] = true;
    } else {
      fail(document.getElementById('checkbox'));
      flags[4] = false;
    }
  });

  publish.addEventListener('submit', event => {
    ['name', 'email'].forEach((field, i) => {
      var _field = publish[field];
      if (!_field.value.trim().length) {
        fail(_field);
        flags[i] = false;
      }
    });
    if (!flags[3]) {
      fail(file);
    }
    if (!publish['agreement'].checked) {
      fail(document.getElementById('checkbox'));
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
        pass(_field);
        document.getElementById(`${_field.name}-error`).innerText = '';
        flags[i] = true;
      } else if (_field.value) {
        fail(_field);
        document.getElementById(`${_field.name}-error`).innerText = `Invalid characters in ${_field.name}.`;
        if (_field.name == 'email') {
          document.getElementById(`${_field.name}-error`).innerText = `Invalid ${_field.name}.`;
        }
        if (subflag2) {
          document.getElementById(`${_field.name}-error`).innerText = `Cannot exceed ${fv[1]} characters.`;
        }
        flags[i] = false;
      } else {
        fail(_field);
        flags[i] = false;
      }
    });
  });

  contact.addEventListener('submit', event => {
    field_val.forEach((fv, i) => {
      var _field = contact[fv[0]];
      if (!_field.value.trim().length) {
        fail(_field);
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
