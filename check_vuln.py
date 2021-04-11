import os

def check():
    vuln_file_path = os.path.join("env", "Lib", "site-packages", "pygame", "sysfont.py")
    with open(vuln_file_path, "r") as vuln_file:
        content = vuln_file.read()
        result = content.find("shell=True")
        if result > 0:
            return False
        else:
            return True
