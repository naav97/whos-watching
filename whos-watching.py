import os
import re
import platform

suspicious_files = []

# Define browser extension directories based on OS
def get_extension_directories():
    system = platform.system()
    if system == "Windows":
        return [
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions"),
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Extensions"),
        ]
    elif system == "Darwin":  # macOS
        return [
            os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Extensions"),
            os.path.expanduser("~/Library/Application Support/Firefox/Profiles"),
        ]
    elif system == "Linux":
        return [
            #os.path.expanduser("~/.config/google-chrome/Default/Extensions"),
            #os.path.expanduser("~/.mozilla/firefox"),
            os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default/Extensions"),
        ]
    return []

# Example call to list directories
extension_dirs = get_extension_directories()
print("Checking extension directories:", extension_dirs)

# Define regular expressions for detecting network requests
network_patterns = [
    re.compile(r'\bfetch\b'),                  # fetch API
    re.compile(r'\bXMLHttpRequest\b'),         # XMLHttpRequest
    re.compile(r'\baxios\b'),                  # axios library
    re.compile(r'\b\$\.ajax\b'),               # jQuery AJAX
]

def read_file(file, root):
    if file.endswith(".js"):
        file_path = os.path.join(root, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Check for network patterns in file content
                if any(pattern.search(content) for pattern in network_patterns):
                    suspicious_files.append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

def scan_extension_for_network_requests(extension_dir):
    # Walk through the directory to find .js files
    for root, dirs, files in os.walk(extension_dir):
        for file in files:
            read_file(file, root)

def clean():
    global suspicious_files
    suspicious_files = []

def scan_extension(pdir):
    for extension in os.listdir(pdir):
        ext_path = os.path.join(pdir, extension)
        if os.path.isdir(ext_path):
            scan_extension_for_network_requests(ext_path)
            if suspicious_files:
                print(f"\nNetwork requests found in extension: {extension}")
                for file in suspicious_files:
                    print(f"  - {file}")
                clean()

# Step 4: Scan All Extensions and Output Results
def scan_all_extensions(extension_dirs):
    for directory in extension_dirs:
        if os.path.exists(directory):
            print(f"\nScanning directory: {directory}")
            scan_extension(directory)

# Run the scan
scan_all_extensions(extension_dirs)
