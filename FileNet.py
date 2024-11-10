
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import socket
import io
import base64
import uuid
import webbrowser
import time
import qrcode
import os
import threading
import sys
import signal

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Add a shutdown event
shutdown_event = threading.Event()
server = None

# Get the base directory for the executable
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    default_share_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'Share-Folder')
    if not os.path.exists(default_share_folder):
        os.makedirs(default_share_folder)
    SHARED_FOLDER = default_share_folder
else:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SHARED_FOLDER = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Share-Folder')

app.template_folder = os.path.join(base_dir, 'templates')

MOBILE_TOKENS = {}
USERS = {
    'sriram': generate_password_hash('snucse')
}

def shutdown_server():
    """Shutdown the Flask server"""
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()

@app.route('/shutdown', methods=['POST'])


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
        s.close()
        return IP
    except Exception:
        return '127.0.0.1'

def open_browser():
    try:
        time.sleep(1.5)
        local_ip = get_local_ip()
        webbrowser.open(f'http://{local_ip}:5000/login')
    except Exception as e:
        print(f"Error opening browser: {e}")

# Update the login_required decorator (no changes needed, included for completeness)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        if token and token in MOBILE_TOKENS:
            return f(*args, **kwargs)
        
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@login_required
def shutdown():
    """Endpoint to shutdown the server"""
    try:
        shutdown_event.set()
        shutdown_server()
        return 'Server shutting down...'
    except Exception as e:
        print(f"Error during shutdown: {e}")
        return 'Error during shutdown', 500

def format_size(size_in_bytes):
    try:
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < 1024 * 1024:
            return f"{size_in_bytes/1024:.2f} KB"
        else:
            return f"{size_in_bytes/1024/1024:.2f} MB"
    except Exception:
        return "0 B"

@app.route('/')
@login_required
def index():
    try:
        token = str(uuid.uuid4())
        MOBILE_TOKENS[token] = True
        
        local_ip = get_local_ip()
        qr_data = f'http://{local_ip}:5000/files?token={token}'
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return render_template('index.html', qr_code=qr_base64)
    except Exception as e:
        print(f"Error in index route: {e}")
        return "An error occurred", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            if username in USERS and check_password_hash(USERS[username], password):
                session['logged_in'] = True
                return redirect(url_for('index'))
            return render_template('login.html', error='Invalid credentials')
        
        return render_template('login.html')
    except Exception as e:
        print(f"Error in login route: {e}")
        return "An error occurred", 500

@app.route('/files')
@login_required
def list_files():
    try:
        if not os.path.exists(SHARED_FOLDER):
            os.makedirs(SHARED_FOLDER)
            
        files = []
        for filename in os.listdir(SHARED_FOLDER):
            try:
                path = os.path.join(SHARED_FOLDER, filename)
                size = os.path.getsize(path) if os.path.exists(path) else 0
                files.append({
                    'name': filename,
                    'size': format_size(size),
                    'type': 'Directory' if os.path.isdir(path) else 'File'
                })
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue

        token = request.args.get('token', '')
        return render_template('files.html', files=files, token=token)
    except Exception as e:
        print(f"Error in list_files route: {e}")
        return "An error occurred", 500

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    try:
        file_path = os.path.join(SHARED_FOLDER, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        return "File not found", 404
    except Exception as e:
        print(f"Error in download route: {e}")
        return "An error occurred", 500

@app.route('/logout')
def logout():
    try:
        token = request.args.get('token')
        if token and token in MOBILE_TOKENS:
            del MOBILE_TOKENS[token]
        
        session.pop('logged_in', None)
        return redirect(url_for('login'))
    except Exception as e:
        print(f"Error in logout route: {e}")
        return "An error occurred", 500

def run_app():
    try:
        threading.Thread(target=open_browser, daemon=True).start()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting the application: {e}")
        
def signal_handler(signum, frame):
    print("Received shutdown signal")
    shutdown_event.set()
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    run_app()    
    

