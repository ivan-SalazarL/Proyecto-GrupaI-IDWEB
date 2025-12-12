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

// --- 8. Lógica del Modal de Edición (¡Ahora sí actualiza la tabla!) ---
  
  let filaAEditar = null; // Variable para recordar qué fila estamos editando

  // Función para abrir el modal
  window.abrirModal = (nombreActual, estadoActual) => {
    const modal = document.getElementById("modalEditar");
    const inputNombre = document.getElementById("editNombre");
    const selectEstado = document.getElementById("editEstado");
    
    // Llenamos el formulario con los datos actuales
    if(inputNombre) inputNombre.value = nombreActual;
    
    // Ajustamos el select al estado correcto (minúsculas para coincidir con el value)
    if(selectEstado) selectEstado.value = estadoActual.toLowerCase(); 
    
    if(modal) modal.style.display = "flex";
  };

  window.cerrarModal = () => {
    const modal = document.getElementById("modalEditar");
    if(modal) modal.style.display = "none";
    filaAEditar = null; // Limpiamos la referencia al cerrar
  };

  // 1. Detectar Click en botones "Editar"
  const tabla = document.querySelector("table");
  if (tabla) {
    tabla.addEventListener("click", (e) => {
      // Verificamos si lo que se clickeó es un enlace o botón de "Editar"
      if (e.target.closest("a") && e.target.textContent.includes("Editar")) {
        e.preventDefault();
        
        // Guardamos la fila entera (<tr>) en la variable global
        filaAEditar = e.target.closest("tr");
        
        // Obtenemos los datos actuales de esa fila
        // cells[0] es el Nombre, cells[3] es el Estado (según tu tabla)
        const nombre = filaAEditar.cells[0].innerText; 
        const estado = filaAEditar.cells[3].innerText; 

        abrirModal(nombre, estado);
      }
    });
  }

  // 2. Guardar los cambios al enviar el formulario
  const formEditar = document.getElementById("formEditar");
  if(formEditar) {
    formEditar.addEventListener("submit", (e) => {
      e.preventDefault();

      if (filaAEditar) {
        // Obtenemos los nuevos valores del formulario
        const nuevoNombre = document.getElementById("editNombre").value;
        const nuevoEstado = document.getElementById("editEstado").value; // "activo" o "inactivo"

        // A. Actualizamos el Nombre (Columna 0)
        filaAEditar.cells[0].innerText = nuevoNombre;

        // B. Actualizamos el Estado y el color del Badge (Columna 3)
        const celdaEstado = filaAEditar.cells[3];
        
        if (nuevoEstado === "activo") {
          celdaEstado.innerHTML = '<span class="badge badge-activo">Activo</span>';
        } else {
          celdaEstado.innerHTML = '<span class="badge badge-inactivo">Inactivo</span>';
        }

        mostrarNotificacion("Proveedor actualizado correctamente", "success");
      }

      cerrarModal();
    });
  }

  // Cerrar si se hace click fuera del modal
  window.onclick = (event) => {
    const modal = document.getElementById("modalEditar");
    if (event.target == modal) {
      cerrarModal();
    }
  };