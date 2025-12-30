document.addEventListener("DOMContentLoaded", () => {
  
  // --- 1. Lógica del Menú Activo (Resaltar página actual) ---
  const rutaActual = window.location.pathname.split("/").pop();
  const enlaces = document.querySelectorAll("nav a");
  
  enlaces.forEach(enlace => {
    const href = enlace.getAttribute("href");
    // Si el href coincide con la ruta actual, añadir clase activo
    if (href && href.includes(rutaActual) && rutaActual !== "") {
      enlace.classList.add("activo");
    }
  });

  // --- 2. Modo Oscuro (Persistente) ---
  const btnTema = document.getElementById("btnTema");
  const body = document.body;
  
  // Revisar preferencia guardada
  if (localStorage.getItem("tema") === "oscuro") {
    body.classList.add("dark-mode");
    if(btnTema) btnTema.textContent = "☀️";
  }

  if (btnTema) {
    btnTema.addEventListener("click", () => {
      body.classList.toggle("dark-mode");
      
      // Guardar preferencia y cambiar icono
      if (body.classList.contains("dark-mode")) {
        localStorage.setItem("tema", "oscuro");
        btnTema.textContent = "☀️";
      } else {
        localStorage.setItem("tema", "claro");
        btnTema.textContent = "🌙";
      }
    });
  }

  // --- 3. Auto-ocultar Mensajes Flash (Toast) ---
  // Si aparecen mensajes de confirmación (verdes/rojos), borrarlos a los 4 seg
  const flashMessages = document.getElementById("flash-messages");
  if (flashMessages) {
    setTimeout(() => {
      flashMessages.style.opacity = '0';
      setTimeout(() => flashMessages.remove(), 500); // Quitar del DOM
    }, 4000);
  }

  // --- 4. Buscador Simple en Tabla (Opcional) ---
  const inputBuscador = document.getElementById("buscadorProveedores");
  const tablaBody = document.querySelector("table tbody");

  if (inputBuscador && tablaBody) {
    inputBuscador.addEventListener("keyup", (e) => {
      const texto = e.target.value.toLowerCase();
      const filas = tablaBody.querySelectorAll("tr");
      
      filas.forEach(fila => {
        const contenido = fila.innerText.toLowerCase();
        fila.style.display = contenido.includes(texto) ? "" : "none";
      });
    });
  }
});