if (window.location.pathname.split('/')[2] == 'edit_article') {
  var title = new Validators(
    'title', [256], /[\s\S]+/
  )

  var authors = new Validators(
    'authors', [256], /^[a-zA-Z \-\'\,]+$/
  )

  var abstract = new Validators(
    'abstract', [1024], /[\s\S]+/
  )

  var keywords = new Validators(
    'keywords', [5, 256], /[\s\S]+/
  )

  var reviewers = new Validators(
    'reviewers', [256], /[\s\S]*/, false
  )

  var form = new Form('edit-article-form');
  var id = window.location.pathname.split('/')[3];
  fetch(`/admin/article_json/${id}`)
    .then(response => response.json())
    .then(article => {
      title.default = article['title'];
      authors.default = article['authors'].join(', ');
      abstract.default = article['abstract'];
      keywords.default = article['keywords'].join(', ');
      reviewers.default = article['reviewers'];
      form._form.elements['field'].value = article['field'];
      form.validate(
        text=[title, authors, abstract, keywords, reviewers]
      );
    })
    .catch(error => console.log(error))
}
