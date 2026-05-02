-- =====================================================
-- SISTEMA DE TRIAGE CLÍNICO ASISTIDO POR IA
-- Esquema de Base de Datos PostgreSQL
-- =====================================================

-- Extensión para generar UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLA: pacientes
-- =====================================================
CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    tipo_documento VARCHAR(10) NOT NULL DEFAULT 'CC',
    nombre_completo VARCHAR(150) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(10) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    direccion VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_pacientes_documento ON pacientes(numero_documento);
CREATE INDEX idx_pacientes_nombre ON pacientes(nombre_completo);
CREATE INDEX idx_pacientes_fecha_registro ON pacientes(fecha_registro);

-- =====================================================
-- TABLA: usuarios
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'operador',
    correo VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_ultimo_acceso TIMESTAMP
);

CREATE INDEX idx_usuarios_nombre ON usuarios(nombre_usuario);

-- =====================================================
-- TABLA: triajes
-- =====================================================
CREATE TABLE IF NOT EXISTS triajes (
    id_triaje UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id_paciente),
    id_usuario UUID NOT NULL REFERENCES usuarios(id_usuario),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    presion_arterial_sistolica INTEGER,
    presion_arterial_diastolica INTEGER,
    frecuencia_cardiaca INTEGER,
    temperatura DECIMAL(4,1),
    saturacion_oxigeno INTEGER,
    sintomas_principales TEXT,
    sintomas_texto_libre TEXT,
    antecedentes_relevantes TEXT,
    nivel_urgencia VARCHAR(20),
    estado VARCHAR(20) DEFAULT 'completado',
    fecha_atencion_inicio TIMESTAMP,
    fecha_atencion_fin TIMESTAMP,
    observaciones TEXT
);

CREATE INDEX idx_triajes_paciente ON triajes(id_paciente);
CREATE INDEX idx_triajes_fecha ON triajes(fecha_hora);
CREATE INDEX idx_triajes_urgencia ON triajes(nivel_urgencia);
CREATE INDEX idx_triajes_usuario ON triajes(id_usuario);

-- =====================================================
-- TABLA: resultados_ia
-- =====================================================
CREATE TABLE IF NOT EXISTS resultados_ia (
    id_resultado UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_triaje UUID NOT NULL REFERENCES triajes(id_triaje),
    nivel_urgencia_sugerido VARCHAR(20),
    confiabilidad DECIMAL(5,2),
    posibles_diagnosticos TEXT,
    recomendaciones TEXT,
    modelo_ia VARCHAR(50),
    parametros_entrada TEXT,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resultados_triaje ON resultados_ia(id_triaje);

-- =====================================================
-- TABLA: logs_auditoria
-- =====================================================
CREATE TABLE IF NOT EXISTS logs_auditoria (
    id_log UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_usuario UUID REFERENCES usuarios(id_usuario),
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(50),
    id_registro_afectado UUID,
    detalles JSONB,
    direccion_ip VARCHAR(45),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_usuario ON logs_auditoria(id_usuario);
CREATE INDEX idx_logs_fecha ON logs_auditoria(fecha_hora);
CREATE INDEX idx_logs_accion ON logs_auditoria(accion);

-- =====================================================
-- DATOS INICIALES: usuario admin
-- =====================================================
-- Contraseña: admin123 (hash bcrypt generado correctamente)
INSERT INTO usuarios (nombre_usuario, contrasena_hash, nombre_completo, rol, correo)
VALUES (
    'admin',
    '$2b$12$NLAk2UxRZOkKGcuIeXGCoufmu6x.MqWkGBzsNwhuXFtMPNTfowtC6',
    'Administrador del Sistema',
    'administrador',
    'admin@triage-ia.local'
) ON CONFLICT (nombre_usuario) DO NOTHING;

-- Usuario operador para pruebas
INSERT INTO usuarios (nombre_usuario, contrasena_hash, nombre_completo, rol, correo)
VALUES (
    'operador',
    '$2b$12$NLAk2UxRZOkKGcuIeXGCoufmu6x.MqWkGBzsNwhuXFtMPNTfowtC6',
    'Operador de Triaje',
    'operador',
    'operador@triage-ia.local'
) ON CONFLICT (nombre_usuario) DO NOTHING;
