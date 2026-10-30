import json,os,urllib.request
from http.server import BaseHTTPRequestHandler,HTTPServer
from readiness import readiness

def dependency_available():
    try:
        with urllib.request.urlopen("http://inventory:8080/ping",timeout=1) as r: return r.status==200
    except Exception: return False

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        if os.getenv("ROLE")=="inventory":
            code,body=(200,{"status":"available"}) if self.path=="/ping" else (404,{"error":"not found"})
        elif self.path=="/health": code,body=200,{"status":"alive"}
        elif self.path=="/ready": code,body=readiness(dependency_available)
        else: code,body=404,{"error":"not found"}
        data=json.dumps(body).encode();self.send_response(code);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(data)
print("Starting "+os.getenv("ROLE","api")+" on 8080",flush=True)
HTTPServer(("0.0.0.0",8080),Handler).serve_forever()
