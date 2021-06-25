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

// ARTICLES
function paginate(objects, per_page) {
  objects.forEach(object => object.style.display = 'none');
  const max = Math.ceil(objects.length/per_page);
  if (/^page[0-9]+$/.test(window.location.hash.slice(1))) {
    var page = parseInt(window.location.hash.split('page')[1]);
  } else {
    var page = max + 1;
  }
  if (page > max) {
    window.location.hash = 'page1';
    page = 1;
  }
  var objects_ = Array.from(objects).slice(per_page*(page-1), per_page*page);
  objects_.forEach(object => object.style.display = 'block');
  scrollTo(0, 0);

  const ul = document.getElementById('pagin');
  const li = ul.querySelectorAll('li');
  var a = li[0].querySelector('a');
  if (page-1 >= 1) {
    a.href = `#page${page-1}`;
    a.innerText = page-1;
    a.style.display = 'block';
  } else {
    a.style.display = 'none';
  }
  li[1].innerText = page;
  var a = li[2].querySelector('a');
  if (page+1 <= max) {
    a.href = `#page${page+1}`;
    a.innerText = page+1;
    a.style.display = 'block';
  } else {
    a.style.display = 'none';
  }
  ul.style.display = 'grid';
}

var articles = document.querySelectorAll(`.article`);
const per_page = 10;
if (!articles.length && document.getElementById('no-results')) {
  document.getElementById('no-results').style.display = 'block';
} else if (articles.length > per_page) {
  if (window.location.hash.slice(1)) {
    paginate(articles, per_page);
  } else {
    window.location.hash = 'page1';
  }
  window.addEventListener('hashchange', () => paginate(articles, per_page));
} else {
  articles.forEach(article => article.style.display = 'block');
}
