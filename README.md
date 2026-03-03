# PDF Joiner por carpeta

Script para **Python 3.8** que recorre recursivamente un árbol de carpetas y crea, en cada carpeta, un PDF con el nombre de esa carpeta.

Ejemplo:

- `FRUTAS/TOMATE/a.pdf` + `FRUTAS/TOMATE/b.pdf` → `FRUTAS/TOMATE/TOMATE.pdf`
- `FRUTAS/PERA/a.pdf` + `FRUTAS/PERA/b.pdf` → `FRUTAS/PERA/PERA.pdf`
- `FRUTAS/BANANA/a.pdf` + `FRUTAS/BANANA/b.pdf` → `FRUTAS/BANANA/BANANA.pdf`

## Requisitos

```bash
pip install PyPDF2==3.0.1
```

## Uso

Desde la carpeta del script:

```bash
python join_pdfs_por_carpeta.py "C:\\ruta\\a\\FRUTAS"
```

Si no pasás ruta, usa la carpeta actual:

```bash
python join_pdfs_por_carpeta.py
```

Modo silencioso:

```bash
python join_pdfs_por_carpeta.py "C:\\ruta\\a\\FRUTAS" --quiet
```

## Comportamiento

- Procesa **cada carpeta** del árbol.
- Une solo los PDFs que están **directamente** dentro de esa carpeta.
- El resultado se llama `<NOMBRE_CARPETA>.pdf` y se guarda en esa misma carpeta.
- Si ya existe ese archivo, se reemplaza.
- El propio archivo de salida no se vuelve a agregar a sí mismo.
