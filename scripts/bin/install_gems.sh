#!/usr/bin/env bash

sudo gem update --system 3.6.9

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
  'google-cloud-translate'
  'highline'
  'i18n'
  'i3ipc'
  'jongleur'
  'json'
  'jsonl'
  'hashie'
  'kramdown'
  'langchainrb'
  'lingua'
  'logging'
  'jongleur'
  'mimemagic'
  'minitest'
  'mocha'
  'multi_json'
  'net-ssh'
  'numpy'
  'langchain'
  'lingua'
  'ohm-contrib'
  'ohm'
  'open3'
  'open4'
  'parallel'
  'pastel'
  'pg'
  'pgvector'
  'pry-doc'
  'pry'
  'psych'
  'pycall'
  'pragmatic_segmenter'
  'pragmatic_tokenizer'
  'rake'
  'rdoc'
  'redis-namespace'
  'redis'
  'rexml'
  'rouge'
  'ruby-lsp'
  'ruby_llm'
  'ruby-spacy'
  'rugged'
  'sequel'
  'solargraph'
  'sync'
  'sys-proctable'
  'timeout'
  'treetop'
  'tty-box'
  'tty-command'
  'tty-config'
  'tty-editor'
  'tty-exit'
  'tty-file'
  'tty-font'
  'tty-link'
  'tty-logger'
  'tty-markdown'
  'tty-option'
  'tty-prompt'
  'tty-screen'
  'tty-spinner'
  'tty-table'
  
)

# https://stackoverflow.com/a/42399479
mapfile -t DIFF < \
    <(comm -23 \
        <(IFS=$'\n'; echo "${GEMS[*]}" | sort) \
        <(IFS=$'\n'; echo "${INSTALLED_GEMS[*]}" | sort) \
    )

for gem in "${DIFF[@]}"; do
  gem install --user-install "$gem" || continue
done
