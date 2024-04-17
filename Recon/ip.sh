#!/bin/bash

# Define text colors
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NC=$(tput sgr0)

# Print banner
echo "${YELLOW}-------------------------------------"
echo "      Domain Ping Status Checker"
echo "-------------------------------------${NC}"
echo

# Initialize counters
total_domains=0
live_domains=0
offline_domains=0

# Read each domain from the file
while IFS= read -r domain; do
    # Increment total domain counter
    ((total_domains++))

    # Ping the domain and capture the output
    ping_output=$(ping -c 1 "$domain" 2>&1)

    # Check if ping was successful
    if [ $? -eq 0 ]; then
        # Extract the IP address from the ping output
        ip_address=$(echo "$ping_output" | awk '/^PING/{print $3}' | tr -d '():')

        # Increment live domain counter
        ((live_domains++))

        # Print the live status and IP address with green color
        echo "${GREEN}Live:${NC} $domain - $ip_address"
    else
        # Increment offline domain counter
        ((offline_domains++))

        # Print the not live status with red color
        echo "${RED}Offline:${NC} $domain"
    fi
done < domains.txt

# Print summary
echo
echo "${YELLOW}-------------------------------------"
echo "           Summary"
echo "-------------------------------------${NC}"
echo "Total domains scanned: $total_domains"
echo "${GREEN}Live domains: $live_domains${NC}"
echo "${RED}Offline domains: $offline_domains${NC}"
echo "${YELLOW}-------------------------------------${NC}"

