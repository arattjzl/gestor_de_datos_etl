##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: txt_extractor.py
# Capitulo: Flujo de Datos
# Autor(es): Equipo 5
# Version: 1.0.0 abril 2024
# Descripción:
#
#   Este archivo define un procesador de datos que se encarga de extraer
#   el contenido de un archivo XML
#-------------------------------------------------------------------------
import luigi, os
from os.path import isfile, join
from src.readers.zip_reader import ZIPReader

class TXTExtractor(luigi.Task):

    def requires(self):
        return ZIPReader()

    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        assets_dir = join(project_dir, "assets")
        files = [f for f in os.listdir(assets_dir) if isfile(join(assets_dir, f))]
        txt_files = [f for f in files if f.endswith(".txt")]
        targets = []
        for file in txt_files:
            targets.append(luigi.LocalTarget(join(assets_dir, file)))
        return targets