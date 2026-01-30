"""
Vercel serverless handler: barcha so'rovlarni Django WSGI ga yo'naltiradi.
"""
import io
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote

# Loyiha rootini path ga qo'shamiz (api/ ning bir ust darajasi)
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")

from django.core.wsgi import get_wsgi_application

_application = get_wsgi_application()


def _make_environ(handler):
    """BaseHTTPRequestHandler dan WSGI environ quriladi."""
    path = handler.path
    if "?" in path:
        path_info, query_string = path.split("?", 1)
    else:
        path_info, query_string = path, ""
    path_info = unquote(path_info)

    content_length = handler.headers.get("Content-Length", "").strip()
    content_length = int(content_length) if content_length else 0
    body = handler.rfile.read(content_length) if content_length else b""

    environ = {
        "REQUEST_METHOD": handler.command,
        "SCRIPT_NAME": "",
        "PATH_INFO": path_info or "/",
        "QUERY_STRING": query_string,
        "CONTENT_TYPE": handler.headers.get("Content-Type", ""),
        "CONTENT_LENGTH": str(content_length),
        "wsgi.input": io.BytesIO(body),
        "wsgi.errors": sys.stderr,
        "wsgi.version": (1, 0),
        "wsgi.run_once": True,
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.url_scheme": "https",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "443",
        "SERVER_PROTOCOL": "HTTP/1.1",
    }
    for key, value in handler.headers.items():
        key = "HTTP_" + key.upper().replace("-", "_")
        environ[key] = value
    return environ


def _handle_request(handler):
    """WSGI app ni chaqiradi va javobni handler orqali yozadi."""
    status_headers = [None, None]

    def start_response(status, response_headers, exc_info=None):
        status_headers[0] = status
        status_headers[1] = response_headers

    environ = _make_environ(handler)
    result = _application(environ, start_response)
    status = status_headers[0]
    response_headers = status_headers[1]

    # Status: "200 OK" -> code 200
    status_code = int(status.split()[0]) if status else 200
    handler.send_response(status_code)
    for name, value in response_headers:
        handler.send_header(name, value)
    handler.end_headers()
    for chunk in result:
        if chunk:
            handler.wfile.write(chunk)
    if hasattr(result, "close"):
        result.close()


class handler(BaseHTTPRequestHandler):
    """Vercel: barcha so'rovlar Django WSGI ga uzatiladi."""

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        _handle_request(self)

    def do_POST(self):
        _handle_request(self)

    def do_HEAD(self):
        _handle_request(self)

    def do_PUT(self):
        _handle_request(self)

    def do_DELETE(self):
        _handle_request(self)

    def do_PATCH(self):
        _handle_request(self)

    def do_OPTIONS(self):
        _handle_request(self)
