#!/usr/bin/env python3
# File name: kali_sender.py
# Fixed version

import socket
import time

def main():
    print("""
╔══════════════════════════════════════╗
║        KALI PASSWORD SENDER          ║
║        (HasnainDarkNet)               ║
╚══════════════════════════════════════╝
    """)
    
    ip = input("[*] Windows IP: ")
    port = 4444
    
    while True:
        try:
            pwd = input("\n[hasnain] Enter New password (or 'quit'): ").strip()
            
            if pwd.lower() == 'quit':
                break
            
            if pwd:
                print(f"[*] Connecting to {ip}:{port}...")
                
                # Create socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((ip, port))
                
                print("[✓] Connected to Windows!")
                
                # Send password
                s.send(pwd.encode())
                print(f"[✓] Password sent: {pwd}")
                
                # Receive response
                response = s.recv(1024).decode()
                print(f"[Windows] {response}")
                
                s.close()
                
        except ConnectionRefusedError:
            print("[!] Connection refused! Windows Script Run?")
        except TimeoutError:
            print("[!] Connection timeout!")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
