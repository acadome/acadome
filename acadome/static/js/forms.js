class Form {
  constructor(form_id) {
    this._form = document.getElementById(form_id);
    this._green = '#00ab66';
    this._red = '#d11a2a';
    this._flags = [false, false, false];
  }

  _length(field, m) {
    if (m.length == 1) {
      if (field.value.length > m[0]) {
        return false;
      } else {
        return true;
      }
    } else if (m.length == 2) {
      if (field.value.trim().length < m[0]
      || field.value.length > m[1]) {
        return false;
      } else {
        return true;
      }
    }
  }

  _pass(field, border) {
    if (border) {
      field.style.padding = '9px 19px';
      field.style.border = `${this._green} solid 2px`;
    } else {
      field.style.padding = '10px 20px';
      field.style.border = `#ccc solid 1px`;
    }
    document.getElementById(`${field.name}-error`).innerText = '';
    return true;
  }

  _fail(field) {
    field.style.padding = '9px 19px';
    field.style.border = `${this._red} solid 2px`;
    return false;
  }

  _validateTextFields(validators) {
    var flags = [];
    for (var i=0; i < validators.length; i++) {
      flags[i] = !validators[i]['required'];
    }

    validators.forEach((val, i) => {
      var field = this._form.elements[val['name']];
      if (val['default']) {
        field.value = val['default'];
        flags[i] = this._pass(field, val['border']);
      }
      field.addEventListener('change', () => {
        if (field.value.trim().length) {
          if (!this._length(field, val['length'])) {
            document.getElementById(`${field.name}-error`).innerText = `Must be between ${val['length'][0]} and ${val['length'][1]} characters.`;
            flags[i] = this._fail(field);
          } else if (!val['regex'].test(field.value)) {
            switch (field.name) {
              case 'email':
                document.getElementById('email-error').innerText = 'Invalid email address.';
                break;
              case 'password':
                document.getElementById('password-error').innerText = 'Allowed characters: a-z, A-Z, 0-9, and _.';
                break;
              default:
                document.getElementById(`${field.name}-error`).innerText = `Invalid characters in ${field.name}.`;
            }
            flags[i] = this._fail(field);
          } else {
            flags[i] = this._pass(field, val['border'])
          }
        } else {
          if (val['required']) {
            document.getElementById(`${field.name}-error`).innerText = '';
            flags[i] = this._fail(field);
          } else {
            flags[i] = this._pass(field, val['border']);
          }
        }
      });
    });

    this._form.addEventListener('submit', event => {
      validators.forEach((val, i) => {
        var field = this._form.elements[val['name']];
        if (!field.value.trim().length) {
          if (val['required']) {
            flags[i] = this._fail(field);
          } else {
            flags[i] = this._pass(field, val['border']);
          }
        } else {
          flags[i] = this._pass(field, val['border']);
        }
      });
      if (flags.includes(false)) {
        this._flags[0] = false;
      } else {
        this._flags[0] = true;
      }
    });
  }

  _validateBooleanField(field) {
    this._form.elements[field].addEventListener('change', event => {
      if (event.target.checked) {
        this._form.elements[field].style.outline = `2px solid #fff`;
        this._flags[1] = true;
      } else {
        this._form.elements[field].style.outline = `2px solid ${this._red}`;
        this._flags[1] = false;
      }
    });
    this._form.addEventListener('submit', () => {
      if (!this._flags[1]) {
        this._form.elements[field].style.outline = `2px solid ${this._red}`;
      }
    });
  }

  _validateFileField(field) {
    var fileName = this._form.elements['file-name'];
    this._form.elements[field].addEventListener('change', event => {
      if (event.target.files[0]) {
        var upload = event.target.files[0];
        fileName.value = upload.name;
        var fileError = document.getElementById('file-name-error');
        if (upload.name.slice(-4).toLowerCase() != '.pdf') {
          fileError.innerText = 'Invalid file type. Please upload a PDF.';
          this._flags[2] = this._fail(fileName);
        } else if (upload.size > 20971520) {
          fileError.innerText = 'File size exceeds 20MB.';
          this._flags[2] = this._fail(fileName);
        } else {
          this._flags[2] = this._pass(fileName, true);
        }
      }
    });
    this._form.addEventListener('submit', () => {
      if (!this._flags[2]) {
        this._fail(fileName);
      }
    });
  }

  validate(text, boolean=null, file=null) {
    this._validateTextFields(text);
    if (boolean) {
      this._validateBooleanField(boolean);
    } else {
      this._flags[1] = true;
    }
    if (file) {
      this._validateFileField(file);
    } else {
      this._flags[2] = true;
    }
    this._form.addEventListener('submit', () => {
      if (this._flags.includes(false)) {
        event.preventDefault();
      } else {
        document.querySelector('.spinner').style.visibility = 'visible';
      }
    });
  }
}

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
