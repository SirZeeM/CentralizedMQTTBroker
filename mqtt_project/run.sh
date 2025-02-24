#!/bin/bash

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check and install Python if not present
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
        exit 1
    fi
}

# Function to detect OS and architecture
detect_system() {
    OS="$(uname -s)"
    ARCH="$(uname -m)"
    
    case "${OS}" in
        Linux*)     OS_TYPE=Linux;;
        Darwin*)    OS_TYPE=Mac;;
        MINGW*|MSYS*|CYGWIN*) OS_TYPE=Windows;;
        *)          OS_TYPE="Unknown"
    esac
    
    case "${ARCH}" in
        x86_64|amd64) ARCH_TYPE=amd64;;
        arm64|aarch64) ARCH_TYPE=arm64;;
        *)          ARCH_TYPE="Unknown"
    esac
    
    echo -e "${BLUE}Detected OS: ${OS_TYPE}${NC}"
    echo -e "${BLUE}Detected Architecture: ${ARCH_TYPE}${NC}"
}

# Function to setup virtual environment
setup_venv() {
    echo -e "${BLUE}Setting up virtual environment...${NC}"
    
    # Handle different OS cases for venv creation
    case "${OS_TYPE}" in
        Windows)
            python -m venv venv
            source venv/Scripts/activate
            ;;
        *)
            python3 -m venv venv
            source venv/bin/activate
            ;;
    esac
    
    # Upgrade pip
    python -m pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements-test.txt" ]; then
        pip install -r requirements-test.txt
    else
        # Install minimum required packages if requirements.txt doesn't exist
        pip install pytest pytest-asyncio
    fi
}

# Function to set environment variables
setup_env() {
    # Get the repository root directory
    REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" 
    if [ -z "$REPO_ROOT" ]; then # If git is not available, use the current directory
        REPO_ROOT="$(pwd)"
    fi
    
    # Export necessary environment variables
    export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH}"
    export MQTT_PROJECT_ROOT="${REPO_ROOT}"
    
    echo -e "${GREEN}Environment variables set:${NC}"
    echo "PYTHONPATH: ${PYTHONPATH}"
    echo "MQTT_PROJECT_ROOT: ${MQTT_PROJECT_ROOT}"
}

# Function to run tests with proper configuration
run_tests() {
    local test_path=$1
    # Run pytest with asyncio mode enabled
    PYTHONPATH="${REPO_ROOT}" pytest -v --asyncio-mode=auto "${test_path}"
}

# Function to display and handle test selection menu
select_tests() {
    echo -e "\n${BLUE}Available Test Suites:${NC}"
    echo "1) Basic Packet Operations Tests"
    echo "2) Encode and Decode Tests"
    echo "3) Error Handling Tests"
    echo "4) QoS Levels Tests"
    echo "5) Run All Tests"
    echo "0) Exit"
    
    read -p "Select test suite to run (0-5): " choice
    
    case $choice in
        1)
            run_tests "mqtt_protocol/tests/test_basic_packet_operations.py"
            ;;
        2)
            run_tests "mqtt_protocol/tests/test_encode_and_decode.py"
            ;;
        3)
            run_tests "mqtt_protocol/tests/test_error_handling.py"
            ;;
        4)
            run_tests "mqtt_protocol/tests/test_qos_levels.py"
            ;;
        5)
            run_tests "mqtt_protocol/tests/"
            ;;
        0)
            echo -e "${GREEN}Exiting...${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
}

# Function to check if pytest-asyncio is installed
check_pytest_asyncio() {
    if ! pip show pytest-asyncio > /dev/null 2>&1; then
        echo -e "${BLUE}Installing pytest-asyncio...${NC}"
        pip install pytest-asyncio
    fi
}

# Main execution
main() {
    echo -e "${BLUE}=== MQTT Project Test Runner ===${NC}"
    
    # Check prerequisites
    check_python
    
    # Detect system
    detect_system
    
    # Setup virtual environment
    setup_venv
    
    # Check for pytest-asyncio
    check_pytest_asyncio
    
    # Setup environment variables
    setup_env
    
    # Run test selection menu
    while true; do
        select_tests
        echo -e "\n${BLUE}Press Enter to continue or Ctrl+C to exit${NC}"
        read
    done
}

# Run main function
main