##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: txt_transformer.py
# Capitulo: Flujo de Datos
# Autor(es): Equipo 5
# Version: 1.0.0 abril 2024
# Descripción:
#
#   Este archivo define un procesador de datos que se encarga de transformar
#   y formatear el contenido de un archivo HTM
#-------------------------------------------------------------------------
from src.extractors.txt_extractor import TXTExtractor
from os.path import join
import luigi, os, json

class TXTTransformer(luigi.Task):

    def requires(self):
        return TXTExtractor()

    def run(self):
        result = []
        for file in self.input():
            with file.open() as txt_file:
                texto = txt_file.read() # se lee el archivo completo
                texto = texto.replace("\n", ",") # cambia el salto de línea por una coma
                lineas = texto.split(';')[:-1] # obtiene todos los registros separados por ";" omitiendo el último ya que este era una lista vacía
                for linea in lineas:
                    datos = linea.split(',') # obtiene todos los campos de cada registro separados por ','
                    result.append(
                                {
                                    "description": datos[-6],
                                    "quantity": str(abs(int(datos[-5]))),
                                    "price": str(abs(float(datos[-3]))),
                                    "total": abs(float(datos[-5]) * float(datos[-3])),
                                    "invoice": datos[-8],
                                    "provider": datos[-2],
                                    "country": datos[-1],
                                }
                            )
        with self.output().open('w') as out:
            out.write(json.dumps(result, indent=4))

    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))