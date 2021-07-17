switch (window.location.pathname.split('/')[2]) {
  case '':
    var form = document.getElementById('field-form');
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
    break;

  case 'edit_article':
    const title = new Validators(
      'title', [256], /[\s\S]+/
    )

    const authors = new Validators(
      'authors', [256], /^[a-zA-Z \-\'\,]+$/
    )

    const abstract = new Validators(
      'abstract', [1024], /[\s\S]+/
    )

    const keywords = new Validators(
      'keywords', [5, 256], /[\s\S]+/
    )

    const reviewers = new Validators(
      'reviewers', [256], /[\s\S]*/, false
    )

    var form = new Form('edit-article-form');
    const id = window.location.pathname.split('/')[3];
    fetch(`/admin/article_json/${id}`)
      .then(response => response.json())
      .then(article => {
        title.default = article['title'];
        authors.default = article['authors'].join(', ');
        abstract.default = article['abstract'];
        keywords.default = article['keywords'].join(', ');
        form.form.elements['field'].value = article['field'];
        reviewers.default = article['reviewers'];
        form.validate(
          text=[title, authors, abstract, keywords, reviewers]
        );
      })
      .catch(error => console.log(error));
    break;
}
