#!/bin/bash
# install.sh - AI Bug Buster v2 Installer

echo "🚀 Installing AI Bug Buster v2..."

# 1. Install dependencies
pip install pytest 2>/dev/null || echo "⚠️ pytest installation failed, please install manually."

# 2. Make scripts executable
chmod +x src/bug_cracker.py src/runner.py

# 3. Set up environment variables (Optional, suggests to user)
ABS_PATH=$(pwd)
echo ""
echo "✅ Installation complete!"
echo ""
echo "To finish setup, please add the following to your ~/.bashrc or ~/.zshrc:"
echo "----------------------------------------------------------------"
echo "export PATH=\$PATH:$ABS_PATH/src"
echo "export BUG_BUSTER_TEST_CMD=\"pytest -xvs\""
echo "----------------------------------------------------------------"
echo ""
echo "Then run 'source ~/.bashrc' to apply changes."
