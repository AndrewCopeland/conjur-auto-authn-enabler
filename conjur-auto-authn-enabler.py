import urllib.request
import urllib.parse
import ssl
import json
import time
import os

INFO_URL = "https://localhost/info"
CONJUR_ENV_FILE="/opt/conjur/etc/conjur.conf"

def get_configured_authn():
    context = ssl._create_unverified_context()
    f = urllib.request.urlopen(INFO_URL, context=context)
    response=f.read().decode('utf-8')
    print(response)

    json_response = json.loads(response)
    try:
        configured_authns=json_response["authenticators"]["configured"]
    except KeyError:
        time.sleep(5)
        return get_configured_authn()
    
    print("Configured authns: {}".format(configured_authns))
    return configured_authns

def create_conjur_authenticators_line(configured_authns):
    conjur_authn_line = "CONJUR_AUTHENTICATORS="
    for configured_authn in configured_authns:
        conjur_authn_line += "{},".format(configured_authn)

    conjur_authn_line = conjur_authn_line.rstrip(",")
    return conjur_authn_line

def replace_conjur_authenticators_config(conjur_authn_line):
    lines = None
    with open(CONJUR_ENV_FILE, 'r') as f:
        lines = f.readlines()

    conjur_authn_exists=False
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("CONJUR_AUTHENTICATORS="):
            print("changing current {} => {}".format(line, conjur_authn_line))
            conjur_authn_exists=True
            lines[i]=conjur_authn_line

    if not conjur_authn_exists:
        lines.append(conjur_authn_line)

    with open(CONJUR_ENV_FILE, 'w') as f:
        f.writelines(lines)

def restart_conjur():
    print("Restarting conjur")
    os.system("sv restart conjur")

def main():
    previous_config_authns=""
    while True:
        try:
            configured_authns=get_configured_authn()
            if configured_authns != previous_config_authns:
                conjur_authn_line=create_conjur_authenticators_line(configured_authns)
                replace_conjur_authenticators_config(conjur_authn_line)
                restart_conjur()
                previous_config_authns=configured_authns
            else:
                logging.info("No newly configured authenticators")
            time.sleep(5)
        except:
            logging.warning("Failed to connect to {}, trying again in 30 seconds...".format(INFO_URL))
            time.sleep(30)

if __name__ == "__main__":
    main()
