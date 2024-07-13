document.addEventListener('DOMContentLoaded', function () {
  function moreDocumentation() {
    var small = document.getElementById('PrototypeSmall');
    var big = document.getElementById('PrototypeBig');
    small.style.display = 'none';
    big.style.display = 'block';
  }

  function lessDocumentation() {
    var small = document.getElementById('PrototypeSmall');
    var big = document.getElementById('PrototypeBig');
    small.style.display = 'block';
    big.style.display = 'none';
  }

  // Attach event listeners for more/less functionality
  const moreLinks = document.querySelectorAll('a[onclick="moreDocumentation()"]');
  moreLinks.forEach(link => link.addEventListener('click', function (event) {
    event.preventDefault();
    moreDocumentation();
  }));

  const lessLinks = document.querySelectorAll('a[onclick="lessDocumentation()"]');
  lessLinks.forEach(link => link.addEventListener('click', function (event) {
    event.preventDefault();
    lessDocumentation();
  }));
});
