#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file="$1"
output_file="ip_addresses.txt"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' not found."
    exit 1
fi

# Loop through each domain in the input file
while IFS= read -r domain; do
    # Perform a ping to resolve the domain to an IP address
    ip_address=$(ping -c 1 "$domain" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1)
    
    # Check if the IP address is valid
    if [ -n "$ip_address" ]; then
        # Append the IP address to the output file
        echo "$domain: $ip_address" >> "$output_file"
    else
        echo "Failed to resolve IP address for: $domain"
    fi
done < "$input_file"

echo "IP addresses extracted and saved to '$output_file'."

