#!/usr/bin/env python3
"""RAM Scanner · panel de control local para ver qué consume tu RAM."""
import json, os, platform, socket, subprocess, sys, threading, webbrowser
from collections import defaultdict, deque
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import psutil

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))
CATS = {
    "Navegadores": ("chrome", "firefox", "msedge", "edge", "brave", "opera", "safari", "vivaldi"),
    "Desarrollo": ("code", "python", "node", "java", "docker", "idea", "pycharm", "studio", "git", "vmmem", "wsl"),
    "Comunicación": ("slack", "discord", "teams", "zoom", "telegram", "whatsapp", "skype"),
    "Multimedia y juegos": ("spotify", "vlc", "steam", "obs", "epic", "premiere", "photoshop", "game"),
    "Sistema": ("system", "svchost", "kernel", "systemd", "launchd", "dwm", "explorer", "windowserver",
                "finder", "gnome", "kwin", "xorg", "wayland"),
}
HIST = deque(maxlen=120)                       # historial de RAM total en uso
APPH = defaultdict(lambda: deque(maxlen=20))   # historial por aplicación (para fugas)
STATE = {"data": None}


def categorize(name):
    n = name.lower()
    return next((c for c, keys in CATS.items() if any(k in n for k in keys)), "Otros")


def scan():
    groups = defaultdict(lambda: {"mb": 0.0, "pids": [], "user": ""})
    for p in psutil.process_iter(["pid", "name", "memory_info", "username"]):
        try:
            mi = p.info["memory_info"]
            if not mi:
                continue
            g = groups[p.info["name"] or "?"]
            g["mb"] += mi.rss / 2**20
            g["pids"].append(p.info["pid"])
            g["user"] = p.info["username"] or ""
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    apps = [{"name": k, "mb": round(v["mb"], 1), "count": len(v["pids"]), "pids": v["pids"][:40],
             "user": v["user"], "cmd": "", "cat": categorize(k)} for k, v in groups.items()]
    apps.sort(key=lambda a: -a["mb"])
    vm, sw = psutil.virtual_memory(), psutil.swap_memory()
    mb = lambda b: round(b / 2**20)
    return {"host": socket.gethostname(), "os": platform.platform(),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": mb(vm.total), "used": mb(vm.total - vm.available), "free": mb(vm.available),
            "swap_used": mb(sw.used), "swap_total": mb(sw.total), "apps": apps}


def snap():
    """Escanea, guarda historial y marca apps cuya RAM sube sin parar (posibles fugas)."""
    d = scan()
    HIST.append([d["time"][11:], d["used"]])
    leaks = []
    for a in d["apps"]:
        h = APPH[a["name"]]
        h.append(a["mb"])
        w = list(h)[-6:]
        if len(w) == 6 and all(w[i + 1] - w[i] >= -1 for i in range(5)) and w[-1] - w[0] >= 30:
            leaks.append({"name": a["name"], "growth": round(w[-1] - w[0], 1), "mb": a["mb"]})
    d["leaks"], d["history"] = leaks, list(HIST)
    STATE["data"] = d
    return d


def locate(path):
    if sys.platform == "win32":
        subprocess.Popen(["explorer", f"/select,{path}"])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", "-R", path])
    else:
        subprocess.Popen(["xdg-open", os.path.dirname(path)])


def read(name):
    with open(os.path.join(DIR, name), encoding="utf-8") as f:
        return f.read()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def allowed(self):  # solo desde esta máquina (evita ataques por DNS rebinding)
        return self.headers.get("Host") in (f"127.0.0.1:{PORT}", f"localhost:{PORT}")

    def send(self, body, ctype="application/json", code=200):
        b = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if not self.allowed():
            return self.send("forbidden", "text/plain", 403)
        if self.path == "/":
            return self.send(read("panel.html"), "text/html")
        if self.path == "/report":
            payload = json.dumps(STATE["data"] or snap(), ensure_ascii=False).replace("</", "<\\/")
            return self.send(read("report_template.html").replace("__DATA__", payload), "text/html")
        self.send("not found", "text/plain", 404)

    def do_POST(self):
        if not self.allowed() or self.headers.get("X-RS") != "1":
            return self.send("forbidden", "text/plain", 403)
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/api/scan":
            return self.send(json.dumps(snap()))
        if self.path == "/api/locate" and STATE["data"]:
            try:
                locate(psutil.Process(int(body["pid"])).exe())
                return self.send('{"ok":true}')
            except Exception as e:
                return self.send(json.dumps({"ok": False, "error": str(e)}), code=400)
        self.send("{}", code=404)


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://127.0.0.1:{PORT}"
    print(f"RAM Scanner funcionando en {url}\nCierra esta ventana (o Ctrl+C) para salir.")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
