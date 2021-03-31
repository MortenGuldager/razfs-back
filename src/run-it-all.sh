#!/bin/bash
set -e
cd /prod/razfs-back
bin/prepare-zfs.sh
venv/bin/python bin/maintain_snapshots.py
venv/bin/python bin/main.py
