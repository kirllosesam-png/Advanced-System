import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

HTML = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>Krollos Control Panel</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { background: #000; color: #0f0; text-align: center; font-family: monospace; }
        .box { display: flex; justify-content: space-around; margin-top: 20px; }
        img { width: 45%; border: 2px solid #0f0; border-radius: 10px; background: #111; }
    </style>
</head>
<body>
    <h1>🚀 Krollos Live Dashboard</h1>
    <p id="status">🔴 Offline</p>
    <div class="box">
        <div><h3>Camera</h3><img id="cam" src=""></div>
        <div><h3>Screen</h3><img id="scr" src=""></div>
    </div>
    <script>
        var socket = io();
        socket.on('connect', () => document.getElementById('status').innerText = "🟢 Online");
        socket.on('v_frame', (d) => document.getElementById('cam').src = 'data:image/jpeg;base64,' + d);
        socket.on('s_frame', (d) => document.getElementById('scr').src = 'data:image/jpeg;base64,' + d);
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@socketio.on('v_frame')
def v(d): emit('v_frame', d, broadcast=True)

@socketio.on('s_frame')
def s(d): emit('s_frame', d, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
  
