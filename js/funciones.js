document.addEventListener("DOMContentLoaded", () => {
  const enlaces = document.querySelectorAll("nav a");
  const ruta = window.location.pathname.split("/").pop();

  enlaces.forEach(enlace => {
    const href = enlace.getAttribute("href");
    if (ruta === href) {
      enlace.classList.add("activo");
    } else {
      enlace.classList.remove("activo");
    }
  });

  const formulario = document.querySelector("form[action='enviar_soporte.php']");
  if (formulario) {
    formulario.addEventListener("submit", e => {
      e.preventDefault();
      alert("Tu mensaje ha sido enviado correctamente. ¡Gracias por contactarnos!");
      formulario.reset();
    });
  }

  const buscador = document.querySelector(".accion-buscar form");
  if (buscador) {
    buscador.addEventListener("submit", e => {
      e.preventDefault();
      const consulta = buscador.querySelector("input").value.trim();
      if (consulta) {
        alert(`Buscando: ${consulta}`);
      } else {
        alert("Por favor ingresa un nombre o categoría para buscar.");
      }
    });
  }

  const botones = document.querySelectorAll(".cta-button, button");
  botones.forEach(boton => {
    boton.addEventListener("mouseenter", () => boton.style.transform = "scale(1.05)");
    boton.addEventListener("mouseleave", () => boton.style.transform = "scale(1)");
  });
});
