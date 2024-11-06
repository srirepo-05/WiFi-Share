import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
from pyqrcode import QRCode
import png
import os

PORT = 8010

os.environ['USERPROFILE']

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop/Notes')
os.chdir(desktop)
current_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(current_dir, './pages/index2.html')

Handler = http.server.SimpleHTTPRequestHandler
hostname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = "http://" + s.getsockname()[0] + ":" + str(PORT)
link = IP

url = pyqrcode.create(link)
qr_path=os.path.join(current_dir, './assets/myqr.svg')
url.svg(qr_path, scale=8)
webbrowser.open(index_path)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
	print("serving at port", PORT)
	print("Type this in your Browser", IP)
	print("or Use the QRCode")
	httpd.serve_forever()
