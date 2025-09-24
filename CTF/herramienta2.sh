#!/bin/bash

# --- Configuración inicial ---
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget python3 python3-pip python3-venv golang ruby \
    build-essential libssl-dev libffi-dev zlib1g-dev libncurses-dev \
    gcc-multilib g++-multilib net-tools nmap wireshark tshark

# --- Herramientas clásicas de CTF ---
sudo apt install -y binwalk exiftool steghide foremost john hashcat fcrackzip \
    sqlmap hydra burpsuite metasploit-framework dirb nikto netcat-traditional \
    socat tcpdump hexedit radare2 gdb

# --- Herramientas desde GitHub ---
echo "[+] Clonando repositorios de GitHub..."
mkdir -p ~/Tools && cd ~/Tools

git_tools=(
    "https://github.com/rebootuser/LinEnum.git"              # LinEnum
    "https://github.com/carlospolop/PEASS-ng.git"           # PEASS-ng (LinPEAS/WinPEAS)
    "https://github.com/GTFOBins/GTFOBins.github.io.git"     # GTFOBins
    "https://github.com/mzet-/linux-exploit-suggester.git"   # Linux Exploit Suggester
    "https://github.com/danielmiessler/SecLists.git"         # SecLists
    "https://github.com/maurosoria/dirsearch.git"            # Dirsearch (añadido)
    "https://github.com/Josue87/MailFinder.git"              # MailFinder (añadido)
    "https://github.com/p1ngul1n0/yesitsme.git"             # yesitsme (añadido)
)

for repo in "${git_tools[@]}"; do
    git clone "$repo"
done

# --- Instalar herramientas de Python ---
pip3 install --user pwntools impacket scapy requests beautifulsoup4 pycryptodome

# --- Instalar herramientas de Go ---
go_tools=(
    "github.com/OJ/gobuster/v3@latest"
    "github.com/ffuf/ffuf@latest"
    "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"
    "github.com/projectdiscovery/httpx/cmd/httpx@latest"     # Para reversely.ia (HTTP analysis)
)

for tool in "${go_tools[@]}"; do
    go install "$tool"
done

# --- Añadir ~/go/bin al PATH ---
if [[ ":$PATH:" != *":$HOME/go/bin:"* ]]; then
    echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
fi

# --- Herramientas adicionales (binarios/scripts) ---
echo "[+] Configurando herramientas adicionales..."
# Instalar dirsearch (ya clonado, pero se puede instalar dependencias)
cd ~/Tools/dirsearch && pip3 install -r requirements.txt

# Instalar MailFinder (requiere Node.js)
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt install -y nodejs
fi
cd ~/Tools/MailFinder && npm install

# Instalar yesitsme (Python)
cd ~/Tools/yesitsme && pip3 install -r requirements.txt

# --- Crear archivo tools_info.txt con información ---
echo "[+] Creando archivo tools_info.txt..."
cat > ~/Tools/tools_info.txt << 'EOF'
=== CTF Tools Info ===
- Dirsearch: ~/Tools/dirsearch/dirsearch.py (Uso: python3 dirsearch.py -u <URL> -e <EXTENSIONES>)
- MailFinder: ~/Tools/MailFinder (Uso: node MailFinder.js -d <DOMINIO>)
- yesitsme: ~/Tools/yesitsme/yesitsme.py (Uso: python3 yesitsme.py -h)
- Reversely.ia: Herramienta online para análisis inverso (https://reversely.ia)
- Nuclei: Escaneo de vulnerabilidades (Uso: nuclei -u <URL>)
- SecLists: Wordlists en ~/Tools/SecLists/
EOF

# --- Descargar Ghidra (opcional) ---
read -p "[?] ¿Descargar Ghidra? (y/n): " choice
if [[ "$choice" =~ [yY] ]]; then
    wget -qO- "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.3.2_build/ghidra_10.3.2_PUBLIC_20230711.zip" | unzip -d ~/Tools/
    echo "Ghidra: ~/Tools/ghidra_10.3.2_PUBLIC/" >> ~/Tools/tools_info.txt
fi

# --- Mensaje final ---
echo -e "\n[+] ¡Instalación completada!"
echo -e "[+] Todas las herramientas están en ~/Tools/"
echo -e "[+] Revisa ~/Tools/tools_info.txt para instrucciones de uso.\n"
