# Video de apoyo 2 — «De un script a un proyecto reproducible: Git y Docker»

Paso a paso para grabar. Cada bloque indica qué se muestra en pantalla, qué comando se escribe
y qué debe aparecer. Duración objetivo: **5 a 7 minutos**.

> **Antes de empezar**, deja el proyecto en el punto de partida: una carpeta con `src/` y
> `data/` y nada más. Los archivos que se van creando durante el video (`.gitignore`,
> `requirements.txt`, `Dockerfile`, `docker-compose.yml`) están en este repositorio: tenlos a
> mano en un editor para pegarlos, no los escribas de cero frente a la cámara.

---

## Lista de verificación previa

- [ ] Docker Desktop abierto y respondiendo: `docker version` muestra cliente **y** servidor.
- [ ] La imagen ya construida una vez antes de grabar, para que el `build` del video use caché
      y no tarde varios minutos: `docker compose build`.
- [ ] Terminal con fuente grande (16 pt o más) y ventana limpia: `clear`.
- [ ] `git config user.name` y `user.email` ya configurados.
- [ ] Carpeta de trabajo sin un `.git` previo (si estás repitiendo la toma: `rm -rf .git`).
- [ ] Datos presentes: `ls data/` muestra `calidad_agua.csv`.

---

## Introducción · 00:00 – 00:40

**En pantalla:** el script abierto en el editor.

Presenta el problema: el análisis funciona, pero solo aquí. No hay forma de saber qué versión
produjo cada número ni con qué librerías corrió. En los próximos minutos lo convertimos en un
proyecto que otra persona puede clonar y ejecutar.

Menciona explícitamente el NEEXO: Tema 1 (Git), Tema 2 (entornos y contenedores) y la Tabla 6
del Tema 3 (lista de verificación del cuaderno reproducible).

---

## Paso 1 · El punto de partida · 00:40 – 01:10

```bash
ls -R
python src/perfilamiento_agua.py
```

**Debe aparecer** la salida completa del perfilamiento, terminando en la tabla de Polars con
`6.84 / 1082` y `7.16 / 707`.

**Qué decir:** funciona. El problema no es que falle, es que nadie más puede repetirlo.

---

## Paso 2 · Historia: `git init` y el primer commit · 01:10 – 02:10

```bash
git init
git status
```

**Debe aparecer** `data/` y `src/` como archivos sin seguimiento.

Pega el `.gitignore` y repite:

```bash
git status
```

**Punto clave del video:** ahora `data/calidad_agua.csv` **ya no aparece**. Explica por qué: el
repositorio guarda el método, no la información; los datos pesan, cambian y a veces no se pueden
redistribuir. Lo que sí entra es el diccionario y, en el README, el origen y la suma de
verificación.

```bash
git add .
git commit -m "Perfilamiento de calidad del agua: version inicial del analisis"
git log --oneline
```

---

## Paso 3 · Entorno: fijar las versiones · 02:10 – 03:00

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy polars
pip freeze > requirements.txt
cat requirements.txt
```

**Qué decir:** `pip freeze` deja escrito con qué versiones corrió. Sin esto, «instala pandas» es
una instrucción distinta cada mes.

Muestra el `requirements.txt` del proyecto, que ya trae las versiones fijas con `==`.

```bash
git add requirements.txt
git commit -m "Fija las versiones del entorno con requirements.txt"
```

---

## Paso 4 · El Dockerfile · 03:00 – 04:10

Pega el `Dockerfile` y recórrelo línea por línea en pantalla. Tres puntos, y nada más:

1. `FROM python:3.13-slim` — la base va **fijada por versión**. Con `:latest` el proyecto deja de
   ser reproducible en cuanto la imagen base cambie.
2. `COPY requirements.txt` **antes** que el código — así Docker reutiliza la capa de instalación
   mientras las dependencias no cambien.
3. No se copia `data/` — la imagen contiene el método; los datos entran como volumen.

```bash
docker build -t pa-u1-perfilamiento:1.0 .
```

---

## Paso 5 · La demostración que vale el video · 04:10 – 05:10

Primero **sin** el volumen:

```bash
docker run --rm pa-u1-perfilamiento:1.0
```

**Debe fallar** con:

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/calidad_agua.csv'
```

**Qué decir:** esto no es un error, es la prueba de que la imagen no esconde los datos adentro.

Ahora **con** el volumen:

```bash
docker run --rm -v "$PWD/data:/app/data:ro" pa-u1-perfilamiento:1.0
```

> En PowerShell: `docker run --rm -v "${PWD}/data:/app/data:ro" pa-u1-perfilamiento:1.0`

**Debe aparecer** la misma salida del paso 1, idéntica, pero ahora dentro del contenedor.

---

## Paso 6 · Compose y el cuaderno · 05:10 – 06:10

Pega el `docker-compose.yml` y explica que recoge en un archivo lo que acabas de escribir a mano.

```bash
docker compose run --rm perfilar
docker compose up jupyter
```

Abre `http://localhost:8888`, entra a `perfilamiento_agua.ipynb` y muestra **Kernel → Restart
Kernel and Run All Cells**.

**Qué decir:** reiniciar el kernel y ejecutar todo es lo que distingue un cuaderno que funciona
de uno que parece funcionar. Es el punto 1 de la Tabla 6 del NEEXO.

```bash
docker compose down
```

---

## Cierre · 06:10 – 06:50

```bash
git add Dockerfile docker-compose.yml README.md
git commit -m "Agrega entorno reproducible con Docker y Compose"
git log --oneline
git tag -a v1.0 -m "Version del analisis reportada en el informe"
git rev-parse HEAD
```

**Qué decir:** ese identificador es el que se cita en el informe. Con él, el `requirements.txt`
y el `Dockerfile`, cualquier persona reconstruye exactamente este resultado.

Cierra enunciando la evidencia que pide la Actividad 1 de la unidad: repositorio con historia,
entorno declarado, Dockerfile y cuaderno que corre completo.

---

## Si algo falla durante la grabación

| Síntoma | Causa más probable | Salida |
|---|---|---|
| `docker: command not found` | Docker Desktop cerrado | Ábrelo y espera a que el ícono quede estable. |
| El `build` tarda minutos | Caché fría | Construye antes de grabar; en el video se ve con caché. |
| `permission denied` en el volumen | Ruta con espacios o unidad no compartida | Comillas en `"$PWD/data:/app/data:ro"`; en Windows, comparte la unidad en Docker Desktop. |
| Puerto 8888 ocupado | Otro Jupyter corriendo | `docker compose down`, o cambia a `8889:8888` en el compose. |
| El cuaderno no ve los datos | Se abrió fuera de `/app` | La ruta `data/calidad_agua.csv` es relativa a la carpeta del cuaderno. |

---

*Material del curso: María Fernanda Ochoa · Programación avanzada · Unidad 1*
