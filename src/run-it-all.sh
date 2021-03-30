#!/bin/bash
cd /prod/razfs-back
venv/bin/python bin/maintain_snapshots.py
venv/bin/python bin/main.py
