# Perfilamiento de la calidad del agua

Proyecto reproducible de la **Unidad 1 — Reproducibilidad, entornos y manipulación de datos**
de la asignatura *Programación avanzada* (Escuela Colombiana de Ingeniería Julio Garavito).

---

## 1. ¿Qué es este proyecto?

Perfila un conjunto de 3.276 muestras de agua con nueve variables fisicoquímicas y una
etiqueta de potabilidad: cuantifica valores ausentes y duplicados, obtiene los estadísticos
descriptivos y el balance de clases, contrasta las mediciones contra rangos de referencia con
máscaras booleanas de NumPy, detecta atípicos con el puntaje z y construye el perfil por clase,
primero con Pandas y después con Polars en modo diferido.

Es el soporte práctico del Anexo A del NEEXO y el proyecto que se usa en el **Video de apoyo 2:
«De un script a un proyecto reproducible: Git y Docker»**.

Contiene dos formas de ver lo mismo:

| Archivo | Para qué sirve |
|---|---|
| `src/perfilamiento_agua.py` | El análisis como script: una sola ejecución, salida por consola. |
| `perfilamiento_agua.ipynb` | El mismo análisis como cuaderno, explicado paso a paso. Se entrega ya ejecutado. |

---

## 2. ¿Cómo se instala?

Hay dos caminos. El segundo es el que se graba en el video.

### Opción A — Entorno virtual local

Requiere Python 3.13.

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows:  .venv\Scripts\activate
pip install -r requirements.txt
```

### Opción B — Docker (recomendada)

Requiere Docker Desktop o Docker Engine con el complemento Compose. No hace falta tener Python
instalado.

```bash
docker compose build
```

---

## 3. ¿Cómo se ejecuta?

### Con entorno virtual

```bash
python src/perfilamiento_agua.py        # el script
jupyter lab                              # y abrir perfilamiento_agua.ipynb
```

### Con Docker

```bash
docker compose run --rm perfilar        # ejecuta el script y termina
docker compose up jupyter                # abre JupyterLab en http://localhost:8888
```

Para detener JupyterLab: `Ctrl+C`, y después `docker compose down`.

### Qué se debe ver

La salida completa esperada está en [`docs/salida_esperada.txt`](docs/salida_esperada.txt).
Las cifras de control, para verificar de un vistazo que la ejecución fue correcta:

| Verificación | Valor esperado |
|---|---|
| Dimensión | `(3276, 10)` |
| Ausentes | pH 15,0 % · Sulfatos 23,8 % · Trihalometanos 4,9 % |
| Filas duplicadas | `0` |
| Balance de clases | 0,61 no potable / 0,39 potable |
| Fuera de rango | pH 1457 de 2785 · Cloraminas 3187 de 3276 · THM 602 de 3114 · Turbidez 314 de 3276 |
| Atípicos en Dureza (\|z\| > 3) | `18` |
| Consulta en Polars | NO → pH 6,84 (1082 filas) · SI → pH 7,16 (707 filas) |

Si alguna cifra no coincide, lo primero que hay que revisar es la versión de las librerías
(`pip freeze`) y la suma de verificación del archivo de datos (sección 4).

---

## 4. ¿De dónde salen los datos?

`data/calidad_agua.csv` — 3.276 filas × 10 columnas, 518.883 bytes.

* **Origen:** conjunto público *Water Quality* (potabilidad del agua), distribuido en Kaggle
  por Aditya Kadiwal bajo licencia CC0 (dominio público). Las columnas se renombraron al
  español; los valores no se modificaron.
* **Suma de verificación:** `md5 = acf24aba3c4bb29f05def7122fae1de0`

  Para comprobarla:
  ```bash
  md5sum data/calidad_agua.csv          # en macOS:  md5 data/calidad_agua.csv
  ```
* **Diccionario de variables:** `data/diccionario.csv`, con la unidad y el rango de referencia
  de cada variable. Los rangos que usa el análisis están en la constante `LIMITES` del script.

El archivo de datos **no se versiona en Git**: `.gitignore` excluye `data/*.csv`. Esa es una
decisión deliberada de la Unidad 1 —el repositorio guarda el método, no la información— y por
eso este README documenta el origen y la suma de verificación: son los datos que permiten
recuperar exactamente el mismo archivo.

---

## 5. Estructura

```
.
├── Dockerfile                  # cómo se construye el entorno de ejecución
├── docker-compose.yml          # dos servicios: perfilar y jupyter
├── requirements.txt            # dependencias con versión fija
├── .gitignore                  # qué NO entra al repositorio
├── .dockerignore               # qué NO entra a la imagen
├── README.md
├── perfilamiento_agua.ipynb    # el análisis explicado, ya ejecutado
├── data/
│   ├── calidad_agua.csv        # datos (no versionado)
│   └── diccionario.csv         # variables, unidades y rangos de referencia
├── src/
│   └── perfilamiento_agua.py   # el análisis como script
├── salidas/                    # resultados generados (no versionado)
└── docs/
    ├── salida_esperada.txt     # salida completa de una ejecución correcta
    └── GUION_VIDEO2.md         # paso a paso para grabar el Video de apoyo 2
```

---

## 6. Entorno verificado

| Componente | Versión |
|---|---|
| Python | 3.13 |
| pandas | 3.0.5 |
| NumPy | 2.5.3 |
| Polars | 1.44.2 |
| JupyterLab | 4.6.6 |

El cuaderno de este repositorio se ejecutó completo con esas versiones, con el kernel
reiniciado y de principio a fin.

---

## 7. Dos advertencias de uso

* **`--IdentityProvider.token=` en `docker-compose.yml`** desactiva el token de JupyterLab para
  que el servicio abra sin pedir clave durante la clase. El puerto está atado a `127.0.0.1`, de
  modo que solo es accesible desde este computador. Si el proyecto se publica en un servidor,
  hay que quitar esa línea.
* **El contenedor corre como `root`**, que es lo que evita problemas de permisos con los
  volúmenes montados en Windows, macOS y Linux. En un despliegue real se define un usuario sin
  privilegios con `USER`.

---

*Material del curso: María Fernanda Ochoa · Programación avanzada · Unidad 1*
