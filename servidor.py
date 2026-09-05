#!/usr/bin/env python3
"""Servidor local para ver la plantilla.

Igual que `python3 -m http.server`, pero mandando Cache-Control: no-store en
cada respuesta. Sin eso el navegador se queda con la versión vieja de
index.html y parece que los cambios no se aplicaron — que es exactamente lo
que pasó al agregar las diapositivas nuevas.

Uso:  python3 servidor.py [puerto]     (por defecto 4180)
"""
import http.server
import pathlib
import socketserver
import sys

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 4180
RAIZ = pathlib.Path(__file__).parent


class SinCache(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(RAIZ), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, *args):
        pass  # sin ruido en la consola


with socketserver.TCPServer(("", PUERTO), SinCache) as httpd:
    print(f"Plantilla en http://localhost:{PUERTO}/  (Ctrl+C para detener)")
    httpd.serve_forever()
