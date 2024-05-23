from flask import Flask, render_template, jsonify

app = Flask(__name__)

import requests
import json
import re

def check_and_print_responses(urls, output_file):
    results = []
    for url in urls:
        response = requests.get(url)
        status = "CHECKED" if response.status_code == 200 else f"FAILED ({response.status_code})"
        results.append({"url": url, "status": status})
        if response.status_code == 200:
            print(f"Checking response for {url}... {status}")
            print(response.text, file=output_file)
        else:
            print(f"Checking response for {url}... {status}")
            print(f"Invalid response for {url}:", file=output_file)
    return results

def main():
    ############################### File paths from the System ###############################
    ips_file = "D:\\TI FEED WEB APP\\FeedIps.txt"
    urls_file = "D:\\TI FEED WEB APP\\FeedURLs.txt"
    all_ips_file = "D:\\TI FEED WEB APP\\AllIps.txt"
    all_urls_file = "D:\\TI FEED WEB APP\\AllUrls.txt"
    
    # Read IPs from file and check responses
    with open(ips_file, 'r') as file:
        ips_urls = file.read().splitlines()

    # Read URLs from file and check responses
    with open(urls_file, 'r') as file:
        urls_urls = file.read().splitlines()

    with open(all_ips_file, 'w') as ips_output_file:
        ips_results = check_and_print_responses(ips_urls, ips_output_file)

    print("\n")
    print("Checking for the Status of URL:\n".upper())

    with open(all_urls_file, 'w') as urls_output_file:
        urls_results = check_and_print_responses(urls_urls, urls_output_file)

    print("All the IPs and URLs have been successfully collected. Results saved in AllIps.txt and AllUrls.txt\n".upper())
    return {"ips": ips_results, "urls": urls_results}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/startCollection')
def start_collection():
    results = main()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
