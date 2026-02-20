#!/bin/bash
# DARK8 OS - Automated Installer for Linux
# Supports: Ubuntu, Debian, Linux Mint, Fedora, Arch, CentOS

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INSTALL_DIR="${INSTALL_DIR:-/opt/dark8}"
BIN_DIR="/usr/local/bin"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}║    🖤 DARK8 OS - Linux Installer   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════╝${NC}"
echo ""

# Check if running as root for system-wide installation
if [[ "$INSTALL_DIR" == "/opt/"* ]]; then
    if [[ $EUID -ne 0 ]]; then
        echo -e "${YELLOW}⚠️  System installation requires sudo${NC}"
        echo "Re-running with sudo..."
        sudo "$0" "$@"
        exit 0
    fi
fi

# Detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$(echo $DISTRIB_ID | tr '[:upper:]' '[:lower:]')
    else
        echo -e "${RED}❌ Unable to detect OS${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ OS Detected: $OS${NC}"
}

# Install system dependencies
install_deps() {
    echo ""
    echo -e "${YELLOW}[1/5] Installing system dependencies...${NC}"
    
    if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]] || [[ "$OS" == "linuxmint" ]]; then
        sudo apt-get update
        sudo apt-get install -y \
            python3.10 \
            python3-pip \
            python3-venv \
            git \
            curl \
            build-essential \
            libssl-dev \
            libffi-dev
    
    elif [[ "$OS" == "fedora" ]] || [[ "$OS" == "rhel" ]] || [[ "$OS" == "centos" ]]; then
        sudo dnf install -y \
            python3.10 \
            python3-pip \
            git \
            curl \
            gcc \
            openssl-devel \
            libffi-devel
    
    elif [[ "$OS" == "arch" ]]; then
        sudo pacman -Sy --noconfirm \
            python \
            python-pip \
            git \
            curl \
            base-devel
    
    else
        echo -e "${YELLOW}⚠️  Unsupported OS. Please install dependencies manually${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Dependencies installed${NC}"
}

# Create installation directory
create_dirs() {
    echo ""
    echo -e "${YELLOW}[2/5] Creating installation directories...${NC}"
    
    sudo mkdir -p "$INSTALL_DIR"
    sudo mkdir -p ~/.dark8/{data,cache,logs}
    sudo chown -R $USER:$USER ~/.dark8
    
    echo -e "${GREEN}✓ Directories created${NC}"
}

# Copy files
copy_files() {
    echo ""
    echo -e "${YELLOW}[3/5] Copying files...${NC}"
    
    sudo cp -r "$PROJECT_ROOT/dark8_core" "$INSTALL_DIR/"
    sudo cp -r "$PROJECT_ROOT/docs" "$INSTALL_DIR/"
    sudo cp "$PROJECT_ROOT/requirements.txt" "$INSTALL_DIR/"
    sudo cp "$PROJECT_ROOT/pyproject.toml" "$INSTALL_DIR/"
    sudo cp "$PROJECT_ROOT/.env.example" "$INSTALL_DIR/.env"
    
    echo -e "${GREEN}✓ Files copied${NC}"
}

# Setup Python environment
setup_venv() {
    echo ""
    echo -e "${YELLOW}[4/5] Setting up Python environment...${NC}"
    
    cd "$INSTALL_DIR"
    python3.10 -m venv venv || python3 -m venv venv
    
    # Activate and install
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓ Python environment ready${NC}"
}

# Create wrapper script
create_wrapper() {
    echo ""
    echo -e "${YELLOW}[5/5] Creating wrapper script...${NC}"
    
    cat > /tmp/dark8 << 'EOF'
#!/bin/bash
INSTALL_DIR="/opt/dark8"
source "$INSTALL_DIR/venv/bin/activate"
cd "$INSTALL_DIR"
python -m dark8_core "$@"
EOF
    
    sudo mv /tmp/dark8 "$BIN_DIR/dark8"
    sudo chmod +x "$BIN_DIR/dark8"
    
    echo -e "${GREEN}✓ Wrapper script created${NC}"
}

# Create systemd service
create_service() {
    echo ""
    echo -e "${YELLOW}Creating systemd service...${NC}"
    
    cat > /tmp/dark8-os.service << EOF
[Unit]
Description=DARK8 OS - Autonomous AI System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python -m dark8_core --mode api
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo mv /tmp/dark8-os.service /etc/systemd/system/
    sudo systemctl daemon-reload
    
    echo -e "${GREEN}✓ Service file created${NC}"
    echo ""
    echo "To enable the service:"
    echo "  sudo systemctl enable dark8-os"
    echo "  sudo systemctl start dark8-os"
}

# Check Ollama
check_ollama() {
    echo ""
    echo -e "${YELLOW}Checking Ollama...${NC}"
    
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}✓ Ollama is installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama not found. Install from:${NC}"
        echo "   https://ollama.ai"
    fi
}

# Main installation flow
main() {
    detect_os
    install_deps
    create_dirs
    copy_files
    setup_venv
    create_wrapper
    create_service
    check_ollama
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✓ Installation Complete!          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Configure: nano ~/.env"
    echo "  2. Run CLI:   dark8"
    echo "  3. Run API:   dark8 --mode api"
    echo ""
}

main
