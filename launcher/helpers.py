import os
import requests

latest_url = "https://github.com/mazurwiktor/albion-online-stats/releases/latest"
downloading_url = "https://github.com/mazurwiktor/albion-online-stats/releases/download/0.8.1/albion-online-stats-linux"


    # Check latest version.
def latest_version():
    req = requests.get(latest_url)
    if req.status_code == 200:
        return os.path.basename(req.url)
    return 0


    # Check users version.
def current_version():
    try:
        with open('current_version.txt', 'r') as f:
            v = f.read()
        return v
    except FileNotFoundError:
        return 0


    #Compare versions.
def check_version(latest):
    current = current_version()
    if current == 0:
        return None
    elif current < latest:
        return True
    else:
        return False


    # Create version control file.
def version_file(version):
    with open('current_version.txt', 'w') as f:
        f.write(version)
    return
