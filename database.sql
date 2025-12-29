CREATE DATABASE IF NOT EXISTS SistemaFarmaceutico;
USE SistemaFarmaceutico;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'usuario') DEFAULT 'usuario'
);

CREATE TABLE productos_digemid (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_sanitario VARCHAR(100),
    nombre_producto VARCHAR(255),
    concentracion VARCHAR(255),
    forma_farmaceutica VARCHAR(255),
    titular_registro VARCHAR(255)
);

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    estado ENUM('activo','inactivo') DEFAULT 'activo'
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    proveedor_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

-- Usuario administrador de prueba
INSERT INTO usuarios (nombre, email, password, rol)
VALUES ('Administrador', 'admin@admin.com', 'admin123', 'admin');

-- Usuario normal de prueba
INSERT INTO usuarios (nombre, email, password, rol)
VALUES ('Usuario', 'user@user.com', 'user123', 'usuario');
