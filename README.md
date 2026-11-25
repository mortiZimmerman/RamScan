# 🧠 RAM Scanner

**¿Qué coño se está comiendo mi RAM?** Panel de control local, con botones físicos, que escanea tus procesos, los agrupa por aplicación y te lo enseña en el navegador. Todo corre en tu PC (`127.0.0.1`), no envía nada a internet.

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Plataformas](https://img.shields.io/badge/Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![Licencia](https://img.shields.io/badge/licencia-MIT-green)

[![Donar](https://img.shields.io/badge/💙_Donar-PayPal-0070ba)](https://paypal.me/mauortiz2002)

> **App 100% gratuita**, sin anuncios ni cuentas. Si te ha servido, puedes [invitarme a un café](https://paypal.me/mauortiz2002) (voluntario).

## ✨ Características

- 🔒 **Panel por pasos**: primero se escanea; el resto de botones se desbloquean después (luz roja → verde → ámbar).
- 🔍 Escaneo rápido y **barra visual** de uso total (verde / ámbar / rojo según el nivel).
- 🏆 **Ranking** de aplicaciones con **buscador**.
- 📁 **Agrupa por aplicación**: los 20 procesos de Brave salen como una sola fila.
- 📈 **Historial** de uso de RAM en gráfica.
- 🔄 **Tiempo real** (cada 3 s).
- ⚠️ **Alertas** cuando un programa supera X GB.
- 💀 **Detector de fugas**: avisa de apps cuya memoria sube sin parar.
- 📂 Botón **abrir ubicación** del programa.
- 📄 **Informe HTML** con mapa de consumo, categorías y diagnóstico.
- 📤 **Exportar** desde el informe a CSV (Excel), JSON, Markdown, HTML o PDF.
- ✅ Confirmación antes de cada acción.

## 🚀 Instalación

Necesitas [Python 3.8+](https://www.python.org/downloads/).

```bash
git clone https://github.com/mortiZimmerman/RamScanner.git
cd RamScanner
```

**Windows:** doble clic en `ram_scanner.bat` (instala `psutil` solo la primera vez y abre el navegador).

**macOS / Linux:**
```bash
pip install -r requirements.txt
python3 ram_scanner.py
```

Para salir, cierra la ventana negra (o `Ctrl+C`).

## 🕹️ Cómo se usa

1. **Escanear**: lee todos los procesos y desbloquea el panel.
2. **Abrir informe**: informe HTML completo en pestaña nueva.
3. **Tiempo real**: refresca cada 3 s y construye el historial.
4. **Alerta**: te avisa si una app pasa del límite en GB.
5. **Fugas**: con tiempo real activo, marca las apps que suben 30 MB o más en 6 lecturas seguidas.

> 💡 Ejecútalo como administrador (o con `sudo`) para ver todos los procesos y abrir sus ubicaciones.

## ❓ FAQ

**¿Es gratis?** Sí, totalmente gratuita y sin límites. Las donaciones por [PayPal](https://paypal.me/mauortiz2002) son voluntarias.

**¿Envía datos a internet?** No, todo corre en `127.0.0.1`.

**¿Por qué no coincide con el Administrador de tareas?** Suma la memoria residente (RSS) por aplicación; otras herramientas cuentan la memoria compartida de otra forma.

**No me abre la ubicación de un proceso.** Ejecuta el `.bat` como administrador.

## 🔐 Seguridad

El servidor escucha solo en `127.0.0.1`, rechaza peticiones con otro `Host` y exige una cabecera propia en las acciones, para que otras webs no puedan controlarlo.

## 🗺️ Roadmap

- [ ] Cerrar procesos desde el panel
- [ ] Comparar dos escaneos

## 🤝 Contribuir

¡Los PR son bienvenidos! Abre un issue con tu idea.

## 💙 Apoyo

Si RAM Scanner te ahorra tiempo, [dona por PayPal](https://paypal.me/mauortiz2002). ¡Gracias!

## 📜 Licencia

MIT
