#!/bin/bash

# Define paths
INSTALL_DIR="$HOME/.gitgate"
BIN_DIR="/usr/local/bin"

echo "🟠 Installing gitGate..."

# 1. Create directory structures
mkdir -p "$INSTALL_DIR"

# 2. Pull down files from your online repository (Replace URLs with your actual repository raw layout)
# curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/gitgate.py -o "$INSTALL_DIR/gitgate.py"
# curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/review_rules.md -o "$INSTALL_DIR/review_rules.md"

# 3. Create a clean system-wide executable shortcut link
cat << 'EOF' > "$INSTALL_DIR/gitgate-runner"
#!/bin/bash
python3 "$HOME/.gitgate/gitgate.py" "$@"
EOF

chmod +x "$INSTALL_DIR/gitgate-runner"

# Link to local path bin executable environment
sudo ln -sf "$INSTALL_DIR/gitgate-runner" "$BIN_DIR/gitgate"

echo "✔ gitGate installed successfully! Run it using the command: gitgate"