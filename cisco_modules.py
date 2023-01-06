import subprocess

def auth_cisco_vpn(username, password, domain):

    credentials = "printf 'y\\n" + username + "\\n" + password + "\\ny'"
    vpn_cmd = "/opt/cisco/anyconnect/bin/vpn -s connect '" + domain + "'"
    cmd = credentials + " | " + vpn_cmd

    # Command Execution
    print("Connecting to CISCO VPN... ")
    subprocess.Popen(cmd,
                     shell=True,
                     executable="/bin/bash",
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).communicate()


def disconnect_cisco_vpn():

    cmd = "/opt/cisco/anyconnect/bin/vpn disconnect"
    print("\nDisconnecting...  ")
    subprocess.Popen(cmd,
                     shell=True,
                     executable="/bin/bash",
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).communicate()