# 🧠 RAM Scanner

**¿Qué coño se está comiendo mi RAM?** RAM Scanner escanea todos los procesos, los agrupa por aplicación y te genera un informe visual en HTML (o JSON/CSV) para que lo veas de un vistazo.

!\[Python](https://img.shields.io/badge/python-3.8%2B-blue) !\[Plataformas](https://img.shields.io/badge/Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) !\[Licencia](https://img.shields.io/badge/licencia-MIT-green)

## ✨ Características

* 🗺️ **Mapa de consumo**: cada bloque es una app, su tamaño es lo que gasta.
* 📦 **Agrupa por aplicación**: Chrome con 40 procesos aparece como una sola fila, con todos sus PID.
* 🏷️ **Categorías** (navegadores, desarrollo, sistema...) con filtro y totales.
* 💡 **Diagnóstico automático**: quién manda, apps con demasiados procesos, swap en uso, RAM al límite.
* 🔍 **Detector de fugas** (`--watch`): marca las apps cuya memoria crece mientras vigilas.
* 🔎 Tabla con **búsqueda y ordenación**. Modo claro/oscuro automático.
* 📄 Exporta a **HTML, JSON o CSV**. Un solo archivo, sin conexión a internet.

## 🚀 Instalación

Necesitas Python 3.8 o superior.

```bash
git clone https://github.com/mortiZimmerman/RamScanner.git
cd RamScan
python -m pip install -r requirements.txt
```

## 🧪 Uso

```bash
python ram\_scanner.py --open                 # informe HTML y lo abre en el navegador
python ram\_scanner.py -o datos.csv           # exporta a CSV (también .json)
python ram\_scanner.py --top 30               # solo las 30 apps que más consumen
python ram\_scanner.py --watch 60 --open      # vigila 60 s y detecta fugas de memoria
```

|Opción|Qué hace|
|-|-|
|`-o, --output`|Archivo de salida. La extensión decide el formato (`.html`, `.json`, `.csv`).|
|`--top N`|Guarda solo las N apps con más consumo.|
|`-w, --watch SEG`|Toma dos fotos con SEG segundos de diferencia y marca las que crecen.|
|`--open`|Abre el informe al terminar.|

> 💡 En Windows/macOS/Linux, ejecútalo como administrador (o con `sudo`) para ver los procesos de otros usuarios.

## ⚙️ Cómo funciona

Usa [`psutil`](https://github.com/giampaolo/psutil) para leer la memoria residente (RSS) de cada proceso, los suma por nombre y rellena una plantilla HTML (`report\_template.html`) con los datos incrustados.

## 🗺️ Roadmap

* \[ ] Modo en vivo con servidor local
* \[ ] Comparar dos informes
* \[ ] Botón para cerrar procesos

## 🤝 Contribuir

¡Los PR son bienvenidos! Abre un issue con tu idea o envía directamente tu pull request.

## 📜 Licencia

MIT

