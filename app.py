from flask import Flask, render_template, jsonify
import random
import datetime

app = Flask(__name__)

EPS = ["Sura", "Sanitas", "Nueva EPS", "Salud Total", "Coosalud"]
IPS_CALI = ["Fundación Valle del Lili", "Clínica Imbanaco", "HUV", "ESE Ladera", "Clínica Farallones"]

CUPS_DB = [
    {"codigo": "890201", "descripcion": "Consulta de primera vez por medicina general"},
    {"codigo": "903866", "descripcion": "Hemograma completo automatizado"},
    {"codigo": "881340", "descripcion": "Ecografía de abdomen total"},
    {"codigo": "933600", "descripcion": "Sesión de fisioterapia integral"},
    {"codigo": "011101", "descripcion": "Craneotomía diagnóstica vía abierta"},
    {"codigo": "371101", "descripcion": "Cardiotomía de revisión inmediata"}
]

CIE11_DB = [
    {"codigo": "BA41.Z", "descripcion": "Hipertensión arterial esencial"},
    {"codigo": "5B51.5", "descripcion": "Diabetes mellitus tipo 2 asociada a obesidad"},
    {"codigo": "CA40.0", "descripcion": "Asma extrínseca con crisis aguda"},
    {"codigo": "BC60.3", "descripcion": "Infarto agudo de miocardio"},
    {"codigo": "FA01.0", "descripcion": "Trastorno depresivo mayor"}
]

RIPS_TIPOS = ["AM (Medicamentos)", "AP (Procedimientos)", "AC (Consultas)", "AU (Urgencias)", "AH (Hospitalización)"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datos_ia')
def datos_ia():
    hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
    id_rips = f"RIPS-{random.randint(100000, 999999)}"
    
    procedimiento = random.choice(CUPS_DB)
    diagnostico = random.choice(CIE11_DB)
    entidad = random.choice(IPS_CALI)
    cobertura = random.choice(EPS)
    tipo_rips = random.choice(RIPS_TIPOS)
    medico = random.choice(["Dr. Juan Arana", "Dra. Elena Ortiz", "Dr. Luis Vivas", "Dra. Sara Restrepo"])
    
    if "Consulta" in procedimiento["descripcion"] or "Hemograma" in procedimiento["descripcion"]:
        valor = random.randint(45000, 180000)
    elif "Ecografía" in procedimiento["descripcion"] or "Fisioterapia" in procedimiento["descripcion"]:
        valor = random.randint(250000, 950000)
    else: 
        valor = random.randint(15000000, 55000000)

    if random.random() < 0.25: 
        valor = valor * 150  
        
    if "Consulta" in procedimiento["descripcion"] and valor > 500000:
        estado = "FRAUDE DETECTADO"
        color = "#d32f2f"
        motivo = "Sobrecosto severo: Tarifa excede el manual tarifario."
        antecedentes = "Alta reincidencia. 3 glosas previas por sobrefacturación."
        riesgo_puntuacion = "98%"
    elif valor > 20000000:
        estado = "ALTO RIESGO"
        color = "#ffa500"
        motivo = "Costo elevado bajo revisión de pertinencia médica."
        antecedentes = "Entidad bajo observación preventiva por el Ministerio."
        riesgo_puntuacion = "72%"
    else:
        estado = "AUDITADO"
        color = "#2e7d32"
        motivo = "Concordancia médica y tarifaria correcta."
        antecedentes = "Historial limpio. Comportamiento dentro del promedio."
        riesgo_puntuacion = "12%"

    return jsonify({
        "hora": hora_actual,
        "rips_id": id_rips,
        "tipo_rips": tipo_rips,
        "entidad": entidad,
        "eps": cobertura,
        "cups_cod": procedimiento["codigo"],
        "cups_desc": procedimiento["descripcion"],
        "cie11_cod": diagnostico["codigo"],
        "cie11_desc": diagnostico["descripcion"],
        "valor": f"${valor:,}",
        "estado": estado,
        "color": color,
        "motivo": motivo,
        "medico": medico,
        "antecedentes": antecedentes,
        "riesgo": riesgo_puntuacion,
        "fecha": datetime.datetime.now().strftime('%d/%m/%Y')
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)