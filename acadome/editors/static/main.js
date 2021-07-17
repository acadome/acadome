const form = document.getElementById('field-form');
form.addEventListener('submit', event => event.preventDefault());
const select = form.elements['field'];
select.addEventListener('change', () => {
  document.querySelectorAll('.article').forEach(article => {
    if (article.className.includes(select.value)) {
      article.style.display = 'block';
    } else {
      article.style.display = 'none';
    }
    if (document.querySelectorAll(`.${select.value}`).length) {
      document.querySelector('.no-results').classList.add('hidden');
    } else {
      document.querySelector('.no-results').classList.remove('hidden');
    }
  });
});
