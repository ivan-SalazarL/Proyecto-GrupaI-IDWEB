document.addEventListener("DOMContentLoaded", () => {
  
  // --- 1. Lógica del Menú Activo ---
  const rutaActual = window.location.pathname.split("/").pop() || "index.html";
  const enlaces = document.querySelectorAll("nav a");
  enlaces.forEach(enlace => {
    if (enlace.getAttribute("href") === rutaActual) enlace.classList.add("activo");
    else enlace.classList.remove("activo");
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
        mostrarNotificacion("Modo oscuro activado", "success");
      } else {
        localStorage.setItem("tema", "claro");
        btnTema.textContent = "🌙";
        mostrarNotificacion("Modo claro activado");
      }
    });
  }

  // --- 3. Sistema de Notificaciones (Toast) ---
  // Crea el contenedor si no existe
  if (!document.getElementById("toast-container")) {
    const container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }

  window.mostrarNotificacion = (mensaje, tipo = "info") => {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${tipo}`;
    toast.innerHTML = `<span>${mensaje}</span>`;
    
    container.appendChild(toast);

    // Eliminar del DOM después de 3 segundos
    setTimeout(() => {
      toast.remove();
    }, 3000);
  };

  // --- 4. Reemplazo de Alerts en Formularios ---
  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    form.addEventListener("submit", (e) => {
      // Si no es login (que redirige), prevenimos y mostramos toast
      if (form.getAttribute("action").includes(".php") || form.getAttribute("action") === "#") {
        e.preventDefault();
        const input = form.querySelector("input");
        if(input && input.value.trim() !== "") {
          mostrarNotificacion("¡Acción realizada con éxito!", "success");
          form.reset();
        } else {
          mostrarNotificacion("Por favor completa los campos", "error");
        }
      }
    });
  });

  // --- 5. Buscador de Tabla (Si existe) ---
  const inputBuscador = document.getElementById("buscadorProveedores");
  const tablaProveedores = document.querySelector("table tbody");

  if (inputBuscador && tablaProveedores) {
    inputBuscador.addEventListener("keyup", (e) => {
      const texto = e.target.value.toLowerCase();
      const filas = tablaProveedores.querySelectorAll("tr");
      filas.forEach(fila => {
        const contenido = fila.innerText.toLowerCase();
        fila.style.display = contenido.includes(texto) ? "" : "none";
      });
    });
  }
});