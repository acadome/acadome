class Form {
  constructor(form_id) {
    this.form = document.getElementById(form_id);
    this.green = '#00ab66';
    this.red = '#d11a2a';
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
      field.style.border = `${this.green} solid 2px`;
    } else {
      field.style.padding = '10px 20px';
      field.style.border = `#ccc solid 1px`;
    }
    document.getElementById(`${field.name}-error`).innerText = '';
    return true;
  }

  _fail(field) {
    field.style.padding = '9px 19px';
    field.style.border = `${this.red} solid 2px`;
    return false;
  }

  validate(validators) {
    var flags = [];
    for (var i=0; i < validators.length; i++) {
      flags[i] = !validators[i]['required'];
    }

    validators.forEach((val, i) => {
      var field = this.form.elements[val['name']];
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

    this.form.addEventListener('submit', event => {
      validators.forEach((val, i) => {
        var field = this.form.elements[val['name']];
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
        event.preventDefault();
      }
    });
  }

  checkbox(field) {
    this.form.elements[field].addEventListener('change', event => {
      if (event.target.checked) {
        this.form.elements['tc'].style.outline = `2px solid ${this.green}`;
      } else {
        this.form.elements['tc'].style.outline = `2px solid ${this.red}`;
      }
    });
    this.form.addEventListener('submit', () => {
      if (!this.form.elements['tc'].checked) {
        this.form.elements['tc'].style.outline = `2px solid ${this.red}`;
        event.preventDefault();
      }
    });
  }
}
