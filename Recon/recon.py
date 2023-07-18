import sys
import os
import subprocess

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_subprocess(command):
    subprocess.run(command, shell=True)

def gather_subdomains(domain):
    print("Gathering subdomains with Sublist3r...")
    run_subprocess(f"sublist3r -d {domain} -o subdomains.txt")
    with open("subdomains.txt", "a") as file:
        file.write(domain + "\n")

def compile_third_level_subdomains():
    sublist3r_output = subprocess.run(["cat", "subdomains.txt"], capture_output=True, text=True).stdout
    third_level_domains = subprocess.run(["grep", "-Po", "(\w+\.\w+\.\w+)$"], input=sublist3r_output, capture_output=True, text=True).stdout

    if third_level_domains:
        print("Compiling third-level subdomains...")
        run_subprocess("cat subdomains.txt | grep -Po '(\w+\.\w+\.\w+)$' | sort -u > third-level-subdomains.txt")
        print("Gathering fourth-level domains with Sublist3r...")
        if len(sys.argv) == 2:
            print("Probing for alive third-levels with httprobe...")
            run_subprocess("cat subdomains.txt | sort -u | httprobe -s -p https:443 | sed 's/https\?:\/\///' | tr -d ':443' > probed.txt")
        else:
            print("Probing for alive fourth-level with httprobe...")
            run_subprocess("cat fourth-level/* | sort -u | grep -v {} | httprobe -s -p https:443 | sed 's/https\?:\/\///' | tr -d ':443' > probed.txt".format(sys.argv[2]))
    else:
        print("No third-level domains found...")
        if len(sys.argv) == 2:
            print("Probing for alive domains with httprobe...")
            run_subprocess("cat subdomains.txt | sort -u | grep -v {} | httprobe -s -p https:443 | sed 's/https\?:\/\///' | tr -d ':443' > probed.txt".format(sys.argv[2]))
        else:
            print("Probing for alive domains with httprobe...")
            run_subprocess("cat subdomains.txt | sort -u | httprobe -s -p https:443 | sed 's/https\?:\/\///' | tr -d ':443' > probed.txt")

def cleanup_files():
    print("Cleaning up files...")
    run_subprocess("rm -rf fourth-levels/ spiderlinks.txt")

def run_gospider():
    print("Running Gospider on domains (Things start taking a while from this point onwards. Be patient.)")
    run_subprocess("gospider -S spiderlinks.txt -c 10 -d 5 --blacklist '.(jpg|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico|pdf|svg|txt)' | tee spiderlinks2.txt")
    run_subprocess("cat spiderlinks2.txt | gf urls | grep {} | qsreplace -a 'input' | sort -u > spiderlinks.txt".format(sys.argv[1]))
    run_subprocess("rm spiderlinks2.txt")
    print("Done with the GoSpider scan!")
    print("Link crawling is now finished; find results in the text file: spiderlinks.txt")

def run_exploitation():
    print("Making neat exploitation links with gf")
    print("Generating links to exploit")
    run_subprocess("for patt in $(cat patterns); do gf $patt spiderlinks.txt | grep {} | qsreplace -a | sort -u | tee linkstemp/$patt-links.txt; done".format(sys.argv[1]))
    run_subprocess("for patt in $(cat patterns); do cat linkstemp/$patt-links.txt | gf $patt | qsreplace -a | sort -u | httpx > links/$patt-links.txt; done")
    run_subprocess("rm -rf linkstemp/")

def run_fimap():
    print("Using fimap to scan for LFI vulns")
    run_subprocess("python2 ~/BugBounty/Tools/fimap/src/fimap.py -m -l links/lfi-links.txt -w results/lfi-results.txt")
    print("fimap scan finished")

def run_xss_scan():
    print("Started vulnerability scanning. Please maintain your patience")
    print("Running XSS scans on links..")
    run_subprocess("cat links/xss-links.txt | dalfox pipe | tee results/xss-results.txt")

def run_sql_injections():
    print("Running SQL Injections on links")
    run_subprocess("sqlmap -m links/sqli-links.txt --batch --level 2 | tee results/sqli-results.txt")

def run_waybackmachine():
    print("Running Waybackmachine on all successfully probed domain names")
    run_subprocess("awk '$0=\"https://\"$0' probed.txt | waybackurls | grep {} | qsreplace -a 'input' | sort -u > waybackurls.txt".format(sys.argv[1]))
    print("Waybackmachine search finished")

def main():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print("Usage: ./script.py <domain>")
        print("Example: ./script.py yahoo.com")
        sys.exit(1)

    # Create directories
    create_directory("dirscan/")
    create_directory("fourth-levels/")
    create_directory("results/")
    create_directory("links/")
    create_directory("linkstemp/")

    # Recon and enumeration
    print("Reconnaisance started:")

    gather_subdomains(sys.argv[1])
    compile_third_level_subdomains()

    # Other parts of the script go here...
    cleanup_files()
    run_gospider()
    run_exploitation()
    run_fimap()
    run_xss_scan()
    run_sql_injections()
    run_waybackmachine()

    print("Scanning is done, please refer to results and other text files to see what I found...")

if __name__ == "__main__":
    main()
