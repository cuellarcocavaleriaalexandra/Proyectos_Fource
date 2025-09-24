#!/bin/bash


sudo apt update && sudo apt upgrade -y


sudo apt install -y git curl wget python3 python3-pip python3-venv golang ruby \
    build-essential libssl-dev libffi-dev zlib1g-dev libncurses-dev \
    gcc-multilib g++-multilib net-tools nmap wireshark tshark


sudo apt install -y binwalk exiftool steghide foremost john hashcat fcrackzip \
    sqlmap hydra burpsuite metasploit-framework dirb nikto netcat-traditional \
    socat tcpdump hexedit radare2 gdb


git_tools=(
    "https://github.com/rebootuser/LinEnum.git"              # LinEnum
    "https://github.com/carlospolop/PEASS-ng.git"            # PEASS-ng (LinPEAS/WinPEAS)
    "https://github.com/GTFOBins/GTFOBins.github.io.git"     # GTFOBins
    "https://github.com/mzet-/linux-exploit-suggester.git"   # Linux Exploit Suggester
    "https://github.com/danielmiessler/SecLists.git"         # SecLists (wordlists)
)

echo "[+] Clonando repositorios de GitHub..."
mkdir -p ~/Tools && cd ~/Tools
for repo in "${git_tools[@]}"; do
    git clone "$repo"
done


echo "[+] Instalando herramientas de Python..."
pip3 install --user pwntools impacket scapy requests beautifulsoup4 pycryptodome


echo "[+] Instalando herramientas de Go..."
go install github.com/OJ/gobuster/v3@latest
go install github.com/ffuf/ffuf@latest
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest


if [[ ":$PATH:" != *":$HOME/go/bin:"* ]]; then
    echo 'export PATH="$HOME/go/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
fi


echo "[+] Descargando binarios adicionales..."
wget -qO- "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.3.2_build/ghidra_10.3.2_PUBLIC_20230711.zip" | unzip -d ~/Tools/


echo -e "\n[+] Instalación completada. Herramientas disponibles en ~/Tools."
echo "[+] No olvides configurar Burp Suite, Metasploit y otras GUI manualmente."
