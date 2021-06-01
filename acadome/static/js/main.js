// NAV
const nav = document.querySelectorAll('nav a');
nav.forEach(li => {
  if (window.location.href == li.href) {
    li.style.borderBottom = '#000 solid 2px';
    li.style.pointerEvents = 'none';
    li.style.cursor = 'default';
  }
});
