# WhoIsBehindProxy - CLI Based Proxy Connection Verifier
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

WhoIsBehindProxy Proxy Checker is a powerful script that validates a list of proxies (HTTP, HTTPS, SOCKS) by sending requests to a test server and verifying if the proxy correctly anonymises your IP address. It's built for speed, using concurrency to test hundreds of proxies in seconds.

---

## Features

* **Blazing Fast:** Uses a thread pool to test multiple proxies concurrently.
* **Multiple Protocols:** Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies.
* **Flexible Input:** Test a single proxy, a list from a `.txt` file, or re-test an existing `.csv` file.
* **Clean Output:** Saves results in a well-structured CSV file (`proxies.csv`) with statuses like "Functional" or "Not Functional".
* **Modern & Robust:** Built with modern Python (Type Hints, Dataclasses) and robust libraries like Click and Pandas.

## Requirements
```
click==8.2.1
pandas==1.5.3
requests==2.32.4
```

## Installation
```bash
# 1. Clone the repository
git clone https://github.com/SubhojitGhimire/Who-Is-Behind-Proxy.git
cd Who-Is-Behind-Proxy/proxy-checker

# 2. Install the package in editable mode
pip install -e .
```
After installation, the tool will be available to use in terminal as the `proxy-checker` command.

##  Usage and Command Options
* `--test-url`: Use your own IP-checking service. Defaults to `https://api.ipify.org?format=json`.
* `--csv-path`: Specify a different path for the output CSV file.
* `--timeout`: Set the request timeout in seconds (default: 10).
* `--workers`: Set the number of concurrent threads (default: 10).

The tool has two main commands: `single` for individual proxies and `file` for batch processing.

### Examples

#### Test a Single Proxy

Quickly check if a single proxy is working.

```bash
proxy-checker single http://127.0.0.1:8080
```
The result will be saved to `proxies.csv`.

#### Test from a File

Test a list of proxies from a text file (`.txt`) or re-test proxies from a CSV file (`.csv`).

**1. From a Text File**

Create a `proxies.txt` file with one proxy per line:
```
http://1.2.3.4:8080
https://4.5.6.7:3128
socks5://8.9.1.2:1080
```

Then run the command:
```bash
# Test proxies from proxies.txt with 20 concurrent workers
proxy-checker file proxies.txt --workers 20
```

**2. Re-test from a CSV File**

To re-validate all proxies in your `proxies.csv` output file:
```bash
proxy-checker file proxies.csv
```

## How It Works

1.  **Request:** The tool sends an HTTP GET request to a test URL *through* the specified proxy.
2.  **Response:** The test URL service (e.g., `api.ipify.org`) returns a JSON response containing the IP address it saw (`{"ip":"1.2.3.4"}`).
3.  **Validation:** The tool compares the IP address from the response with the proxy's own IP address.

<h1></h1>

**This README.md file has been improved for overall readability (grammar, sentence structure, and organization) using AI tools.*
