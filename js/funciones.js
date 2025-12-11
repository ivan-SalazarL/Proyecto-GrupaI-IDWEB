document.addEventListener("DOMContentLoaded", () => {
  
  // 1. Lógica del Menú Activo Automático
  // Detecta el archivo actual (ej: proveedores.html) o asume index.html si es la raíz
  const rutaActual = window.location.pathname.split("/").pop() || "index.html";
  const enlaces = document.querySelectorAll("nav a");

  enlaces.forEach(enlace => {
    const href = enlace.getAttribute("href");
    // Si el enlace coincide con la ruta, le ponemos la clase activo
    if (href === rutaActual) {
      enlace.classList.add("activo");
    } else {
      enlace.classList.remove("activo");
    }
  });

  // 2. Manejo de Formulario de Contacto (Simulación)
  const formularioSoporte = document.querySelector("form[action='enviar_soporte.php']");
  if (formularioSoporte) {
    formularioSoporte.addEventListener("submit", e => {
      // Como no hay backend PHP real en este entorno, prevenimos el envío real
      // Si tuvieras PHP, quitarías el e.preventDefault()
      e.preventDefault();
      alert("Tu mensaje ha sido enviado correctamente. ¡Gracias por contactarnos!");
      formularioSoporte.reset();
    });
  }

  // 3. Manejo del Buscador (Simulación)
  const formBuscador = document.querySelector(".accion-buscar form");
  if (formBuscador) {
    formBuscador.addEventListener("submit", e => {
      e.preventDefault();
      const input = formBuscador.querySelector("input");
      const consulta = input ? input.value.trim() : "";
      
      if (consulta) {
        alert(`Simulando búsqueda para: ${consulta}`);
      } else {
        alert("Por favor ingresa un nombre o categoría para buscar.");
      }
    });
  }

  // NOTA: Se eliminaron los eventos mouseenter/mouseleave porque
  // ahora las animaciones se manejan eficientemente desde CSS.
});