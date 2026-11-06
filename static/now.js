// Marca la hora actual en gráficos y tablas, las franjas baratas pasadas o en curso, y rellena el recuadro "Ahora".
(function () {
  var now = Date.now(), H = 3600000;
  document.querySelectorAll("[data-s]").forEach(function (el) {
    var s = +el.getAttribute("data-s"), win = el.hasAttribute("data-e"), e = win ? +el.getAttribute("data-e") : s + H;
    if (now >= s && now < e) el.classList.add(win ? "live" : "now");
    else if (win && now >= e) el.classList.add("past");
  });
  var box = document.querySelector("[data-now]"), row = document.querySelector("tr.now[data-p]");
  if (box && row) {
    box.querySelector(".v").textContent = row.getAttribute("data-p");
    var parts = row.getAttribute("data-l").split(" · "), l = box.querySelector(".l");
    l.textContent = parts[0] + " ";
    if (parts[1]) {
      var pill = document.createElement("span");
      pill.className = "tier t" + (row.getAttribute("data-t") || "1");
      pill.textContent = parts[1];
      l.appendChild(pill);
    }
    box.hidden = false;
  }
})();
