#!/bin/bash

# Function to print banner
print_banner() {
    echo -e "\033[1;34m"
    echo "-------------------------------------------------"
    echo "         Domain Live Check Tool                   "
    echo "-------------------------------------------------"
    echo -e "\033[0m"
}

# Function to check if a domain is live using ping
check_with_ping() {
    input_file=$1
    while IFS= read -r domain || [[ -n "$domain" ]]; do
        echo -n "Checking $domain with ping: "
        if ping -c 1 "$domain" &>/dev/null; then
            echo -e "\033[0;32mLive\033[0m"
            echo "$domain" >> livehosts.txt
        else
            echo -e "\033[0;31mNot Live\033[0m"
            echo "$domain" >> dead.txt
        fi
    done < "$input_file"
}

# Function to check if a domain is live using ncat
check_with_ncat() {
    input_file=$1
    while IFS= read -r domain || [[ -n "$domain" ]]; do
        echo -n "Checking $domain with ncat: "
        if ncat -zv "$domain" 80 &>/dev/null; then
            echo -e "\033[0;32mLive\033[0m"
            echo "$domain" >> livehosts.txt
        else
            echo -e "\033[0;31mNot Live\033[0m"
            echo "$domain" >> dead.txt
        fi
    done < "$input_file"
}

# Function to check if a domain is live using curl
check_with_curl() {
    input_file=$1
    while IFS= read -r domain || [[ -n "$domain" ]]; do
        echo -n "Checking $domain with curl: "
        if curl --head "$domain" &>/dev/null; then
            echo -e "\033[0;32mLive\033[0m"
            echo "$domain" >> livehosts.txt
        else
            echo -e "\033[0;31mNot Live\033[0m"
            echo "$domain" >> dead.txt
        fi
    done < "$input_file"
}

# Main script
print_banner
echo "Select an option:"
echo "1. Check with ping"
echo "2. Check with ncat"
echo "3. Check with curl"

read -p "Enter your choice (1/2/3): " choice

read -p "Enter the path to the input file: " input_file

case $choice in
    1) check_with_ping "$input_file" ;;
    2) check_with_ncat "$input_file" ;;
    3) check_with_curl "$input_file" ;;
    *) echo "Invalid choice. Exiting." ;;
esac

