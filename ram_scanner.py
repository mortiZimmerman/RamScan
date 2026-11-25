#!/usr/bin/env python3
"""RAM Scanner · descubre qué se está comiendo tu memoria y genera un informe HTML/JSON/CSV."""
import argparse, csv, json, os, platform, socket, time, webbrowser
from collections import defaultdict
from datetime import datetime
import psutil

CATS = {
    "Navegadores": ("chrome", "firefox", "msedge", "edge", "brave", "opera", "safari", "vivaldi"),
    "Desarrollo": ("code", "python", "node", "java", "docker", "idea", "pycharm", "studio", "git", "vmmem", "wsl"),
    "Comunicación": ("slack", "discord", "teams", "zoom", "telegram", "whatsapp", "skype"),
    "Multimedia y juegos": ("spotify", "vlc", "steam", "obs", "epic", "premiere", "photoshop", "game"),
    "Sistema": ("system", "svchost", "kernel", "systemd", "launchd", "dwm", "explorer", "windowserver",
                "finder", "gnome", "kwin", "xorg", "wayland"),
}


def categorize(name):
    n = name.lower()
    return next((c for c, keys in CATS.items() if any(k in n for k in keys)), "Otros")


def scan():
    groups = defaultdict(lambda: {"mb": 0.0, "pids": [], "cmd": "", "user": ""})
    for p in psutil.process_iter(["pid", "name", "memory_info", "username", "cmdline"]):
        try:
            mi = p.info["memory_info"]
            if not mi:
                continue
            g = groups[p.info["name"] or "?"]
            g["mb"] += mi.rss / 2**20
            g["pids"].append(p.info["pid"])
            g["user"] = p.info["username"] or ""
            g["cmd"] = " ".join(p.info["cmdline"] or [])[:200]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    apps = [{"name": k, "mb": round(v["mb"], 1), "count": len(v["pids"]), "pids": v["pids"][:40],
             "user": v["user"], "cmd": v["cmd"], "cat": categorize(k)} for k, v in groups.items()]
    apps.sort(key=lambda a: -a["mb"])
    vm, sw = psutil.virtual_memory(), psutil.swap_memory()
    mb = lambda b: round(b / 2**20)
    return {"host": socket.gethostname(), "os": platform.platform(),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": mb(vm.total), "used": mb(vm.total - vm.available), "free": mb(vm.available),
            "swap_used": mb(sw.used), "swap_total": mb(sw.total), "apps": apps}


def watch(seconds):
    """Toma dos fotos separadas en el tiempo y marca quién crece (posibles fugas de memoria)."""
    first = scan()
    print(f"Vigilando {seconds}s para detectar fugas de memoria...")
    time.sleep(seconds)
    data = scan()
    base = {a["name"]: a["mb"] for a in first["apps"]}
    for a in data["apps"]:
        a["growth"] = round(a["mb"] - base.get(a["name"], a["mb"]), 1)
    return data


def export(data, path, fmt):
    if fmt == "json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    elif fmt == "csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["aplicacion", "categoria", "procesos", "ram_mb", "usuario", "pids"])
            for a in data["apps"]:
                w.writerow([a["name"], a["cat"], a["count"], a["mb"], a["user"], " ".join(map(str, a["pids"]))])
    else:
        tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_template.html"),
                   encoding="utf-8").read()
        payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        with open(path, "w", encoding="utf-8") as f:
            f.write(tpl.replace("__DATA__", payload))


def main():
    ap = argparse.ArgumentParser(description="RAM Scanner: ¿qué coño consume mi RAM?")
    ap.add_argument("-o", "--output", default="ram_report.html", help="archivo de salida (.html, .json o .csv)")
    ap.add_argument("--top", type=int, default=0, help="guardar solo las N apps que más consumen")
    ap.add_argument("-w", "--watch", type=int, metavar="SEG", help="vigilar SEG segundos y detectar fugas")
    ap.add_argument("--open", action="store_true", help="abrir el informe al terminar")
    a = ap.parse_args()

    data = watch(a.watch) if a.watch else scan()
    if a.top:
        data["apps"] = data["apps"][:a.top]
    fmt = os.path.splitext(a.output)[1].lstrip(".").lower() or "html"
    export(data, a.output, fmt if fmt in ("json", "csv") else "html")

    print(f"\nRAM: {data['used']} / {data['total']} MB en uso\n")
    for x in data["apps"][:10]:
        print(f"  {x['mb']:>9.1f} MB  {x['count']:>3} proc.  {x['name']}")
    print(f"\nInforme guardado en {os.path.abspath(a.output)}")
    if a.open:
        webbrowser.open("file://" + os.path.abspath(a.output))


if __name__ == "__main__":
    main()
#meowwww :))))