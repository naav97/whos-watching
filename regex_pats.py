import re

network_patterns = [
    re.compile(r'\bfetch\b'),                  # fetch API
    re.compile(r'\bXMLHttpRequest\b'),         # XMLHttpRequest
    re.compile(r'\baxios\b'),                  # axios library
    re.compile(r'\b\$\.ajax\b'),               # jQuery AJAX
]

password_input_pattern = re.compile(r'input\s*\[\s*type\s*=\s*["\']password["\']\s*\]')
