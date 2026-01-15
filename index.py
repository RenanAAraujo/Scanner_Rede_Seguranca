import socket
import datetime
import platform
import subprocess
import json

class NetworkScanner:
    """
    Uma ferramenta de automação em Python para auditar dispositivos na rede local.
    Demonstra conhecimentos em Sockets, subprocessos e manipulação de dados.
    """
    
    def __init__(self):
        self.host_name = socket.gethostname()
        self.local_ip = socket.gethostbyname(self.host_name)
        self.os_info = platform.system()

    def ping_device(self, ip):
        """Verifica se um dispositivo está ativo na rede."""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip]
        return subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def scan_ports(self, ip, ports):
        """Verifica portas específicas para identificar serviços ativos."""
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports

    def run_audit(self, target_range):
        """Executa a auditoria completa em um intervalo de IPs."""
        print(f"Iniciando Auditoria de Rede em: {target_range}")
        print(f"Sistema Operacional do Host: {self.os_info}")
        print("-" * 50)
        
        report = {
            "timestamp": str(datetime.datetime.now()),
            "devices_found": []
        }

        # Exemplo simplificado para varredura de um intervalo (ex: final .1 a .10)
        base_ip = ".".join(self.local_ip.split('.')[:-1])
        for i in range(1, 10):
            ip = f"{base_ip}.{i}"
            if self.ping_device(ip):
                print(f"[+] Dispositivo encontrado: {ip}")
                # Portas comuns: 80 (HTTP), 443 (HTTPS), 21 (FTP), 22 (SSH), 3306 (MySQL)
                found_ports = self.scan_ports(ip, [21, 22, 80, 443, 3306])
                
                device_data = {
                    "ip": ip,
                    "status": "Online",
                    "open_ports": found_ports
                }
                report["devices_found"].append(device_data)
        
        # Salva o relatório em JSON (Automação de relatórios)
        with open("network_report.json", "w") as f:
            json.dump(report, f, indent=4)
        
        print("-" * 50)
        print("Auditoria finalizada. Relatório 'network_report.json' gerado.")

if __name__ == "__main__":
    scanner = NetworkScanner()
    scanner.run_audit("Rede Local")