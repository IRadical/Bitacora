import flet as ft
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

def main(page: ft.Page):
    page.title = "Radical - Log Automator"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 500
    page.window_height = 700
    page.padding = 30

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        datos_json = json.load(f)

    lbl_status = ft.Text("Listo para generar la bitacora", color="blue")
    txt_horas = ft.TextField(
        label="Tiempo trabajado total",
        value=datos_json['horas_totales'],
        icon="timer"
    )
    txt_arranques = ft.TextField(
        label="total de Arranques",
        value=datos_json['arranques_totales'],
        icon="play_arrow"
    )

    def process_log(e):
        try:
            lbl_status.value = "Generando bitacora..."
            page.update()

            doc = DocxTemplate(PLANTILLA)

            contexto = {
                'fecha': datetime.now().strftime("%d/%m/%Y"),
                'horas': txt_horas.value,
                'arranques': txt_arranques.value,
                'fotos_antes': preparar_fotos(doc, FOTOS_DIR, "antes"),
                'fotos_durante': preparar_fotos(doc, FOTOS_DIR, "durante"),
                'fotos_despues': preparar_fotos(doc, FOTOS_DIR, "despues"),
                'fotos_niveles': preparar_fotos(doc, FOTOS_DIR, "niveles")
            }

            doc.render(contexto)

            fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_final = f"BITACORA DE MANTENIMIENTO DE PLANTA DE EMERGENCIA {fecha_archivo}.docx"
            ruta_salida = os.path.join(REPORTES_DIR, nombre_final)

            if not os.path.exists(REPORTES_DIR):
                os.makedirs(REPORTES_DIR)
            
            doc.save(ruta_salida)

            datos_json.update({
                "horas_totales": txt_horas.value,
                "arranques_totales": txt_arranques.value
            })
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, indent=4, ensure_ascii=False)

            lbl_status.value = f"¡Exito! Generado: {nombre_final}"
            lbl_status.color = "green"

        except Exception as ex:
                lbl_status.value = f"Error: {str(ex)}"
                lbl_status.color = "red"
            
        page.update()
    
    page.add(
         ft.Column([
              ft.Text("LOG AUTOMATOR", size=30, weight="bold", color="white"),
              ft.Divider(),
              ft.Text("Datos de la planta (IGSA)", size=16, color="grey"),
              txt_horas,
              txt_arranques,
              ft.ElevatedButton(
                   "GENERAR REPORTE",
                   icon="description",
                   on_click=process_log,
                   style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                   height=50
              ),
              ft.Divider(),
              lbl_status
         ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)