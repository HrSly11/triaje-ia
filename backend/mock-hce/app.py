from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

ANTECEDENTES_BASE = {
    'hipertension': {'tipo': 'enfermedad', 'descripcion': 'Hipertensión arterial diagnosticada hace 5 años'},
    'diabetes': {'tipo': 'enfermedad', 'descripcion': 'Diabetes mellitus tipo 2 en tratamiento'},
    'asma': {'tipo': 'enfermedad', 'descripcion': 'Asma bronquial desde la infancia'},
    'alergias': {'tipo': 'alergia', 'descripcion': 'Alergia a penicilina y codeína'},
    'cirugia': {'tipo': 'procedimiento', 'descripcion': 'Apendicectomía en 2015'},
    'fumador': {'tipo': 'habito', 'descripcion': 'Ex-fumador, dejó hace 3 años'},
    'obesidad': {'tipo': 'condicion', 'descripcion': 'IMC 32, sigue control nutricional'},
}

HISTORIAL_SINTOMAS = [
    'Dolor de cabeza', 'Fiebre', 'Tos', 'Dificultad respiratoria',
    'Dolor abdominal', 'Náuseas', 'Mareos', 'Dolor torácico',
    'Fatiga', 'Insomnio', 'Dolor articular', 'Erupciones cutáneas'
]

PACIENTES_MOCK = {}

def generar_paciente_mock(numero_documento):
    nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Sofia', 'Pedro', 'Laura']
    apellidos = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Hernández', 'Pérez', 'Sánchez']
    
    nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
    fecha_nacimiento = datetime.now() - timedelta(days=random.randint(3650, 25550))
    
    return {
        'id_paciente': str(uuid.uuid4()),
        'numero_documento': numero_documento,
        'tipo_documento': 'CC',
        'nombre_completo': nombre,
        'fecha_nacimiento': fecha_nacimiento.strftime('%Y-%m-%d'),
        'genero': random.choice(['M', 'F']),
        'telefono': f"+57 3{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
        'correo': f"{numero_documento}@email.com",
        'direccion': f"Cra {random.randint(1, 100)} # {random.randint(1, 99)}-{random.randint(1, 99)}",
    }

def generar_antecedentes():
    antecedentes = []
    for key, value in random.sample(list(ANTECEDENTES_BASE.items()), random.randint(1, 4)):
        ant = dict(value)
        ant['nombre'] = key
        ant['fecha_deteccion'] = (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime('%Y-%m-%d')
        antecedentes.append(ant)
    return antecedentes

def generar_historial_sintomas():
    historial = []
    for _ in range(random.randint(2, 8)):
        historial.append({
            'fecha': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'sintoma': random.choice(HISTORIAL_SINTOMAS),
            'diagnostico': f"Episodio de {random.choice(HISTORIAL_SINTOMAS).lower()}",
            'tratamiento': f"Tratamiento estándar aplicado"
        })
    return sorted(historial, key=lambda x: x['fecha'], reverse=True)

def generar_signos_vitales():
    return {
        'presion_arterial': f"{random.randint(90, 160)}/{random.randint(60, 100)}",
        'frecuencia_cardiaca': random.randint(60, 120),
        'temperatura': round(random.uniform(36.0, 39.5), 1),
        'saturacion_oxigeno': random.randint(92, 100),
        'frecuencia_respiratoria': random.randint(12, 24),
        'peso': round(random.uniform(50, 100), 1),
        'altura': round(random.uniform(1.50, 1.90), 2),
    }

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'mock-hce'}), 200

@app.route('/api/pacientes/<numero_documento>', methods=['GET'])
def obtener_paciente(numero_documento):
    if numero_documento not in PACIENTES_MOCK:
        PACIENTES_MOCK[numero_documento] = generar_paciente_mock(numero_documento)
    
    return jsonify(PACIENTES_MOCK[numero_documento]), 200

@app.route('/api/pacientes/<numero_documento>/antecedentes', methods=['GET'])
def obtener_antecedentes(numero_documento):
    if numero_documento not in PACIENTES_MOCK:
        PACIENTES_MOCK[numero_documento] = generar_paciente_mock(numero_documento)
    
    return jsonify({
        'numero_documento': numero_documento,
        'antecedentes': generar_antecedentes(),
        'historial_sintomas': generar_historial_sintomas(),
        'signos_vitales_base': generar_signos_vitales(),
        'fecha_ultima_atencion': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
    }), 200

@app.route('/api/pacientes', methods=['POST'])
def crear_paciente():
    data = request.get_json()
    numero_documento = data.get('numero_documento')
    
    if not numero_documento:
        return jsonify({'error': 'Número de documento requerido'}), 400
    
    if numero_documento in PACIENTES_MOCK:
        return jsonify({'error': 'Paciente ya existe'}), 409
    
    nuevo_paciente = generar_paciente_mock(numero_documento)
    for key in ['tipo_documento', 'nombre_completo', 'fecha_nacimiento', 'genero', 'telefono', 'correo', 'direccion']:
        if key in data:
            nuevo_paciente[key] = data[key]
    
    PACIENTES_MOCK[numero_documento] = nuevo_paciente
    return jsonify(nuevo_paciente), 201

@app.route('/api/pacientes/<numero_documento>/triaje', methods=['POST'])
def registrar_triaje_hce(numero_documento):
    data = request.get_json()
    
    if numero_documento not in PACIENTES_MOCK:
        PACIENTES_MOCK[numero_documento] = generar_paciente_mock(numero_documento)
    
    return jsonify({
        'id_triaje_hce': str(uuid.uuid4()),
        'numero_documento': numero_documento,
        'fecha_registro': datetime.now().isoformat(),
        'estado': 'registrado',
        'datos_triaje': data
    }), 201

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=True)
