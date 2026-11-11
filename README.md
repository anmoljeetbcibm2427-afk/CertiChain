# CertiChain — Blockchain Certificate Verification System

A beginner-friendly educational blockchain mini project built with Python, Flask, HTML, CSS and SHA-256.

## 1. Requirements
- Python 3.10 or newer
- VS Code (recommended)
- A web browser
- Internet is needed only to install Flask

## 2. Project structure

certificate_verification_system/
|-- app.py
|-- requirements.txt
|-- blockchain.json       (created automatically when you run the app)
|-- templates/
|   `-- index.html
`-- static/
    `-- style.css

## 3. Setup on Windows

Open this folder in VS Code. Open Terminal > New Terminal and run:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

If `py` does not work, try `python` instead.

Open this address in your browser:
http://127.0.0.1:5000

Keep the terminal open while using the website. Press Ctrl+C in the terminal to stop the server.

## 4. First test

### Issue a certificate
Use:
- Student name: Amandeep Kaur
- Certificate ID: CERT-1001
- Course name: Python Programming

Click **Issue certificate**. You should see a success message and a new block in the blockchain records.

### Verify the same certificate
Enter:
- Certificate ID: CERT-1001
- Student name: Amandeep Kaur
- Course name: Python Programming

Click **Verify certificate**. The site should report that the certificate is genuine.

### Test a mismatch
Keep the ID as CERT-1001 but change the student name or course. Verification should fail.

### Test an unknown ID
Try CERT-9999. The site should report that the certificate was not found.

### Check blockchain integrity
Click **Check blockchain**. It should report that the blockchain is valid.

## 5. How the blockchain works

Each block contains:
- Index: block number
- Timestamp: when the block was created
- Data: certificate details and its certificate hash
- Previous hash: hash of the block before it
- Hash: SHA-256 fingerprint of the current block

The first block is called the **genesis block**. Its previous hash is `0`.

When a new certificate is issued:
1. The app prepares certificate information.
2. SHA-256 creates a fingerprint for the certificate information.
3. The information and fingerprint are placed in a new block.
4. The new block stores the previous block's hash.
5. The complete chain is saved in `blockchain.json`.

The chain validation function recalculates each block's hash and checks the previous-hash links.

## 6. Important project limitation

This is a local educational prototype. The JSON file is stored on one computer, and there is no distributed network, consensus mechanism, wallet, or real cryptographic identity system. It demonstrates hash linking and tamper detection, not production-grade certificate security.

For a classroom demo, do not enter real personal or confidential student information.

## 7. Common problems

- **No module named flask:** Activate `.venv`, then run `py -m pip install -r requirements.txt`.
- **Python is not recognized:** Install Python from python.org and enable "Add Python to PATH", then reopen VS Code.
- **Address already in use:** Another Flask app may be running. Stop it with Ctrl+C before starting this app again.
- **Port 5000 is busy:** Change the final line in app.py to `app.run(debug=True, port=5001)` and open http://127.0.0.1:5001.
- **Old test certificates appear:** Stop the server, delete `blockchain.json`, then run `py app.py` again. This resets the demo chain.

## 8. Viva questions to prepare

1. What is blockchain? A chain of records called blocks, linked using cryptographic hashes.
2. What is SHA-256? A hash algorithm that creates a 256-bit (64-character hexadecimal) digest.
3. What is a block? A record containing data, timestamp, its hash and the previous block's hash.
4. What is a genesis block? The first block in a blockchain.
5. Why store the previous hash? It links blocks and helps detect changes.
6. What is Flask? A lightweight Python web framework.
7. What is tampering? Unauthorized changing of stored information.
8. Is this a decentralized blockchain? No, it is a local educational prototype.
