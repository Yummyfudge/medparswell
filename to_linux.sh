#!/bin/bash

# Description: Sync medparswell project to Linux dev box using rsync
# Requires SSH key-based auth set up between Mac and Linux box

RSYNC="/opt/homebrew/bin/rsync"  # Explicit modern rsync path
SRC_DIR="$HOME/Projects/medparswell/"
DEST_HOST="192.168.1.172"
DEST_DIR="/home/joe/projects/medparswell"
SSH_USER="joe"

echo "Starting rsync from $SRC_DIR to $SSH_USER@$DEST_HOST:$DEST_DIR"
"$RSYNC" -az --delete --info=progress2 --no-compress --exclude='.git/' \
  -e "ssh -T -c aes128-gcm@openssh.com -o Compression=no -x" \
  --rsync-path="ionice -c2 -n7 rsync" \
  --human-readable --partial --inplace --whole-file \
  --compress-level=0 --checksum \
  --progress \
  "$SRC_DIR" "$SSH_USER@$DEST_HOST:$DEST_DIR"

echo "Sync completed successfully."