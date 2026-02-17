#!/bin/bash

# Install llvmlite Script for MindsDB
# This script installs llvmlite with proper LLVM 20 configuration
#
# Usage:
#   ./install-llvmlite.sh          # Interactive mode (prompts if llvmlite exists)
#   ./install-llvmlite.sh --force   # Force reinstall even if already installed
#   ./install-llvmlite.sh -f        # Same as --force
#
# Requirements:
#   - mindsdb-venv virtual environment must exist
#   - LLVM 20 must be installed via Homebrew (brew install llvm@20)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${GREEN}=== Installing llvmlite for MindsDB ===${NC}"
echo ""

# Check if venv exists
if [ ! -d "mindsdb-venv" ]; then
    echo -e "${RED}❌ mindsdb-venv not found!${NC}"
    echo "Please create the virtual environment first:"
    echo "  python3 -m venv mindsdb-venv"
    exit 1
fi

# Activate venv
echo -e "${YELLOW}Activating virtual environment...${NC}"
source mindsdb-venv/bin/activate

# Check if LLVM 20 is installed
echo -e "${YELLOW}Checking for LLVM 20...${NC}"
if ! brew list llvm@20 >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  LLVM 20 not found. Installing...${NC}"
    brew install llvm@20
fi

# Get LLVM 20 prefix
LLVM20_PREFIX=$(brew --prefix llvm@20)
if [ -z "$LLVM20_PREFIX" ]; then
    echo -e "${RED}❌ Could not find LLVM 20 installation${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found LLVM 20 at: $LLVM20_PREFIX${NC}"

# Set up LLVM environment variables
export LLVM_DIR="$LLVM20_PREFIX/lib/cmake/llvm"
export CMAKE_PREFIX_PATH="$LLVM20_PREFIX:$CMAKE_PREFIX_PATH"
export LDFLAGS="-L$LLVM20_PREFIX/lib"
export CPPFLAGS="-I$LLVM20_PREFIX/include"

echo -e "${GREEN}✅ Set LLVM_DIR=$LLVM_DIR${NC}"
echo -e "${GREEN}✅ Set CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH${NC}"
echo ""

# Verify LLVM CMake config exists
if [ ! -f "$LLVM_DIR/LLVMConfig.cmake" ]; then
    echo -e "${RED}❌ LLVMConfig.cmake not found at $LLVM_DIR${NC}"
    echo "Trying to find it..."
    LLVM_CMAKE=$(find "$LLVM20_PREFIX" -name "LLVMConfig.cmake" 2>/dev/null | head -1)
    if [ -n "$LLVM_CMAKE" ]; then
        LLVM_DIR=$(dirname "$LLVM_CMAKE")
        export LLVM_DIR
        echo -e "${GREEN}✅ Found at: $LLVM_DIR${NC}"
    else
        echo -e "${RED}❌ Could not find LLVMConfig.cmake${NC}"
        exit 1
    fi
fi

# Check for --force flag
FORCE_REINSTALL=false
if [[ "${1:-}" == "--force" ]] || [[ "${1:-}" == "-f" ]]; then
    FORCE_REINSTALL=true
fi

# Check current llvmlite status
echo -e "${YELLOW}Checking current llvmlite installation...${NC}"
if python -c "import llvmlite" 2>/dev/null; then
    CURRENT_VERSION=$(python -c "import llvmlite; print(llvmlite.__version__)" 2>/dev/null || echo "unknown")
    echo -e "${YELLOW}⚠️  llvmlite $CURRENT_VERSION is already installed${NC}"
    if [ "$FORCE_REINSTALL" = true ]; then
        echo -e "${YELLOW}Force flag detected. Reinstalling...${NC}"
        echo -e "${YELLOW}Uninstalling existing llvmlite...${NC}"
        pip uninstall -y llvmlite 2>/dev/null || true
    else
        read -p "Reinstall anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping reinstall. Use --force to reinstall automatically."
            exit 0
        fi
        echo -e "${YELLOW}Uninstalling existing llvmlite...${NC}"
        pip uninstall -y llvmlite 2>/dev/null || true
    fi
fi

# Install llvmlite
echo ""
echo -e "${YELLOW}Installing llvmlite (this may take a few minutes)...${NC}"
if pip install llvmlite; then
    echo -e "${GREEN}✅ llvmlite installed successfully!${NC}"
else
    echo -e "${RED}❌ Failed to install llvmlite${NC}"
    exit 1
fi

# Verify installation
echo ""
echo -e "${YELLOW}Verifying installation...${NC}"
if python -c "import llvmlite; print(f'llvmlite {llvmlite.__version__}')" 2>/dev/null; then
    VERSION=$(python -c "import llvmlite; print(llvmlite.__version__)")
    echo -e "${GREEN}✅ llvmlite $VERSION is working correctly!${NC}"
else
    echo -e "${RED}❌ llvmlite installation verification failed${NC}"
    exit 1
fi

# Also check/install mind-castle (since it was in the error)
echo ""
echo -e "${YELLOW}Checking mind-castle...${NC}"
if ! python -c "import mind_castle" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  mind-castle not found. Installing...${NC}"
    pip install "mind-castle>=0.4.9"
    echo -e "${GREEN}✅ mind-castle installed${NC}"
else
    echo -e "${GREEN}✅ mind-castle is already installed${NC}"
fi

# Final verification
echo ""
echo -e "${GREEN}=== Final Verification ===${NC}"
python -c "
import sys
deps = {
    'llvmlite': 'llvmlite',
    'numba': 'numba',
    'mind_castle': 'mind_castle'
}
print('Checking dependencies...')
for name, module in deps.items():
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'unknown')
        print(f'  ✅ {name}: {version}')
    except ImportError as e:
        print(f'  ❌ {name}: {e}')
        sys.exit(1)
print('\\n✅ All dependencies verified!')
"

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo "You can now run MindsDB with:"
echo "  source mindsdb-venv/bin/activate"
echo "  make run_mindsdb_full_apis"
echo ""
echo "Or use the venv python directly:"
echo "  ./mindsdb-venv/bin/python -m mindsdb"
