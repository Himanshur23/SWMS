#!/bin/bash
set -euo pipefail

# Install Rust
curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable
source $HOME/.cargo/env

# Build your project
pip install -r requirements.txt
python main.py