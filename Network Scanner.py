import socket
import threading
from queue import Queue

# ========= Einstellungen =========
target = input("Gib die IP-Adresse des Netzwerks ein (z.B. 192.168.1.1): ")
ip_parts = target.split('.')[:-1]
base_ip = '.'.join(ip_parts) + '.'

# Port, um Geräte zu testen (z.B. Port 80 = HTTP)
port = 80

# Thread-Queue für gleichzeitiges Scannen
q = Queue()
active_hosts = []


def scan(ip):
    """Versucht, eine Verbindung zum angegebenen IP-Port herzustellen."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"[+] Gerät gefunden: {ip}")
            active_hosts.append(ip)
        sock.close()
    except Exception:
        pass


def threader():
    while True:
        worker = q.get()
        scan(worker)
        q.task_done()


# ========= Threads erstellen =========
for x in range(30):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# ========= IPs in Queue hinzufügen =========
for i in range(1, 255):
    ip = base_ip + str(i)
    q.put(ip)

q.join()

print("\n===== Scan abgeschlossen =====")
if active_hosts:
    for device in active_hosts:
        try:
            hostname = socket.gethostbyaddr(device)
            print(f"{device} → {hostname[0]}")
        except:
            print(device)
else:
    print("Keine Geräte gefunden.")
