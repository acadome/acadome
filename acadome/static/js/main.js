// NAV
const nav = document.querySelectorAll('nav a');
nav.forEach(li => {
  if (window.location.pathname == li.getAttribute('href')) {
    li.style.borderBottom = '#000 solid 2px';
    li.style.pointerEvents = 'none';
    li.style.cursor = 'default';
  }
});

const flash = document.getElementById('hide-flash');
if (flash) {
  flash.addEventListener('click', () => {
    document.getElementById('flash').style.display = 'none';
  });
}
