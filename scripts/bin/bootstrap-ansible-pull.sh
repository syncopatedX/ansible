#!/bin/bash
set -e

# Display banner
echo "====================================="
echo "Ansible Pull Bootstrap for Workstation"
echo "====================================="

# Gather user info
echo "Gathering user information..."
CURRENT_USER=$(whoami)
USER_HOME=$(eval echo ~$CURRENT_USER)
USER_SHELL=$(getent passwd $CURRENT_USER | cut -d: -f7)

echo "User: $CURRENT_USER"
echo "Home: $USER_HOME"
echo "Shell: $USER_SHELL"

# Install prerequisites
echo "Installing prerequisites..."
sudo pacman -Sy --noconfirm --needed git ansible

# Clone repository
echo "Cloning repository..."
REPO_URL="https://github.com/b08x/ansible-workstation-arch.git"
REPO_DIR="/tmp/ansible-workstation-arch"

# Remove existing repo directory if it exists
if [ -d "$REPO_DIR" ]; then
    echo "Removing existing repository directory..."
    rm -rf "$REPO_DIR"
fi

git clone $REPO_URL $REPO_DIR

# Run ansible-pull
echo "Running ansible-pull..."
cd $REPO_DIR
ansible-pull -U $REPO_URL -i localhost, main.yml \
    -e "user_name=$CURRENT_USER" \
    -e "user_home=$USER_HOME" \
    -e "user_shell=$USER_SHELL"

echo "Setup complete!"
