#!/usr/bin/env bash
set -e

if [[ ! "${EUID}" -eq 0 ]]; then
  echo "please run as root. exiting"
  exit
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="$(dirname "$SCRIPT_DIR")"

# Replace the source line with
source "$APP_ROOT/lib/gum_helpers.sh"

# Ensure traps are set after sourcing gum_helpers
trap 'trap_exit' EXIT
trap 'trap_error ${FUNCNAME} ${LINENO}' ERR

# Now you can use the gum functions
gum_init # Initialize gum (download if not present)

gum_title "My Script Title"
gum_info "This is an info message using gum."

if gum_confirm "Do you want to continue?"; then
    gum_green "User confirmed!"
else
    gum_warn "User did not confirm."
fi

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
pacman -Scc --noconfirm

# install pre-requisite packages
pacman -Sy --noconfirm --needed "${BOOTSTRAP_PKGS[@]}"