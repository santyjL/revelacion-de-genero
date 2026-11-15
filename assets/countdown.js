(function initGenderRevealCountdown() {
  function pad(value) {
    return String(value).padStart(2, "0");
  }

  function setHidden(node, hidden) {
    if (!node) {
      return;
    }
    node.style.display = hidden ? "none" : "";
    node.hidden = hidden;
  }

  function tick() {
    var root = document.getElementById("event-countdown");
    if (!root) {
      return;
    }
    var deadline = Number(root.getAttribute("data-deadline-ms"));
    var live = root.querySelector("[data-countdown-live]");
    var done = root.querySelector("[data-countdown-done]");
    if (!deadline) {
      return;
    }
    var diff = deadline - Date.now();
    if (diff <= 0) {
      setHidden(live, true);
      setHidden(done, false);
      return;
    }
    setHidden(live, false);
    setHidden(done, true);
    var total = Math.floor(diff / 1000);
    var days = Math.floor(total / 86400);
    var hours = Math.floor((total % 86400) / 3600);
    var minutes = Math.floor((total % 3600) / 60);
    var seconds = total % 60;
    var units = { days: String(days), hours: pad(hours), minutes: pad(minutes), seconds: pad(seconds) };
    Object.keys(units).forEach(function (key) {
      var el = root.querySelector('[data-unit="' + key + '"]');
      if (el) {
        el.textContent = units[key];
      }
    });
  }

  tick();
  window.setInterval(tick, 1000);
})();
