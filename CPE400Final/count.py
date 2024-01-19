#!/usr/bin/env python3

import sys
import json
from scapy.all import *

# Initialize counters
tcp_count = 0
udp_count = 0
other_count = 0

# Function to process each packet
def process_packet(packet):
    global tcp_count, udp_count, other_count

    # Check if the packet has a layer for TCP or UDP
    if TCP in packet:
        tcp_count += 1
    elif UDP in packet:
        udp_count += 1
    else:
        other_count += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script.py file.pcapng output.json")
        sys.exit(1)

    file_path = sys.argv[1]
    json_file_path = sys.argv[2]

    # Read the pcapng file
    try:
        packets = rdpcap(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    # Process each packet in the file
    for packet in packets:
        process_packet(packet)

    # Create or load existing JSON file
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Update counts in the JSON data
    data[file_path] = {
        "tcp_count": tcp_count,
        "udp_count": udp_count,
        "other_count": other_count
    }

    # Write updated data to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Counts appended to {json_file_path}")