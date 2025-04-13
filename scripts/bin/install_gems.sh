#!/usr/bin/env bash

INSTALLED_GEMS=$(gem list | awk '{ print $1 }')

GEMS=(
  'activesupport'
  'algorithms'
  'amazing_print'
  'awesome_print'
  'bcrypt_pbkdf'
  'childprocess'
  'dotenv'
  'ed25519'
  'eventmachine'
  'ffi'
  'fractional'
  'geo_coord'
  'google_custom_search_api'
  'highline'
  'i18n'
  'i3ipc'
  'jongleur'
  'json'
  'jsonl'
  'kramdown'
  'langchainrb'
  'lingua'
  'logging'
  'mimemagic'
  'minitest'
  'mocha'
  'multi_json'
  'net-ssh'
  'numpy'
  'ohm-contrib'
  'ohm'
  'open3'
  'open4'
  'parallel'
  'pastel'
  'pg'
  'pry-doc'
  'pry'
  'psych'
  'pycall'
  'rake'
  'rdoc'
  'redis-namespace'
  'redis'
  'rexml'
  'rouge'
  'ruby-lsp'
  'rugged'
  'sequel'
  'solargraph'
  'sync'
  'sys-proctable'
  'timeout'
  'treetop'
  'tty-box'
  'tty-command'
  'tty-cursor'
  'tty-markdown'
  'tty-progressbar'
  'tty-prompt'
  'tty-screen'
  'tty-spinner'
  'tty-table'
  'tty-tree'
)

# https://stackoverflow.com/a/42399479
mapfile -t DIFF < \
    <(comm -23 \
        <(IFS=$'\n'; echo "${GEMS[*]}" | sort) \
        <(IFS=$'\n'; echo "${INSTALLED_GEMS[*]}" | sort) \
    )

for gem in "${DIFF[@]}"; do
  gem install "$gem" || continue
done