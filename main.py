import hashlib
import os
import shutil  # This library helps move files

# 1. Load virus hashes from database.txt
def load_signatures(db_file):
    try:
        with open(db_file, "r") as f:
            # Removes extra spaces and loads hashes into a list
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: {db_file} not found!")
        return []

# 2. Calculate MD5 hash of a file (Digital Fingerprint)
def get_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
            # Creating a unique MD5 hash for the file
            return hashlib.md5(file_data).hexdigest()
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return None

# 3. Main Scanner with Quarantine Logic
def start_antivirus_scan(directory_to_scan):
    print(f"--- Antivirus Scan Started in: {directory_to_scan} ---")
    
    # Getting the list of bad hashes from your file
    signatures = load_signatures("database.txt")
    quarantine_path = "quarantine"

    # Create quarantine folder if it doesn't exist
    if not os.path.exists(quarantine_path):
        os.makedirs(quarantine_path)
        print(f"[*] Created quarantine folder.")

    # Looking through every file in the folder
    for filename in os.listdir(directory_to_scan):
        # Skip the script itself and the database file to avoid errors
        if filename == "main.py" or filename == "database.txt":
            continue
            
        file_path = os.path.join(directory_to_scan, filename)
        
        # We only want to scan files, not other folders
        if os.path.isfile(file_path):
            file_hash = get_file_hash(file_path)
            
            # If the file's hash matches one in our database
            if file_hash in signatures:
                print(f"[!] DANGER: Virus found in {filename}!")
                # Move the file to the quarantine folder (Isolation)
                shutil.move(file_path, os.path.join(quarantine_path, filename))
                print(f"[#] Action: {filename} has been moved to Quarantine.")
            else:
                print(f"[+] Safe: {filename}")

# Start the program
if __name__ == "__main__":
    # The dot "." means it will scan the current folder
    start_antivirus_scan(".")