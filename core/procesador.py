import os
from docxtpl import InlineImage
from docx.shared import Mm

def preparar_fotos(doc, ruta_fotos, subcarpeta, ancho_mm=75):
    ruta = os.path.join(ruta_fotos, subcarpeta)
    lista_fotos = []
    
    if os.path.exists(ruta):
        archivos = sorted([f for f in os.listdir(ruta) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        for archivo in archivos:
            ruta_completa = os.path.join(ruta, archivo)
            lista_fotos.append(InlineImage(doc, ruta_completa, width=Mm(ancho_mm)))
    
    return lista_fotos