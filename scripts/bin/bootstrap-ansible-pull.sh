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
BOOTSTRAP_PKGS=(
  'ansible'
  'aria2'
  'base-devel'
  'bc'
  'ccache'
  'cmake'
  'fd'
  'dialog'
  'git'
  'git-lfs'
  'gum'
  'htop'
  'neovim'
  'net-tools'
  'openssh'
  'python-pip'
  'reflector'
  'ruby-bundler'
  'rubygems'
  'rust'
  'unzip'
  'wget'
  'zsh'
)

# clean cache
sudo pacman -Scc --noconfirm

# install pre-requisite packages
sudo pacman -Sy --noconfirm --needed "${BOOTSTRAP_PKGS[@]}"

REPO_URL="https://gitlab.com/syncopatedx/syncopated-ansible.git"

# Run ansible-pull
echo "Running ansible-pull..."

ansible-pull -U $REPO_URL -i localhost, main.yml \
    -e "user_name=$CURRENT_USER" \
    -e "user_home=$USER_HOME" \
    -e "user_shell=$USER_SHELL"

echo "Setup complete!"
