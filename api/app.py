from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager
import os
import json
from datetime import datetime, timedelta
import hashlib
import bcrypt
import requests

app = Flask(__name__)
CORS(app)

DATABASE_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'triage_ia'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres123')
}

HCE_API_URL = os.getenv('HCE_API_URL', 'http://localhost:8001')

db_pool = ThreadedConnectionPool(1, 10, **DATABASE_CONFIG)

@contextmanager
def get_db_connection():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

@contextmanager
def get_db_cursor(cursor_type=RealDictCursor):
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=cursor_type)
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

def log_auditoria(id_usuario, accion, tabla=None, id_registro=None, detalles=None, ip=None):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO logs_auditoria (id_usuario, accion, tabla_afectada, id_registro_afectado, detalles, direccion_ip)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_usuario, accion, tabla, id_registro, json.dumps(detalles) if detalles else None, ip))
    except Exception as e:
        print(f"Error logging audit: {e}")

def verificar_contrasena(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/health', methods=['GET'])
def health_check():
    try:
        with get_db_cursor() as cursor:
            cursor.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    contrasena = data.get('contrasena')
    
    if not nombre_usuario or not contrasena:
        return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND activo = TRUE", (nombre_usuario,))
            usuario = cursor.fetchone()
        
        if not usuario:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        if not verificar_contrasena(contrasena, usuario['contrasena_hash']):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        with get_db_cursor() as cursor:
            cursor.execute("UPDATE usuarios SET fecha_ultimo_acceso = CURRENT_TIMESTAMP WHERE id_usuario = %s", (usuario['id_usuario'],))
        
        log_auditoria(usuario['id_usuario'], 'LOGIN', 'usuarios', usuario['id_usuario'])
        
        return jsonify({
            'id_usuario': str(usuario['id_usuario']),
            'nombre_usuario': usuario['nombre_usuario'],
            'nombre_completo': usuario['nombre_completo'],
            'rol': usuario['rol']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes', methods=['GET'])
def listar_pacientes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    busqueda = request.args.get('busqueda', '')
    
    offset = (page - 1) * per_page
    
    try:
        with get_db_cursor() as cursor:
            if busqueda:
                cursor.execute("""
                    SELECT * FROM pacientes 
                    WHERE activo = TRUE 
                    AND (nombre_completo ILIKE %s OR numero_documento ILIKE %s)
                    ORDER BY fecha_registro DESC
                    LIMIT %s OFFSET %s
                """, (f'%{busqueda}%', f'%{busqueda}%', per_page, offset))
            else:
                cursor.execute("""
                    SELECT * FROM pacientes 
                    WHERE activo = TRUE 
                    ORDER BY fecha_registro DESC
                    LIMIT %s OFFSET %s
                """, (per_page, offset))
            pacientes = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(*) as total FROM pacientes WHERE activo = TRUE")
            total = cursor.fetchone()['total']
        
        return jsonify({
            'pacientes': [dict(p) for p in pacientes],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes/<id_paciente>', methods=['GET'])
def obtener_paciente(id_paciente):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM pacientes WHERE id_paciente = %s", (id_paciente,))
            paciente = cursor.fetchone()
        
        if not paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        return jsonify(dict(paciente)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes', methods=['POST'])
def crear_paciente():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    
    required = ['numero_documento', 'nombre_completo', 'fecha_nacimiento', 'genero']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO pacientes (numero_documento, tipo_documento, nombre_completo, fecha_nacimiento, genero, telefono, correo, direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (
                data['numero_documento'],
                data.get('tipo_documento', 'CC'),
                data['nombre_completo'],
                data['fecha_nacimiento'],
                data['genero'],
                data.get('telefono'),
                data.get('correo'),
                data.get('direccion')
            ))
            paciente = cursor.fetchone()
        
        log_auditoria(id_usuario, 'CREAR_PACIENTE', 'pacientes', paciente['id_paciente'])
        
        return jsonify(dict(paciente)), 201
    except psycopg2.IntegrityError:
        return jsonify({'error': 'El número de documento ya existe'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/priaje', methods=['GET'])
def listar_triajes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    fechaDesde = request.args.get('fecha_desde')
    fechaHasta = request.args.get('fecha_hasta')
    nivel_urgencia = request.args.get('nivel_urgencia')
    
    offset = (page - 1) * per_page
    
    try:
        with get_db_cursor() as cursor:
            query = """
                SELECT t.*, p.nombre_completo as paciente_nombre, p.numero_documento,
                       u.nombre_completo as usuario_nombre
                FROM triajes t
                JOIN pacientes p ON t.id_paciente = p.id_paciente
                JOIN usuarios u ON t.id_usuario = u.id_usuario
                WHERE 1=1
            """
            params = []
            
            if fechaDesde:
                query += " AND t.fecha_hora >= %s"
                params.append(fechaDesde)
            if fechaHasta:
                query += " AND t.fecha_hora <= %s"
                params.append(fechaHasta)
            if nivel_urgencia:
                query += " AND t.nivel_urgencia = %s"
                params.append(nivel_urgencia)
            
            query += " ORDER BY t.fecha_hora DESC LIMIT %s OFFSET %s"
            params.extend([per_page, offset])
            
            cursor.execute(query, params)
            triajes = cursor.fetchall()
            
            count_query = "SELECT COUNT(*) as total FROM triajes t WHERE 1=1"
            count_params = []
            if fechaDesde:
                count_query += " AND t.fecha_hora >= %s"
                count_params.append(fechaDesde)
            if fechaHasta:
                count_query += " AND t.fecha_hora <= %s"
                count_params.append(fechaHasta)
            if nivel_urgencia:
                count_query += " AND t.nivel_urgencia = %s"
                count_params.append(nivel_urgencia)
            
            cursor.execute(count_query, count_params)
            total = cursor.fetchone()['total']
        
        return jsonify({
            'triajes': [dict(t) for t in triajes],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/triajes/lista', methods=['GET'])
def api_listar_triajes():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        nivel_urgencia = request.args.get('nivel_urgencia')
        
        where_clauses = []
        params = []
        
        if fecha_desde:
            where_clauses.append("DATE(t.fecha_hora) >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            where_clauses.append("DATE(t.fecha_hora) <= %s")
            params.append(fecha_hasta)
        if nivel_urgencia:
            where_clauses.append("t.nivel_urgencia = %s")
            params.append(nivel_urgencia)
        
        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)
        
        with get_db_cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) as total FROM triajes t {where_sql}", params)
            total = cursor.fetchone()['total']
        
        with get_db_cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                    t.id_triaje, t.fecha_hora, t.nivel_urgencia, t.estado,
                    t.presion_arterial_sistolica, t.presion_arterial_diastolica,
                    t.frecuencia_cardiaca, t.temperatura, t.saturacion_oxigeno,
                    t.sintomas_principales, t.observaciones,
                    p.nombre_completo as paciente_nombre, 
                    p.numero_documento as paciente_documento,
                    u.nombre_completo as usuario_nombre
                FROM triajes t
                JOIN pacientes p ON t.id_paciente = p.id_paciente
                JOIN usuarios u ON t.id_usuario = u.id_usuario
                {where_sql}
                ORDER BY t.fecha_hora DESC
                LIMIT %s OFFSET %s
            """, params + [per_page, offset])
            triajes = cursor.fetchall()
        
        return jsonify({
            'triajes': [dict(t) for t in triajes],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/triajes/<id_triaje>', methods=['GET'])
def obtener_triaje(id_triaje):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT t.*, p.nombre_completo as paciente_nombre, p.numero_documento,
                       p.fecha_nacimiento, p.genero, p.telefono,
                       u.nombre_completo as usuario_nombre
                FROM triajes t
                JOIN pacientes p ON t.id_paciente = p.id_paciente
                JOIN usuarios u ON t.id_usuario = u.id_usuario
                WHERE t.id_triaje = %s
            """, (id_triaje,))
            triaje = cursor.fetchone()
        
        if not triaje:
            return jsonify({'error': 'Triaje no encontrado'}), 404
        
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM resultados_ia WHERE id_triaje = %s", (id_triaje,))
            resultado_ia = cursor.fetchone()
        
        response = dict(triaje)
        if resultado_ia:
            response['resultado_ia'] = dict(resultado_ia)
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/triajes', methods=['POST'])
def crear_triaje():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    
    required = ['id_paciente']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO triajes (
                    id_paciente, id_usuario,
                    presion_arterial_sistolica, presion_arterial_diastolica,
                    frecuencia_cardiaca, temperatura, saturacion_oxigeno,
                    sintomas_principales, sintomas_texto_libre, antecedentes_relevantes,
                    nivel_urgencia, estado, fecha_atencion_inicio
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING *
            """, (
                data['id_paciente'],
                id_usuario,
                data.get('presion_arterial_sistolica'),
                data.get('presion_arterial_diastolica'),
                data.get('frecuencia_cardiaca'),
                data.get('temperatura'),
                data.get('saturacion_oxigeno'),
                data.get('sintomas_principales'),
                data.get('sintomas_texto_libre'),
                data.get('antecedentes_relevantes'),
                data.get('nivel_urgencia', 'pendiente'),
                data.get('estado', 'en_proceso')
            ))
            triaje = cursor.fetchone()
        
        log_auditoria(id_usuario, 'CREAR_TRIJE', 'triajes', triaje['id_triaje'])
        
        return jsonify(dict(triaje)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/triajes/<id_triaje>/completar', methods=['PUT'])
def completar_triaje(id_triaje):
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE triajes 
                SET nivel_urgencia = %s,
                    observaciones = %s,
                    fecha_atencion_fin = CURRENT_TIMESTAMP,
                    estado = 'completado'
                WHERE id_triaje = %s
                RETURNING *
            """, (
                data.get('nivel_urgencia'),
                data.get('observaciones'),
                id_triaje
            ))
            triaje = cursor.fetchone()
        
        if not triaje:
            return jsonify({'error': 'Triaje no encontrado'}), 404
        
        if data.get('resultado_ia'):
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO resultados_ia (
                        id_triaje, nivel_urgencia_sugerido, confiabilidad,
                        posibles_diagnosticos, recomendaciones, modelo_ia, parametros_entrada
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    id_triaje,
                    data['resultado_ia'].get('nivel_urgencia_sugerido'),
                    data['resultado_ia'].get('confiabilidad'),
                    data['resultado_ia'].get('posibles_diagnosticos'),
                    data['resultado_ia'].get('recomendaciones'),
                    data['resultado_ia'].get('modelo_ia', 'gpt-4'),
                    data['resultado_ia'].get('parametros_entrada')
                ))
        
        log_auditoria(id_usuario, 'COMPLETAR_TRIJE', 'triajes', id_triaje, {'nivel_urgencia': data.get('nivel_urgencia')})
        
        with get_db_cursor() as cursor:
            cursor.execute("SELECT p.numero_documento, t.* FROM triajes t JOIN pacientes p ON t.id_paciente = p.id_paciente WHERE t.id_triaje = %s", (id_triaje,))
            triaje_completo = cursor.fetchone()
        
        if triaje_completo:
            webhook_data = {
                'numero_documento': triaje_completo['numero_documento'],
                'id_triaje': str(triaje_completo['id_triaje']),
                'nivel_urgencia': triaje_completo['nivel_urgencia'],
                'fecha_hora': triaje_completo['fecha_hora'].isoformat() if triaje_completo['fecha_hora'] else None,
                'sintomas_principales': triaje_completo['sintomas_principales'],
                'presion_arterial_sistolica': triaje_completo.get('presion_arterial_sistolica'),
                'presion_arterial_diastolica': triaje_completo.get('presion_arterial_diastolica'),
                'frecuencia_cardiaca': triaje_completo.get('frecuencia_cardiaca'),
                'temperatura': float(triaje_completo.get('temperatura')) if triaje_completo.get('temperatura') else None,
                'saturacion_oxigeno': triaje_completo.get('saturacion_oxigeno'),
                'recomendaciones': data.get('resultado_ia', {}).get('recomendaciones') if data.get('resultado_ia') else None,
                'posibles_diagnosticos': data.get('resultado_ia', {}).get('posibles_diagnosticos') if data.get('resultado_ia') else None
            }
            try:
                n8n_webhook = os.getenv('N8N_WEBHOOK_TRIAGE', 'http://n8n:5678/webhook/triaje-completado')
                requests.post(n8n_webhook, json=webhook_data, timeout=10)
            except Exception as e:
                print(f"Warning: Could not notify n8n webhook: {e}")
        
        return jsonify(dict(triaje)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/operacional', methods=['GET'])
def dashboard_operacional():
    fecha = request.args.get('fecha', datetime.now().strftime('%Y-%m-%d'))
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_triajes,
                    COUNT(CASE WHEN nivel_urgencia = 'critico' THEN 1 END) as criticos,
                    COUNT(CASE WHEN nivel_urgencia = 'alto' THEN 1 END) as altos,
                    COUNT(CASE WHEN nivel_urgencia = 'moderado' THEN 1 END) as moderados,
                    COUNT(CASE WHEN nivel_urgencia = 'bajo' THEN 1 END) as bajos,
                    AVG(EXTRACT(EPOCH FROM (fecha_atencion_fin - fecha_atencion_inicio))/60) as tiempo_promedio_minutos
                FROM triajes
                WHERE DATE(fecha_hora) = %s
            """, (fecha,))
            metricas = cursor.fetchone()
            
            cursor.execute("""
                SELECT hora, COUNT(*) as cantidad
                FROM (
                    SELECT DATE_TRUNC('hour', fecha_hora) as hora
                    FROM triajes
                    WHERE DATE(fecha_hora) = %s
                ) sub
                GROUP BY hora
                ORDER BY hora
            """, (fecha,))
            triajes_por_hora = cursor.fetchall()
            
            cursor.execute("""
                SELECT nivel_urgencia, COUNT(*) as cantidad
                FROM triajes
                WHERE DATE(fecha_hora) = %s AND nivel_urgencia IS NOT NULL
                GROUP BY nivel_urgencia
            """, (fecha,))
            distribucion_urgencia = cursor.fetchall()
        
        return jsonify({
            'fecha': fecha,
            'metricas': dict(metricas) if metricas else {},
            'triajes_por_hora': [dict(t) for t in triajes_por_hora],
            'distribucion_urgencia': [dict(d) for d in distribucion_urgencia]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/gestion', methods=['GET'])
def dashboard_gestion():
    mes = request.args.get('mes', datetime.now().strftime('%Y-%m'))
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_triajes,
                    COUNT(CASE WHEN nivel_urgencia = 'critico' THEN 1 END) as criticos,
                    COUNT(CASE WHEN nivel_urgencia = 'alto' THEN 1 END) as altos,
                    COUNT(CASE WHEN nivel_urgencia = 'moderado' THEN 1 END) as moderados,
                    COUNT(CASE WHEN nivel_urgencia = 'bajo' THEN 1 END) as bajos,
                    AVG(EXTRACT(EPOCH FROM (fecha_atencion_fin - fecha_atencion_inicio))/60) as tiempo_promedio_minutos
                FROM triajes
                WHERE TO_CHAR(fecha_hora, 'YYYY-MM') = %s
            """, (mes,))
            metricas = cursor.fetchone()
            
            cursor.execute("""
                SELECT DATE(fecha_hora) as fecha, COUNT(*) as cantidad
                FROM triajes
                WHERE TO_CHAR(fecha_hora, 'YYYY-MM') = %s
                GROUP BY DATE(fecha_hora)
                ORDER BY fecha
            """, (mes,))
            triajes_por_dia = cursor.fetchall()
            
            cursor.execute("""
                SELECT u.nombre_completo, COUNT(*) as cantidad
                FROM triajes t
                JOIN usuarios u ON t.id_usuario = u.id_usuario
                WHERE TO_CHAR(t.fecha_hora, 'YYYY-MM') = %s
                GROUP BY u.nombre_completo
            """, (mes,))
            triajes_por_profesional = cursor.fetchall()
            
            cursor.execute("""
                SELECT nivel_urgencia, COUNT(*) as cantidad
                FROM triajes
                WHERE TO_CHAR(fecha_hora, 'YYYY-MM') = %s AND nivel_urgencia IS NOT NULL
                GROUP BY nivel_urgencia
            """, (mes,))
            distribucion_urgencia = cursor.fetchall()
        
        return jsonify({
            'mes': mes,
            'metricas': dict(metricas) if metricas else {},
            'triajes_por_dia': [dict(t) for t in triajes_por_dia],
            'triajes_por_profesional': [dict(t) for t in triajes_por_profesional],
            'distribucion_urgencia': [dict(d) for d in distribucion_urgencia]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hce/<numero_documento>/antecedentes', methods=['GET'])
def obtener_antecedentes_hce(numero_documento):
    try:
        import requests as req
        response = req.get(f'{HCE_API_URL}/api/pacientes/{numero_documento}/antecedentes', timeout=5)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify({'antecedentes': [], 'historial': []}), 200
    except Exception:
        return jsonify({'antecedentes': [], 'historial': []}), 200

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)

@app.route('/api/logs', methods=['GET'])
def obtener_logs():
    accion = request.args.get('accion', '')
    limite = request.args.get('limite', 50, type=int)
    
    try:
        with get_db_cursor() as cursor:
            if accion:
                cursor.execute("""
                    SELECT * FROM logs_auditoria 
                    WHERE accion = %s
                    ORDER BY fecha_hora DESC 
                    LIMIT %s
                """, (accion, limite))
            else:
                cursor.execute("""
                    SELECT * FROM logs_auditoria 
                    ORDER BY fecha_hora DESC 
                    LIMIT %s
                """, (limite,))
            logs = cursor.fetchall()
        
        return jsonify({'logs': [dict(log) for log in logs]}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'logs': []}), 500
