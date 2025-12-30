# SistemaFarmaceutico

SistemaFarmaceutico es una aplicación web empresarial desarrollada como trabajo final del curso, orientada a la gestión y administración de pedidos farmacéuticos. El proyecto integra frontend, backend y base de datos, aplicando los conocimientos adquiridos durante el curso.

## Equipo de Desarrollo
- Iván Salazar – Jefe de Proyecto / Backend
- Franklin Ulloa – Frontend / UX
- Michael Vasquez – Base de Datos

## Tecnologías Utilizadas
- Python 3
- Flask
- MySQL
- HTML5
- CSS3
- JavaScript
- Docker (Dockerfile incluido)

## Funcionalidades Implementadas
- Página principal con presentación del sistema
- Navegación entre múltiples páginas (categorías, proveedores, contacto, nosotros)
- Registro de usuarios
- Inicio de sesión
- Control de roles (usuario y administrador)
- Acceso restringido al panel de administrador
- Conexión a base de datos MySQL
- Inserción y consulta de usuarios desde la base de datos
- Interactividad en el frontend mediante JavaScript

## Estructura del Proyecto
SistemaFarmaceutico/
- app.py
- requirements.txt
- Dockerfile
- database.sql
- README.md
- templates/
  - index.html
  - login.html
  - register.html
  - categorias.html
  - proveedores.html
  - contacto.html
  - nosotros.html
- static/
  - css/
    - estilos.css
    - layout.css
  - js/
    - funciones.js

## Requisitos Previos
- Python 3 instalado
- MySQL o WampServer instalado
- Navegador web actualizado

## Base de Datos
La base de datos se crea utilizando el archivo `database.sql`, el cual contiene:
- Creación de la base de datos SistemaFarmaceutico
- Creación de tablas relacionadas
- Inserción de usuarios de prueba (administrador y usuario normal)

Para importar la base de datos:
1. Abrir phpMyAdmin
2. Seleccionar Importar
3. Cargar el archivo database.sql
4. Ejecutar el script

## Ejecución del Proyecto (sin Docker)
1. Copiar o clonar el proyecto.
2. Importar la base de datos usando database.sql.
3. Instalar las dependencias:
   pip install -r .\requeriments.txt
4. Carga Masiva de Datos (Excel/CSV)
   python importar_digemid.py
4. Ejecutar la aplicación:
   python app.py
5. Abrir el navegador en:
   http://127.0.0.1:5000

## Usuarios de Prueba
Administrador:
- Email: admin@admin.com
- Contraseña: admin123

Usuario normal:
- Email: user@user.com
- Contraseña: user123

## Docker
El proyecto incluye un Dockerfile para la contenerización de la aplicación. En equipos con virtualización habilitada, el sistema puede ejecutarse dentro de un contenedor Docker.

Durante el desarrollo, Docker Desktop no pudo ejecutarse en el entorno local debido a limitaciones de virtualización del hardware. No obstante, la aplicación fue probada exitosamente mediante ejecución local con Flask y MySQL.

## Observaciones Finales
El proyecto cumple con los requerimientos del curso al integrar frontend, backend, base de datos y control de roles, demostrando un proceso completo de desarrollo de una aplicación web empresarial.

## Bibliografía
- Documentación oficial de Flask
- Documentación oficial de MySQL
- Documentación oficial de Docker
