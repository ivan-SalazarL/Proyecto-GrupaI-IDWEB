-- =========================================================
--  SCRIPT DE INICIALIZACIÓN
--  SISTEMA DE GESTIÓN FARMACÉUTICA
-- =========================================================

CREATE DATABASE IF NOT EXISTS SistemaFarmaceutico;
USE SistemaFarmaceutico;

-- =========================================================
--  TABLA USUARIOS
-- =========================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'usuario') DEFAULT 'usuario'
);

-- =========================================================
--  TABLA PRODUCTOS DIGEMID
-- =========================================================
CREATE TABLE productos_digemid (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_sanitario VARCHAR(100),
    nombre_producto VARCHAR(255),
    concentracion VARCHAR(255),
    forma_farmaceutica VARCHAR(255),
    titular_registro VARCHAR(255),
    stock INT DEFAULT 0  
);

-- =========================================================
--  TABLA CATEGORÍAS
-- =========================================================
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- =========================================================
--  TABLA PROVEEDORES
-- =========================================================
CREATE TABLE proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    estado ENUM('activo','inactivo') DEFAULT 'activo'
);

-- =========================================================
--  TABLA PEDIDOS
-- =========================================================
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    proveedor_id INT,
    detalle TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

-- =========================================================
--  TABLA CONTACTOS (FORMULARIO DE CONTACTO)
-- =========================================================
CREATE TABLE contactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
--  USUARIOS INICIALES
-- =========================================================
INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Administrador', 'admin@admin.com', 'admin123', 'admin'),
('Usuario', 'user@user.com', 'user123', 'usuario');

-- =========================================================
--  PROVEEDORES INICIALES
-- =========================================================
INSERT INTO proveedores (nombre, contacto, telefono, estado) VALUES
('A. MENARINI LATIN AMERICA S.L.U.', 'Contacto Comercial', '999000001', 'activo'),
('ABBVIE SAS SUCURSAL DEL PERU', 'Contacto Comercial', '999000002', 'activo'),
('ACCORD HEALTHCARE S.A.C.', 'Contacto Comercial', '999000003', 'activo'),
('AGRIPINO SARMIENTO CCOSCCO', 'Contacto Comercial', '999000004', 'activo'),
('ALCON PHARMACEUTICAL DEL PERU S.A.', 'Contacto Comercial', '999000005', 'activo'),
('ALKOFARMA E.I.R.L.', 'Contacto Comercial', '999000006', 'activo'),
('ALVID MEDIC S.A.C.', 'Contacto Comercial', '999000007', 'activo'),
('ASFARM CONSULTING S.A.C.', 'Contacto Comercial', '999000008', 'activo'),
('ASTRAZENECA PERU S.A.', 'Contacto Comercial', '999000009', 'activo'),
('AXIERTA S.A.C.', 'Contacto Comercial', '999000010', 'activo'),
('B. BRAUN MEDICAL PERU S.A.', 'Contacto Comercial', '999000011', 'activo'),
('BAYER S.A.', 'Contacto Comercial', '999000012', 'activo'),
('BIOS PERU S.A.C.', 'Contacto Comercial', '999000013', 'activo'),
('BIOSYNTEC S.A.C.', 'Contacto Comercial', '999000014', 'activo'),
('BIOTOSCANA FARMA DE PERU S.A.C.', 'Contacto Comercial', '999000015', 'activo'),
('BOEHRINGER INGELHEIM PERU S.A.C.', 'Contacto Comercial', '999000016', 'activo'),
('BONAPHARM S.A.C.', 'Contacto Comercial', '999000017', 'activo'),
('BOTICAS Y SALUD S.A.C.', 'Contacto Comercial', '999000018', 'activo'),
('BRISAFARMA S.A.C.', 'Contacto Comercial', '999000019', 'activo'),
('BRISTOL-MYERS SQUIBB PERU S.A.', 'Contacto Comercial', '999000020', 'activo'),
('CALOX PERU S.A.C.', 'Contacto Comercial', '999000021', 'activo'),
('CORPORACION BIOTEC S.A.C.', 'Contacto Comercial', '999000022', 'activo'),
('CORPORACION D OLAPHARM S.A.C.', 'Contacto Comercial', '999000023', 'activo'),
('CORPORACION SAREPTA E.I.R.L.', 'Contacto Comercial', '999000024', 'activo'),
('CORPORATION MECOFARM S.A.C.', 'Contacto Comercial', '999000025', 'activo'),
('CSP LIFESCIENCES PERU S.A.C.', 'Contacto Comercial', '999000026', 'activo'),
('DEUTSCHE PHARMA S.A.C.', 'Contacto Comercial', '999000027', 'activo'),
('DIPHASAC S.A.C.', 'Contacto Comercial', '999000028', 'activo'),
('DISTRIBUIDORA DROGUERIA LAS AMERICAS', 'Contacto Comercial', '999000029', 'activo'),
('DROGUERIA E.S.C. PHARMED CORPORATION', 'Contacto Comercial', '999000030', 'activo'),
('DROGUERIA FARMEDIC S.A.C.', 'Contacto Comercial', '999000031', 'activo'),
('DROGUERIA INVERSIONES JPS S.A.C.', 'Contacto Comercial', '999000032', 'activo'),
('DROGUERIA LABORATORIOS LANSIER', 'Contacto Comercial', '999000033', 'activo'),
('DROGUERIA PERU S.A.C. - DROPESAC', 'Contacto Comercial', '999000034', 'activo'),
('DROGUERIA SAGITARIO S.R.L.', 'Contacto Comercial', '999000035', 'activo'),
('DROGUERIA TOBAL S.A.C.', 'Contacto Comercial', '999000036', 'activo'),
('DROGUERIAS UNIDAS DEL PERU S.A.C.', 'Contacto Comercial', '999000037', 'activo'),
('ESKE CORPORATION S.A.C.', 'Contacto Comercial', '999000038', 'activo'),
('EUROFARMA PERU S.A.C.', 'Contacto Comercial', '999000039', 'activo'),
('EXELTIS PERU S.A.C.', 'Contacto Comercial', '999000040', 'activo'),
('FARMACEUTICA CONTINENTAL E.I.R.L.', 'Contacto Comercial', '999000041', 'activo'),
('FARMAKONSUMA S.A.', 'Contacto Comercial', '999000042', 'activo'),
('FARMAVAL PERU S.A.', 'Contacto Comercial', '999000043', 'activo'),
('FARMINDUSTRIA S.A.', 'Contacto Comercial', '999000044', 'activo'),
('FRESENIUS KABI PERU S.A.', 'Contacto Comercial', '999000045', 'activo'),
('GALENICUM VITAE PERU S.A.C.', 'Contacto Comercial', '999000046', 'activo'),
('GENFAR DEL PERU S.A.C.', 'Contacto Comercial', '999000047', 'activo'),
('GENOMMA LAB. PERU S.A.', 'Contacto Comercial', '999000048', 'activo'),
('GRUNENTHAL PERUANA S.A.', 'Contacto Comercial', '999000049', 'activo'),
('HERSIL S.A.C.', 'Contacto Comercial', '999000050', 'activo'),
('INRETAIL PHARMA S.A.', 'Contacto Comercial', '999000051', 'activo'),
('INSTITUTO QUIMIOTERAPICO S.A.', 'Contacto Comercial', '999000052', 'activo'),
('INTIPHARMA S.A.C.', 'Contacto Comercial', '999000053', 'activo'),
('LABORATORIOS AC FARMA S.A.', 'Contacto Comercial', '999000054', 'activo'),
('LABORATORIOS AMERICANOS S.A.', 'Contacto Comercial', '999000055', 'activo'),
('LABORATORIOS BAGO DEL PERU S.A.', 'Contacto Comercial', '999000056', 'activo'),
('LABORATORIOS ELIFARMA S.A.', 'Contacto Comercial', '999000057', 'activo'),
('LABORATORIOS FARMACEUTICOS MARKOS', 'Contacto Comercial', '999000058', 'activo'),
('LABORATORIOS INDUQUIMICA S.A.', 'Contacto Comercial', '999000059', 'activo'),
('LABORATORIOS OFTALMICOS S.A.C.', 'Contacto Comercial', '999000060', 'activo'),
('LABORATORIOS PORTUGAL S.R.L.', 'Contacto Comercial', '999000061', 'activo'),
('LABORATORIOS ROEMMERS S.A.', 'Contacto Comercial', '999000062', 'activo'),
('LABORATORIOS SIEGFRIED S.A.C.', 'Contacto Comercial', '999000063', 'activo'),
('MEDIFARMA S.A.', 'Contacto Comercial', '999000064', 'activo'),
('MEDROCK CORPORATION S.A.C.', 'Contacto Comercial', '999000065', 'activo'),
('MEGA LABS LATAM S.A.', 'Contacto Comercial', '999000066', 'activo'),
('MSN LABS PERU S.A.C.', 'Contacto Comercial', '999000067', 'activo'),
('NORDIC PHARMACEUTICAL COMPANY', 'Contacto Comercial', '999000068', 'activo'),
('NOVARTIS BIOSCIENCES PERU S.A.', 'Contacto Comercial', '999000069', 'activo'),
('OPELLA HEALTHCARE DEL PERU S.A.C.', 'Contacto Comercial', '999000070', 'activo'),
('OQCORP S.A.C.', 'Contacto Comercial', '999000071', 'activo'),
('ORGANON BIOSCIENCES PERU S.R.L.', 'Contacto Comercial', '999000072', 'activo'),
('PERUFARMA S.A.', 'Contacto Comercial', '999000073', 'activo'),
('PFIZER S.A.', 'Contacto Comercial', '999000074', 'activo'),
('PHARMAGEN S.A.C.', 'Contacto Comercial', '999000075', 'activo'),
('PROCTER & GAMBLE PERU S.R.L.', 'Contacto Comercial', '999000076', 'activo'),
('QUIMFA PERU S.A.C.', 'Contacto Comercial', '999000077', 'activo'),
('QUIMICA SUIZA S.A.C.', 'Contacto Comercial', '999000078', 'activo'),
('ROCHE FARMA (PERU) S.A.', 'Contacto Comercial', '999000079', 'activo'),
('SANDERSON S.A.', 'Contacto Comercial', '999000080', 'activo'),
('SANOFI - AVENTIS DEL PERU S.A.', 'Contacto Comercial', '999000081', 'activo'),
('SEVEN PHARMA S.A.C.', 'Contacto Comercial', '999000082', 'activo'),
('SHERFARMA S.A.C.', 'Contacto Comercial', '999000083', 'activo'),
('SUN PHARMACEUTICAL INDUSTRIES', 'Contacto Comercial', '999000084', 'activo'),
('TAKEDA S.R.L.', 'Contacto Comercial', '999000085', 'activo'),
('TECNOFARMA S.A.', 'Contacto Comercial', '999000086', 'activo'),
('TEVA PERU S.A.', 'Contacto Comercial', '999000087', 'activo'),
('UNIMED DEL PERU S.A.', 'Contacto Comercial', '999000088', 'activo'),
('VITA PHARMA S.A.C.', 'Contacto Comercial', '999000089', 'activo'),
('VITALIS PERU S.A.C.', 'Contacto Comercial', '999000090', 'activo'),
('WORLD DRUG PHARMACEUTICAL S.A.C.', 'Contacto Comercial', '999000091', 'activo');

-- =========================================================
--  (OPCIONAL) TRIGGER O SCRIPT PARA STOCK INICIAL
--  Si ya tienes productos, esto les dará stock aleatorio.
--  Si importas desde Python después, asegúrate de que tu script
--  de carga maneje o ignore esta columna.
-- =========================================================
-- UPDATE productos_digemid SET stock = FLOOR(RAND() * 100);