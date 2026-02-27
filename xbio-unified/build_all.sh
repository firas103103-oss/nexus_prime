#!/bin/bash
set -e
cd "$(dirname "$0")"
echo "Building X-BIO firmware..."
export PATH="$HOME/.local/bin:$PATH"
pio run -e esp32s3_omega_wifi
pio run -e esp32s3_first_breath
echo "Done."
