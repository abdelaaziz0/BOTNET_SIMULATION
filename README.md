# 🌐 Botnet Simulation Framework

Un framework Python pour simuler un réseau de botnets dans un environnement contrôlé, à des fins éducatives et de recherche en cybersécurité.

## ⚠️ Avertissement

**Ce projet est fourni UNIQUEMENT à des fins éducatives et de recherche en sécurité dans un environnement isolé et contrôlé.**

N'utilisez ce code en aucun cas sur des réseaux ou systèmes sans autorisation explicite préalable. L'utilisation de ce code sur des systèmes réels sans autorisation est illégale et contraire à l'éthique.

## 📋 Présentation

Ce projet simule un réseau de botnets avec un serveur de commande et contrôle (C&C) et des clients bots. Il permet d'explorer et de comprendre les mécanismes de fonctionnement d'un botnet dans un environnement sécurisé.

### Fonctionnalités principales

- **Serveur C&C** : Accepte des connexions entrantes et attribue un identifiant à chaque bot
- **Bots clients** : Se connectent au serveur et exécutent les commandes reçues
- **Système de commandes** : Permet d'envoyer des instructions à tous les bots ou à un bot spécifique
- **Simulations** : Inclut des simulations de ping, d'attaques par raw sockets et de commandes SSH via Paramiko

## 🔧 Prérequis

- Python 3.6+
- Modules Python : paramiko, socket, threading, argparse

## 📦 Installation

```bash
# Cloner le repository
git clone https://github.com/abdelaaziz0/BOTNET_SIMULATION.git
cd botnet-simulation

# Installer les dépendances
pip install paramiko
```

## 🚀 Utilisation

Le script peut être lancé en mode serveur ou en mode bot :

### Mode serveur C&C

```bash
python botnet_sim.py server --host 127.0.0.1 --port 9999
```

### Mode bot client

```bash
python botnet_sim.py bot --host 127.0.0.1 --port 9999
```

## 💻 Commandes disponibles

### Commandes du serveur C&C

- `broadcast <commande>` : Envoie une commande à tous les bots connectés
- `send <bot_id> <commande>` : Envoie une commande à un bot spécifique

### Commandes supportées par les bots

- `ping` : Le bot répond avec "pong"
- `raw_attack` : Simule une attaque via raw sockets
- `ssh <commande>` : Simule l'exécution d'une commande SSH via Paramiko
- Toute autre commande : Retourne un message générique de confirmation

## 🔍 Architecture

Le projet se compose de deux classes principales :

### CommandAndControlServer

Gère les connexions entrantes des bots, attribue des identifiants et fournit une interface pour envoyer des commandes.

Caractéristiques :
- Gestion multi-thread des connexions
- Système de verrouillage pour éviter les problèmes de concurrence
- Interface en ligne de commande pour le contrôle

### BotClient

Simule le comportement d'un bot dans un botnet.

Caractéristiques :
- Connexion automatique au serveur C&C
- Envoi périodique de heartbeat
- Exécution de commandes simulées

## 🛠️ Personnalisation

Vous pouvez enrichir ce projet en ajoutant :

- Chiffrement des communications
- Mécanismes d'authentification
- Persistance des connexions
- Techniques d'évasion simulées
- Interface graphique pour le contrôle des bots
- Système de logs avancé

## 📚 Applications pédagogiques

Ce projet peut être utilisé pour :

- Comprendre les mécanismes de commande et contrôle dans les botnets
- Étudier les techniques de persistance et de communication
- Développer des méthodes de détection
- Former aux techniques de réponse aux incidents

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à soumettre des pull requests ou à ouvrir des issues pour améliorer le projet.

## 📝 Auteurs

- BELKHAIR Abdelaaziz - Développement initial
