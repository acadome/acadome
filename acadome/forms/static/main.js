class TextVal {
  constructor(
    name, required=true, length=[0, 256], regex=/^[\s\S]*$/,
    border=true, placeholder='', preset='', dbVal=''
  ) {
    this.name = name;
    this.required = required;
    this.length = length;
    this.regex = regex;
    this.border = border;
    this.placeholder = placeholder;
    this.preset = preset;
    this.dbVal = dbVal;
  }
}

class FileVal {
  constructor(
    name, formats, size=2
  ) {
    this.name = name;
    this.formats = formats;
    this.size = size;
  }
}

class ValidateForm {
  constructor(id) {
    this.form = document.getElementById(id);
    this._action = this.form.getAttribute('action');
    this._flags = {};
    this._green = '#00ab66';
    this._red = '#d11a2a';
    this._password = null;
    this._booleans = [];
  }

  _pass(field, border) {
    if (border) {
      field.style.padding = '9px 19px';
      field.style.border = `${this._green} solid 2px`;
    } else {
      field.style.padding = '10px 20px';
      field.style.border = `#ccc solid 1px`;
    }
  }

  _fail(field) {
    field.style.padding = '9px 19px';
    field.style.border = `${this._red} solid 2px`;
  }

  _initText(obj) {
    const field = this.form.elements[obj.name];
    var flag = !obj.required;
    this._flags[obj.name] = flag;
    field.placeholder = obj.placeholder;
    if (obj.preset && !field.value) {
      field.value = obj.preset;
      this._flags[obj.name] = true;
      this._pass(field, obj.border);
    }
    return [field, flag]
  }

  _postJSON(endpoint, data) {
    return fetch(endpoint, {
      method: 'POST',
      cache: 'no-cache',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(response => response.text());
  }

  validateText(obj) {
    var [field, flag] = this._initText(obj);
    field.addEventListener('change', () => {
      const error = document.getElementById(`${obj.name}-error`);
      if (obj.name != 'password') field.value = field.value.trim();
      if (field.value.length) {
        if (field.value.length >= obj.length[0] && field.value.length <= obj.length[1]) {
          flag = obj.regex.test(field.value);
          switch (obj.name) {
            case 'email':
              var msg = 'Invalid email address.'
              break;
            case 'password':
              var msg = 'Allowed characters: ';
              break;
            default:
              var msg = `Invalid characters in ${obj.name}.`
          }
          error.innerText = flag ? '' : msg;
        } else {
          flag = false;
          error.innerText = obj.length[0] ? `Must be between ${obj.length[0]} and ${obj.length[1]} characters.` : `Cannot exceed ${obj.length[1]} characters.`;
        }
      } else {
        flag = !obj.required;
        error.innerText = '';
      }
      flag ? this._pass(field, obj.border) : this._fail(field);
      this._flags[obj.name] = flag;
    });
    this.form.addEventListener('submit', () => {
      this._flags[obj.name] ? this._pass(field, obj.border) : this._fail(field);
    });
  }

  validateEmail(obj) {
    if (!obj.dbVal) return this.validateText(obj);
    var [field, flag] = this._initText(obj);
    field.addEventListener('change', () => {
      field.value = field.value.trim()
      const error = document.getElementById(`${obj.name}-error`);
      this._postJSON(`/form/${obj.dbVal}_email`, {'email': field.value})
        .then(data => {
          if (field.value.length) {
            if (obj.regex.test(field.value)) {
              flag = !data;
              error.innerText = data;
            } else {
              flag = false;
              error.innerText = 'Invalid email address.';
            }
          } else {
            flag = !obj.required;
            error.innerText = '';
          }
          flag ? this._pass(field, obj.border) : this._fail(field);
          this._flags[obj.name] = flag;
        })
        .catch(error => console.log(error));
    });
    this.form.addEventListener('submit', () => {
      this._flags[obj.name] ? this._pass(field, obj.border) : this._fail(field);
    });
  }

  validatePassword(obj) {
    this.validateText(obj);
    if (obj.dbVal) this._password = obj;
  }

  validateSelect(name, preset) {
    const field = this.form.elements[name];
    this._flags[name] = true;
    if (preset) field.value = preset;
    this._pass(field, true);
  }

  validateFile(obj) {
    const field = this.form.elements[obj.name];
    this._flags[obj.name] = false;
    const filename = this.form.elements[`${obj.name}-name`];
    field.addEventListener('change', event => {
      var subflags = new Array(event.target.files.length);
      filename.value = '';
      Array.from(event.target.files).forEach((upload, i) => {
        filename.value += i < event.target.files.length-1 ? `${upload.name}; ` : upload.name;
        const error = document.getElementById(`${obj.name}-error`);
        if (obj.formats.includes(upload.name.slice(-4).toLowerCase())) {
          if (upload.size < obj.size*1024*1024) {
            subflags[i] = true;
            error.innerText = '';
          } else {
            subflags[i] = false;
            error.innerText = `File size exceeds ${obj.size}MB limit.`;
          }
        } else {
          subflags[i] = false;
          error.innerText = 'Invalid file type.';
        }
      });
      var flag = !subflags.includes(false);
      flag ? this._pass(filename, true) : this._fail(filename);
      this._flags[obj.name] = flag;
    });
    this.form.addEventListener('submit', () => {
      if (!this._flags[obj.name]) this._fail(filename);
    });
  }

  validateBoolean(name, preset=false) {
    const field = this.form.elements[name];
    this._booleans.push(name)
    this._flags[name] = preset;
    field.checked = preset;
    field.addEventListener('change', () => {
      if (field.checked) {
        field.style.outline = `2px solid #fff`;
        this._flags[name] = true;
      } else {
        field.style.outline = `2px solid ${this._red}`;
        this._flags[name] = false;
      }
    });
    this.form.addEventListener('submit', () => {
      if (!this._flags[name]) field.style.outline = `2px solid ${this._red}`;
    });
  }

  _postForm(action, formdata) {
    fetch(action, {
      method: 'POST',
      body: formdata
    })
      .then(response => response.text())
      .then(endpoint => window.location.pathname = endpoint)
      .catch(error => console.log(error))
    document.querySelector('.spinner').style.visibility = 'visible';
  }

  submit() {
    this.form.addEventListener('submit', event => {
      event.preventDefault()
      if (Object.keys(this._flags).find(f => !this._flags[f])) return;
      const formdata = new FormData(this.form);
      formdata.set('js', true);
      if (this._password) {
        const field = this.form.elements[this._password.name];
        this._postJSON(`/form/${this._password.dbVal}_password`, {
          'email': this.form.elements['email'].value,
          'password': field.value
        })
          .then(data => {
            var flag = !data;
            document.getElementById(`${this._password.name}-error`).innerText = data;
            flag ? this._pass(field, this._password.border) : this._fail(field);
            this._flags[this._password.name] = flag;
            if (flag) this._postForm(this._action, formdata);
          })
          .catch(error => console.log(error));
      } else {
        this._postForm(this._action, formdata);
      }
    });
  }
}
