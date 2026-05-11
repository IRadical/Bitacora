import os
import json
from datetime import datetime
from docxtpl import DocxTemplate
from core.procesador import preparar_fotos 

NOMBRE_USUARIO = "Radical"
PLANTILLA_NOMBRE = "plantilla_maestra.docx"
CARPETA_REPORTES = "reportes_finales"

BASE_DIR = os.path.dirname(__file__)
PLANTILLA = os.path.join(BASE_DIR, PLANTILLA_NOMBRE)
REPORTES_DIR = os.path.join(BASE_DIR, CARPETA_REPORTES)
DATA_FILE = os.path.join(BASE_DIR, "data", "persistencia.json")
FOTOS_DIR = os.path.join(BASE_DIR, "fotos")

def generar_bitacora():
    if not os.path.exists(DATA_FILE):
        print(f"Error: No se encontró {DATA_FILE}")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    print(f"--- GENERADOR BITACORA | USUARIO: {NOMBRE_USUARIO} ---")
    
    print(f"Último registro: {datos['horas_totales']} | {datos['arranques_totales']} arranques")
    horas_input = input("Ingresa el Tiempo Trabajado Total (ej. 329h 42m): ")
    arranques_input = input("Ingresa el Total de Arranques (ej. 1217): ")

    try:
        doc = DocxTemplate(PLANTILLA)
    except Exception as e:
        print(f"Error al abrir la plantilla: {e}")
        print("Tip: Si sale KeyError 'NULL', copia el contenido a un Word nuevo y guárdalo.")
        return

    contexto = {
        'fecha': datetime.now().strftime("%d/%m/%Y"),
        'horas': horas_input,
        'arranques': arranques_input,
        'fotos_antes': preparar_fotos(doc, FOTOS_DIR, "antes"),
        'fotos_durante': preparar_fotos(doc, FOTOS_DIR, "durante"),
        'fotos_despues': preparar_fotos(doc, FOTOS_DIR, "despues"),
        'fotos_niveles': preparar_fotos(doc, FOTOS_DIR, "niveles")
    }

    doc.render(contexto)
    
    fecha_archivo = datetime.now().strftime("%d-%m-%Y")
    nombre_final = f"BITACORA DE MANTENIMIENTO DE PLANTA DE EMERGENCIA {fecha_archivo}.docx"
    ruta_salida = os.path.join(REPORTES_DIR, nombre_final)

    if not os.path.exists(REPORTES_DIR):
        os.makedirs(REPORTES_DIR)

    doc.save(ruta_salida)

    datos.update({
        "horas_totales": horas_input,
        "arranques_totales": arranques_input
    })
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Reporte generado: {nombre_final}")

if __name__ == "__main__":
    generar_bitacora()