// Marca la hora actual en gráficos y tablas, y rellena el recuadro "Ahora".
(function () {
  var now = Date.now(), H = 3600000;
  document.querySelectorAll("[data-s]").forEach(function (el) {
    var s = +el.getAttribute("data-s");
    if (now >= s && now < s + H) el.classList.add("now");
  });
  var box = document.querySelector("[data-now]");
  var row = document.querySelector("tr.now[data-p]");
  if (box && row) {
    box.querySelector(".v").textContent = row.getAttribute("data-p");
    box.querySelector(".l").textContent = row.getAttribute("data-l");
    box.hidden = false;
  }
})();
