// SEARCH
const search = document.forms['search-form'];
if (search) {
  search.addEventListener('submit', event => {
    _search = search['search'];
    if (_search.value.length > 128 || !_search.value.trim().length) {
      event.preventDefault();
    }
  });
}

// FIELDS AND SUBFIELDS OF RESEARCH
const fields = document.querySelectorAll('.box');
if (fields) {
  fields.forEach(field => {
    field.addEventListener('click', event => window.location.href = event.currentTarget.querySelector('a').href);
  });
}
