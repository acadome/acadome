document.querySelector('main').classList.remove('hidden');
if (!window.location.pathname.slice(1)) {
  document.getElementById('search').focus();
}

// NAV
const nav = document.querySelectorAll('nav a');
nav.forEach(li => {
  if (window.location.pathname == li.getAttribute('href')) {
    li.style.borderBottom = '#000 solid 2px';
    li.style.pointerEvents = 'none';
    li.style.cursor = 'default';
  }
});

// FLASH
const flash = document.getElementById('hide-flash');
if (flash) {
  flash.addEventListener('click', () => {
    document.getElementById('flash').classList.add('hidden');
  });
}
