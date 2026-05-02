-- =====================================================
-- DATOS DE PRUEBA PARA EL SISTEMA DE TRIAGE
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

-- Obtener IDs de pacientes y usuarios para crear triajes
DO $$
DECLARE
    paciente_id UUID;
    usuario_id UUID;
    niveles TEXT[] := ARRAY['critico', 'alto', 'moderado', 'bajo'];
    estados TEXT[] := ARRAY['completado', 'completado', 'completado', 'completado', 'completado', 'en_proceso'];
BEGIN
    SELECT id_usuario INTO usuario_id FROM usuarios LIMIT 1;
    
    -- Triajes para HOY (2 mayo 2026)
    FOR i IN 0..4 LOOP
        SELECT id_paciente INTO paciente_id FROM pacientes ORDER BY RANDOM() LIMIT 1;
        INSERT INTO triajes (
            id_paciente, id_usuario, fecha_hora,
            presion_arterial_sistolica, presion_arterial_diastolica,
            frecuencia_cardiaca, temperatura, saturacion_oxigeno,
            sintomas_principales, sintomas_texto_libre, antecedentes_relevantes,
            nivel_urgencia, estado,
            fecha_atencion_inicio, fecha_atencion_fin, observaciones
        )
        VALUES (
            paciente_id,
            usuario_id,
            '2026-05-02'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL,
            100 + (random() * 80)::INTEGER,
            60 + (random() * 40)::INTEGER,
            60 + (random() * 60)::INTEGER,
            36.0 + (random() * 3)::DECIMAL(4,1),
            90 + (random() * 10)::INTEGER,
            ARRAY[
                'Dolor torácico',
                'Dificultad respiratoria',
                'Fiebre alta',
                'Dolor abdominal',
                'Trauma craneal',
                'Reacción alérgica',
                'Dolor de cabeza intenso',
                'Vómito persistente'
            ][floor(random() * 8 + 1)::INTEGER],
            CASE WHEN random() > 0.5 THEN 'Paciente refereido de consulta externa' ELSE NULL END,
            CASE WHEN random() > 0.7 THEN 'Antecedentes de hipertensión' ELSE NULL END,
            niveles[1 + floor(random() * 4)::INTEGER],
            'completado',
            '2026-05-02'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL,
            '2026-05-02'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL + interval '45 minutes',
            CASE 
                WHEN random() > 0.8 THEN 'Requiere observación'
                WHEN random() > 0.5 THEN 'Estable'
                ELSE 'Derivado a consulta especializada'
            END
        );
    END LOOP;
    
    -- Triajes para MAÑANA (3 mayo 2026)
    FOR i IN 0..4 LOOP
        SELECT id_paciente INTO paciente_id FROM pacientes ORDER BY RANDOM() LIMIT 1;
        INSERT INTO triajes (
            id_paciente, id_usuario, fecha_hora,
            presion_arterial_sistolica, presion_arterial_diastolica,
            frecuencia_cardiaca, temperatura, saturacion_oxigeno,
            sintomas_principales, sintomas_texto_libre, antecedentes_relevantes,
            nivel_urgencia, estado,
            fecha_atencion_inicio, fecha_atencion_fin, observaciones
        )
        VALUES (
            paciente_id,
            usuario_id,
            '2026-05-03'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL,
            100 + (random() * 80)::INTEGER,
            60 + (random() * 40)::INTEGER,
            60 + (random() * 60)::INTEGER,
            36.0 + (random() * 3)::DECIMAL(4,1),
            90 + (random() * 10)::INTEGER,
            ARRAY[
                'Dolor torácico',
                'Dificultad respiratoria',
                'Fiebre alta',
                'Dolor abdominal',
                'Trauma craneal',
                'Reacción alérgica',
                'Dolor de cabeza intenso',
                'Vómito persistente'
            ][floor(random() * 8 + 1)::INTEGER],
            CASE WHEN random() > 0.5 THEN 'Paciente refereido de consulta externa' ELSE NULL END,
            CASE WHEN random() > 0.7 THEN 'Antecedentes de hipertensión' ELSE NULL END,
            niveles[1 + floor(random() * 4)::INTEGER],
            'completado',
            '2026-05-03'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL,
            '2026-05-03'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL + interval '45 minutes',
            CASE 
                WHEN random() > 0.8 THEN 'Requiere observación'
                WHEN random() > 0.5 THEN 'Estable'
                ELSE 'Derivado a consulta especializada'
            END
        );
    END LOOP;
    
    -- Triajes para PASADO MAÑANA (4 mayo 2026)
    FOR i IN 0..4 LOOP
        SELECT id_paciente INTO paciente_id FROM pacientes ORDER BY RANDOM() LIMIT 1;
        INSERT INTO triajes (
            id_paciente, id_usuario, fecha_hora,
            presion_arterial_sistolica, presion_arterial_diastolica,
            frecuencia_cardiaca, temperatura, saturacion_oxigeno,
            sintomas_principales, sintomas_texto_libre, antecedentes_relevantes,
            nivel_urgencia, estado,
            fecha_atencion_inicio, fecha_atencion_fin, observaciones
        )
        VALUES (
            paciente_id,
            usuario_id,
            '2026-05-04'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL,
            100 + (random() * 80)::INTEGER,
            60 + (random() * 40)::INTEGER,
            60 + (random() * 60)::INTEGER,
            36.0 + (random() * 3)::DECIMAL(4,1),
            90 + (random() * 10)::INTEGER,
            ARRAY[
                'Dolor torácico',
                'Dificultad respiratoria',
                'Fiebre alta',
                'Dolor abdominal',
                'Trauma craneal',
                'Reacción alérgica',
                'Dolor de cabeza intenso',
                'Vómito persistente'
            ][floor(random() * 8 + 1)::INTEGER],
            CASE WHEN random() > 0.5 THEN 'Paciente refereido de consulta externa' ELSE NULL END,
            CASE WHEN random() > 0.7 THEN 'Antecedentes de hipertensión' ELSE NULL END,
            niveles[1 + floor(random() * 4)::INTEGER],
            'completado',
            '2026-05-04'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL,
            '2026-05-04'::TIMESTAMP + (i * 3 || ' hours')::INTERVAL + interval '45 minutes',
            CASE 
                WHEN random() > 0.8 THEN 'Requiere observación'
                WHEN random() > 0.5 THEN 'Estable'
                ELSE 'Derivado a consulta especializada'
            END
        );
    END LOOP;
END $$;

-- Insertar algunos resultados de IA
INSERT INTO resultados_ia (id_triaje, nivel_urgencia_sugerido, confiabilidad, posibles_diagnosticos, recomendaciones, modelo_ia)
SELECT 
    t.id_triaje,
    t.nivel_urgencia,
    75 + (random() * 25)::DECIMAL(5,2),
    CASE t.nivel_urgencia
        WHEN 'critico' THEN 'Posible síndrome coronario agudo, requiere evaluación inmediata'
        WHEN 'alto' THEN 'Infección respiratoria aguda, posible neumonía'
        WHEN 'moderado' THEN 'Gastroenteritis aguda, deshidratación leve'
        WHEN 'bajo' THEN 'Ansiedad, crisis de pánico'
    END,
    CASE t.nivel_urgencia
        WHEN 'critico' THEN ' ECG, enzimas cardíacas, sala de procedimientos'
        WHEN 'alto' THEN 'Radiografía de tórax, análisis de sangre'
        WHEN 'moderado' THEN 'Hidratación IV, dieta blanda'
        WHEN 'bajo' THEN 'Soporte emocional, seguimiento ambulatorio'
    END,
    'triage-ia-v1.0'
FROM triajes t
WHERE random() > 0.3;

-- Mostrar resumen
SELECT 'Pacientes registrados: ' || COUNT(*) FROM pacientes;
SELECT 'Triajes registrados: ' || COUNT(*) FROM triajes;
SELECT 'Resultados IA: ' || COUNT(*) FROM resultados_ia;
