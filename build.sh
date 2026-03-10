#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python generate_data.py
python train_model.py
