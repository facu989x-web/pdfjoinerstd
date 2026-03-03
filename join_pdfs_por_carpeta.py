#!/usr/bin/env python3
"""Une PDFs por carpeta recorriendo un árbol de directorios.

Para cada carpeta visitada, se crea (o reemplaza) un PDF cuyo nombre es el de
la carpeta y cuyo contenido es la concatenación de todos los PDFs que están
*directamente* dentro de esa carpeta.
"""

import argparse
import os
import sys
from typing import List

try:
    from PyPDF2 import PdfMerger
except ImportError:
    print(
        "Error: falta PyPDF2. Instalalo con: pip install PyPDF2==3.0.1",
        file=sys.stderr,
    )
    raise


PDF_EXTENSION = ".pdf"


def listar_pdfs_de_carpeta(carpeta: str, nombre_salida: str) -> List[str]:
    """Devuelve la lista de PDFs de una carpeta excluyendo el archivo de salida."""
    archivos_pdf = []
    for nombre in os.listdir(carpeta):
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta):
            continue
        if not nombre.lower().endswith(PDF_EXTENSION):
            continue
        if nombre.lower() == nombre_salida.lower():
            continue
        archivos_pdf.append(ruta)

    archivos_pdf.sort(key=lambda p: os.path.basename(p).lower())
    return archivos_pdf


def unir_pdfs(archivos_pdf: List[str], salida_pdf: str) -> None:
    """Concatena una lista de archivos PDF en un único PDF de salida."""
    merger = PdfMerger()
    try:
        for archivo in archivos_pdf:
            merger.append(archivo)
        merger.write(salida_pdf)
    finally:
        merger.close()


def procesar_arbol(ruta_base: str, verbose: bool = True) -> int:
    """Procesa recursivamente el árbol y crea un PDF por carpeta.

    Retorna la cantidad de PDFs generados.
    """
    generados = 0

    for carpeta_actual, _, _ in os.walk(ruta_base):
        nombre_carpeta = os.path.basename(os.path.normpath(carpeta_actual))
        if not nombre_carpeta:
            # Caso raíz tipo "C:\\"
            nombre_carpeta = "resultado"

        nombre_salida = f"{nombre_carpeta}.pdf"
        salida_pdf = os.path.join(carpeta_actual, nombre_salida)

        archivos_pdf = listar_pdfs_de_carpeta(carpeta_actual, nombre_salida)
        if not archivos_pdf:
            if verbose:
                print(f"[SKIP] {carpeta_actual} (sin PDFs)")
            continue

        unir_pdfs(archivos_pdf, salida_pdf)
        generados += 1

        if verbose:
            print(
                f"[OK] {salida_pdf} | archivos unidos: {len(archivos_pdf)}"
            )

    return generados


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Recorre carpetas recursivamente y crea un PDF por carpeta "
            "con los PDFs que contiene."
        )
    )
    parser.add_argument(
        "ruta",
        nargs="?",
        default=".",
        help="Ruta base a recorrer (por defecto: carpeta actual).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="No muestra logs por carpeta.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ruta_base = os.path.abspath(args.ruta)

    if not os.path.isdir(ruta_base):
        print(f"Error: la ruta no existe o no es carpeta: {ruta_base}", file=sys.stderr)
        return 1

    generados = procesar_arbol(ruta_base, verbose=not args.quiet)
    print(f"\nTotal de PDFs generados: {generados}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
