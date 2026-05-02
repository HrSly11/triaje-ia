-- =====================================================
-- DATOS DE PRUEBA SIMPLES PARA EL SISTEMA DE TRIAGE
-- =====================================================

-- Insertar pacientes de prueba
INSERT INTO pacientes (numero_documento, tipo_documento, nombre_completo, fecha_nacimiento, genero, telefono, correo, direccion)
VALUES 
    ('1001234567', 'CC', 'María Fernanda López Gómez', '1985-03-15', 'Femenino', '3001234567', 'maria.lopez@email.com', 'Calle 45 #23-10, Bogotá'),
    ('1002345678', 'CC', 'Carlos Andrés Martínez Ruiz', '1972-08-22', 'Masculino', '3002345678', 'carlos.martinez@email.com', 'Carrera 7 #56-30, Bogotá'),
    ('1003456789', 'CC', 'Ana Sofía Pérez Torres', '2015-11-08', 'Femenino', '3003456789', 'ana.perez@email.com', 'Calle 100 #15-20, Bogotá'),
    ('1004567890', 'CC', 'José Guillermo Silva Díaz', '1990-05-30', 'Masculino', '3004567890', 'jose.silva@email.com', 'Carrera 30 #65-45, Bogotá'),
    ('1005678901', 'CC', 'Laura Valentina Ramírez Castro', '2008-02-14', 'Femenino', '3005678901', 'laura.ramirez@email.com', 'Calle 80 #12-30, Bogotá'),
    ('1006789012', 'CC', 'Miguel Ángel González Herrera', '1965-12-25', 'Masculino', '3006789012', 'miguel.gonzalez@email.com', 'Carrera 15 #78-90, Bogotá'),
    ('1007890123', 'CC', 'Sandra Milena Rojas Vargas', '1995-07-18', 'Femenino', '3007890123', 'sandra.rojas@email.com', 'Calle 34 #67-12, Bogotá'),
    ('1008901234', 'CC', 'Pedro Pablo Jiménez Morales', '1950-04-02', 'Masculino', '3008901234', 'pedro.jimenez@email.com', 'Carrera 68 #23-45, Bogotá'),
    ('1009012345', 'CC', 'Diana Carolina Sánchez Lima', '1988-09-28', 'Femenino', '3009012345', 'diana.sanchez@email.com', 'Calle 12 #45-78, Bogotá'),
    ('1010123456', 'CC', 'Roberto Carlos Díaz Vargas', '1978-01-10', 'Masculino', '3010123456', 'roberto.diaz@email.com', 'Carrera 90 #34-56, Bogotá')
ON CONFLICT (numero_documento) DO NOTHING;

-- Obtener IDs para insertar triajes
DO $$
DECLARE
    p1 UUID;
    p2 UUID;
    p3 UUID;
    p4 UUID;
    p5 UUID;
    u1 UUID;
BEGIN
    SELECT id_paciente INTO p1 FROM pacientes WHERE numero_documento = '1001234567';
    SELECT id_paciente INTO p2 FROM pacientes WHERE numero_documento = '1002345678';
    SELECT id_paciente INTO p3 FROM pacientes WHERE numero_documento = '1003456789';
    SELECT id_paciente INTO p4 FROM pacientes WHERE numero_documento = '1004567890';
    SELECT id_paciente INTO p5 FROM pacientes WHERE numero_documento = '1005678901';
    SELECT id_usuario INTO u1 FROM usuarios WHERE nombre_usuario = 'admin';
    
    -- Triajes para HOY (2 mayo 2026)
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p1, u1, '2026-05-02 08:00:00', 'critico', 'completado', 150, 95, 110, 38.5, 88, 'Dolor torácico agudo', '2026-05-02 08:00:00', '2026-05-02 08:45:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p2, u1, '2026-05-02 10:00:00', 'alto', 'completado', 140, 90, 95, 37.8, 92, 'Dificultad respiratoria', '2026-05-02 10:00:00', '2026-05-02 10:40:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p3, u1, '2026-05-02 12:00:00', 'moderado', 'completado', 125, 80, 78, 37.2, 96, 'Fiebre alta', '2026-05-02 12:00:00', '2026-05-02 12:30:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p4, u1, '2026-05-02 14:00:00', 'bajo', 'completado', 115, 75, 72, 36.8, 98, 'Dolor de cabeza leve', '2026-05-02 14:00:00', '2026-05-02 14:20:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p5, u1, '2026-05-02 16:00:00', 'alto', 'completado', 145, 92, 100, 38.0, 91, 'Trauma craneal', '2026-05-02 16:00:00', '2026-05-02 16:50:00');
    
    -- Triajes para MAÑANA (3 mayo 2026)
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p1, u1, '2026-05-03 08:00:00', 'moderado', 'completado', 120, 78, 75, 37.5, 95, 'Dolor abdominal', '2026-05-03 08:00:00', '2026-05-03 08:35:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p2, u1, '2026-05-03 10:00:00', 'critico', 'completado', 160, 100, 120, 39.0, 85, 'Reacción alérgica severa', '2026-05-03 10:00:00', '2026-05-03 10:55:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p3, u1, '2026-05-03 12:00:00', 'bajo', 'completado', 110, 70, 68, 36.5, 99, 'Vómito leve', '2026-05-03 12:00:00', '2026-05-03 12:15:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p4, u1, '2026-05-03 14:00:00', 'alto', 'completado', 138, 88, 92, 37.9, 93, 'Dificultad respiratoria', '2026-05-03 14:00:00', '2026-05-03 14:45:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p5, u1, '2026-05-03 16:00:00', 'moderado', 'completado', 122, 80, 80, 37.3, 96, 'Fiebre moderada', '2026-05-03 16:00:00', '2026-05-03 16:30:00');
    
    -- Triajes para PASADO MAÑANA (4 mayo 2026)
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p1, u1, '2026-05-04 08:00:00', 'bajo', 'completado', 115, 75, 70, 36.6, 98, 'Consulta de control', '2026-05-04 08:00:00', '2026-05-04 08:15:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p2, u1, '2026-05-04 10:00:00', 'alto', 'completado', 142, 90, 98, 38.2, 90, 'Dolor torácico', '2026-05-04 10:00:00', '2026-05-04 10:50:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p3, u1, '2026-05-04 12:00:00', 'critico', 'completado', 155, 98, 115, 38.8, 86, 'Crisis hipertensiva', '2026-05-04 12:00:00', '2026-05-04 12:55:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_atencion_inicio, fecha_atencion_fin)
    VALUES (p4, u1, '2026-05-04 14:00:00', 'moderado', 'completado', 128, 82, 82, 37.4, 95, 'Dolor abdominal agudo', '2026-05-04 14:00:00', '2026-05-04 14:35:00');
    
    INSERT INTO triajes (id_paciente, id_usuario, fecha_hora, nivel_urgencia, estado, presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca, temperatura, saturacion_oxigeno, sintomas_principales, fecha_amencion_inicio, fecha_atencion_fin)
    VALUES (p5, u1, '2026-05-04 16:00:00', 'bajo', 'completado', 118, 76, 74, 36.7, 97, 'Trauma menor', '2026-05-04 16:00:00', '2026-05-04 16:20:00');
END $$;
