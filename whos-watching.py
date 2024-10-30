import os
import json

from config import *
from regex_pats import *

suspicious_files = []
pass_files = []

extension_dirs = get_extension_directories()
print("Checking extension directories:", extension_dirs)

def read_file(file, root):
    if file.endswith(".js"):
        file_path = os.path.join(root, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Check for network patterns in file content
                if any(pattern.search(content) for pattern in network_patterns):
                    suspicious_files.append(file_path)
                if password_input_pattern.search(content) is not None:
                    pass_files.append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

def loop_over_files(extension_dir):
    # Walk through the directory to find .js files
    for root, dirs, files in os.walk(extension_dir):
        for file in files:
            read_file(file, root)

def clean():
    global suspicious_files
    global pass_files
    suspicious_files = []
    pass_files = []

def find_manifest_file(extension_dir):
    # Traverse the directory tree to find manifest.json
    for root, dirs, files in os.walk(extension_dir):
        if "manifest.json" in files:
            return os.path.join(root, "manifest.json")
    return None

def get_extension_name(extension_dir):
    manifest_path = find_manifest_file(extension_dir)
    if manifest_path:
        try:
            # Check if the manifest.json file exists
            if os.path.exists(manifest_path):
                with open(manifest_path, "r", encoding="utf-8") as manifest_file:
                    manifest_data = json.load(manifest_file)
                    # Extract and return the name of the extension
                    return manifest_data.get("name", "Unknown Extension")
            else:
                print(f"No manifest.json file found in {extension_dir}")
                return "Unknown Extension"
        except Exception as e:
            print(f"Error reading manifest.json in {extension_dir}: {e}")
            return "Unknown Extension"
    return "Unknown Extension"


def scan_extension(pdir):
    for extension in os.listdir(pdir):
        ext_path = os.path.join(pdir, extension)
        if os.path.isdir(ext_path):
            loop_over_files(ext_path)
            ext_name = get_extension_name(ext_path)
            if suspicious_files:
                print(f"\nNetwork requests found in extension: {ext_name}")
                for file in suspicious_files:
                    print(f"  - {file}")
            if pass_files:
                print(f"\nPassword input string found in extension: {ext_name}")
                for file in pass_files:
                    print(f"  - {file}")
            clean()

def scan_all_extensions(extension_dirs):
    for directory in extension_dirs:
        if os.path.exists(directory):
            print(f"\nScanning directory: {directory}")
            scan_extension(directory)

scan_all_extensions(extension_dirs)
