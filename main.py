import flet as ft
import os
import json
import shutil
from datetime import datetime
from docxtpl import DocxTemplate
from core.procesador import preparar_fotos 

PLANTILLA_NOMBRE = "plantilla_maestra.docx"
CARPETA_REPORTES = "reportes_finales"
BASE_DIR = os.path.dirname(__file__)
PLANTILLA = os.path.join(BASE_DIR, PLANTILLA_NOMBRE)
REPORTES_DIR = os.path.join(BASE_DIR, CARPETA_REPORTES)
DATA_FILE = os.path.join(BASE_DIR, "data", "persistencia.json")
FOTOS_DIR = os.path.join(BASE_DIR, "fotos")
CATEGORIAS = ["antes", "durante", "despues", "niveles"]

def main(page: ft.Page):
    page.title = "Radical - Log Automator"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 600
    page.window_height = 900
    page.scroll = "auto"

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        datos_json = json.load(f)

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            dest_folder = page.session.get("current_upload")
            target_path = os.path.join(FOTOS_DIR, dest_folder)
            
            if not os.path.exists(target_path):
                os.makedirs(target_path)
                
            for file in e.files:
                timestamp = datetime.now().strftime("%H%M%S_%f")
                filename = f"{timestamp}_{file.name}"
                shutil.copy(file.path, os.path.join(target_path, filename))
            
            lbl_status.value = f"{len(e.files)} fotos añadidas a '{dest_folder}'"
            lbl_status.color = ft.colors.GREEN
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.append(file_picker)

    def open_picker(categoria):
        page.session.set("current_upload", categoria)
        file_picker.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE)

    def clear_photos(e):
        for cat in CATEGORIAS:
            folder = os.path.join(FOTOS_DIR, cat)
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path): os.unlink(file_path)
                    except: pass
        lbl_status.value = "Fotos eliminadas"
        lbl_status.color = ft.colors.ORANGE
        page.update()

    lbl_status = ft.Text("Listo para generar la bitácora", color=ft.colors.BLUE)
    
    txt_horas = ft.TextField(
        label="Tiempo trabajado total",
        value=datos_json['horas_totales'],
        prefix_icon=ft.icons.TIMER,
        expand=True
    )
    txt_arranques = ft.TextField(
        label="Total de Arranques",
        value=datos_json['arranques_totales'],
        prefix_icon=ft.icons.PLAY_ARROW,
        expand=True
    )

    def build_drop_zone(label, color, category):
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.UPLOAD_FILE, color=color, size=30),
                ft.Text(label, weight="bold", size=12),
            ], horizontal_alignment="center", alignment="center"),
            bgcolor=ft.colors.with_opacity(0.1, color),
            border=ft.border.all(2, color),
            border_radius=10,
            padding=10,
            expand=True,
            height=150,
            on_click=lambda _: open_picker(category)
        )

    def process_log(e):
        try:
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
            
            nombre_final = f"BITACORA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            ruta_salida = os.path.join(REPORTES_DIR, nombre_final)
            
            if not os.path.exists(REPORTES_DIR): os.makedirs(REPORTES_DIR)
            doc.save(ruta_salida)

            datos_json.update({"horas_totales": txt_horas.value, "arranques_totales": txt_arranques.value})
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, indent=4, ensure_ascii=False)

            lbl_status.value = f"Éxito: {nombre_final}"
            lbl_status.color = ft.colors.GREEN
        except Exception as ex:
            lbl_status.value = f"Error: {str(ex)}"
            lbl_status.color = ft.colors.RED
        page.update()

    page.add(
        ft.Text("LOG AUTOMATOR PRO", size=28, weight="bold"),
        ft.Row([txt_horas, txt_arranques]),
        ft.Text("Carga de Imágenes", size=18, weight="bold"),
        ft.Row([
            build_drop_zone("ANTES", ft.colors.BLUE, "antes"),
            build_drop_zone("DURANTE", ft.colors.ORANGE, "durante"),
        ]),
        ft.Row([
            build_drop_zone("DESPUÉS", ft.colors.GREEN, "despues"),
            build_drop_zone("NIVELES", ft.colors.PURPLE, "niveles"),
        ]),
        ft.Divider(),
        ft.FilledButton("GENERAR REPORTE", icon=ft.icons.REPLAY_CIRCLE_FILLED, on_click=process_log, width=600, height=50),
        ft.OutlinedButton("LIMPIAR FOTOS", icon=ft.icons.DELETE_SWEEP, on_click=clear_photos, width=600),
        lbl_status
    )


if __name__ == "__main__":
    ft.app(target=main)