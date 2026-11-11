from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-demo-secret-key"

DATA_FILE = "blockchain.json"


def calculate_hash(data):
    """Create a SHA-256 fingerprint from a dictionary."""
    encoded_data = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded_data).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        data = {
            "certificate_id": "GENESIS",
            "student_name": "Blockchain System",
            "course": "Genesis Block",
            "issue_date": "System Start",
            "certificate_hash": "GENESIS"
        }
        block = {
            "index": 0,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "data": data,
            "previous_hash": "0"
        }
        block["hash"] = calculate_hash(block)
        return block

    def load_chain(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    self.chain = json.load(file)
                if not isinstance(self.chain, list) or not self.chain:
                    self.chain = [self.create_genesis_block()]
                    self.save_chain()
            except (json.JSONDecodeError, OSError):
                self.chain = [self.create_genesis_block()]
                self.save_chain()
        else:
            self.chain = [self.create_genesis_block()]
            self.save_chain()

    def save_chain(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.chain, file, indent=4)

    def add_block(self, certificate_data):
        previous_block = self.chain[-1]
        block = {
            "index": len(self.chain),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "data": certificate_data,
            "previous_hash": previous_block["hash"]
        }
        block["hash"] = calculate_hash(block)
        self.chain.append(block)
        self.save_chain()
        return block

    def is_chain_valid(self):
        if not self.chain:
            return False

        for index, block in enumerate(self.chain):
            block_without_hash = {
                "index": block["index"],
                "timestamp": block["timestamp"],
                "data": block["data"],
                "previous_hash": block["previous_hash"]
            }

            if calculate_hash(block_without_hash) != block["hash"]:
                return False

            if index == 0:
                if block["previous_hash"] != "0":
                    return False
            else:
                previous_block = self.chain[index - 1]
                if block["previous_hash"] != previous_block["hash"]:
                    return False

        return True

    def find_certificate(self, certificate_id):
        for block in self.chain[1:]:
            if block["data"].get("certificate_id") == certificate_id:
                return block
        return None


blockchain = Blockchain()


@app.route("/")
def home():
    return render_template(
        "index.html",
        total_certificates=len(blockchain.chain) - 1,
        chain_valid=blockchain.is_chain_valid(),
        blocks=blockchain.chain[1:][::-1]
    )


@app.route("/issue", methods=["POST"])
def issue_certificate():
    student_name = request.form.get("student_name", "").strip()
    certificate_id = request.form.get("certificate_id", "").strip().upper()
    course = request.form.get("course", "").strip()

    if not student_name or not certificate_id or not course:
        flash("Please fill in all certificate fields.", "error")
        return redirect(url_for("home"))

    if blockchain.find_certificate(certificate_id):
        flash("That certificate ID already exists. Please use a different ID.", "error")
        return redirect(url_for("home"))

    certificate_data = {
        "certificate_id": certificate_id,
        "student_name": student_name,
        "course": course,
        "issue_date": datetime.now().strftime("%Y-%m-%d")
    }
    certificate_data["certificate_hash"] = calculate_hash(certificate_data)

    new_block = blockchain.add_block(certificate_data)
    flash(
        f"Certificate issued successfully! Block #{new_block['index']} was created.",
        "success"
    )
    return redirect(url_for("home"))


@app.route("/verify", methods=["POST"])
def verify_certificate():
    certificate_id = request.form.get("certificate_id", "").strip().upper()
    student_name = request.form.get("verify_student_name", "").strip()
    course = request.form.get("verify_course", "").strip()

    if not certificate_id or not student_name or not course:
        flash("Enter the certificate ID, student name and course.", "error")
        return redirect(url_for("home"))

    block = blockchain.find_certificate(certificate_id)

    if not blockchain.is_chain_valid():
        flash("WARNING: Blockchain integrity check failed. Records may have been modified.", "error")
    elif block is None:
        flash("Certificate not found. It is not registered in this blockchain.", "error")
    else:
        saved = block["data"]
        details_match = (
            saved["student_name"].casefold() == student_name.casefold()
            and saved["course"].casefold() == course.casefold()
        )
        expected_hash = calculate_hash({
            "certificate_id": saved["certificate_id"],
            "student_name": saved["student_name"],
            "course": saved["course"],
            "issue_date": saved["issue_date"]
        })

        if details_match and expected_hash == saved["certificate_hash"]:
            flash(
                f"VERIFIED: Certificate {certificate_id} is genuine. "
                f"It is stored in block #{block['index']}.",
                "success"
            )
        else:
            flash("NOT VERIFIED: The details do not match the registered certificate.", "error")

    return redirect(url_for("home"))


@app.route("/check-chain")
def check_chain():
    if blockchain.is_chain_valid():
        flash("Blockchain is valid. All blocks and links passed the integrity check.", "success")
    else:
        flash("Blockchain is INVALID. A block or link may have been changed.", "error")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
