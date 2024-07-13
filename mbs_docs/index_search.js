document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('search-input');
  const components = document.querySelectorAll('.component');

  searchInput.addEventListener('input', function () {
    const searchTerm = searchInput.value.toLowerCase();
    components.forEach(component => {
      const matches = Array.from(component.querySelectorAll('li')).some(li => li.textContent.toLowerCase().includes(searchTerm));
      component.style.display = matches ? '' : 'none';
    });
  });
});
