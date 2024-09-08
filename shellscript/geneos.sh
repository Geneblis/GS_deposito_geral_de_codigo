#!/bin/bash

# Default packages are for the configuration and corresponding .config folders
# Install packages after installing base Debian with no GUI

# xorg display server installation
sudo apt install -y xorg xbacklight xbindkeys xvkbd xinput

# Build-essential.
sudo apt install -y build-essential 
sudo apt install -y wget

# Microcode for Intel/AMD 
sudo apt install -y amd64-microcode
#sudo apt install -y intel-microcode 

# Browser Installation
sudo apt update && sudo apt install -y wget gnupg lsb-release apt-transport-https ca-certificates

distro=$(if echo " una bookworm vanessa focal jammy bullseye vera uma " | grep -q " $(lsb_release -sc) "; then echo $(lsb_release -sc); else echo focal; fi)

wget -O- https://deb.librewolf.net/keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/librewolf.gpg

sudo tee /etc/apt/sources.list.d/librewolf.sources << EOF > /dev/null
Types: deb
URIs: https://deb.librewolf.net
Suites: $distro
Components: main
Architectures: amd64
Signed-By: /usr/share/keyrings/librewolf.gpg
EOF

sudo apt update

sudo apt install librewolf -y

# Network File Tools/System Events
sudo apt install -y dialog mtools acpi acpid gvfs-backends

sudo systemctl enable avahi-daemon
sudo systemctl enable acpid

# Sound packages (pulseaudio installed prior)
sudo apt install -y alsa-utils volumeicon-alsa

# Neofetch/HTOP
sudo apt install -y neofetch btop

# Command line text editor
sudo apt install -y code

# Install fonts
sudo apt install fonts-font-awesome fonts-powerline fonts-liberation2 fonts-liberation fonts-terminus


# Install LightDM GTK Greeter Settings (lightdm,lightdm-gtk-greeter installs with xfce)

sudo apt install -y lightdm-gtk-greeter-settings
sudo systemctl enable lightdm

sudo apt autoremove

printf "\e[1;32mYou can Reboot!//Voce pode reniciar!\e[0m\n"
