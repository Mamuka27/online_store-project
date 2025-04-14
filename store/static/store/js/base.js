setTimeout(function () {
    const alerts = document.querySelectorAll('.fade-message');
    alerts.forEach(function (alert) {
      $(alert).alert('close');
    });
  }, 3000);
  


  document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("dark-mode-toggle");
    const isDark = localStorage.getItem("darkMode") === "true";
  
    if (isDark) {
      document.body.classList.add("dark-mode");
      if (toggle) toggle.checked = true;
    }
  
    if (toggle) {
      toggle.addEventListener("change", function () {
        if (this.checked) {
          document.body.classList.add("dark-mode");
          localStorage.setItem("darkMode", "true");
        } else {
          document.body.classList.remove("dark-mode");
          localStorage.setItem("darkMode", "false");
        }
      });
    }
  });
  