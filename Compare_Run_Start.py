"""
Compare Running Configuration with startup configuration
"""
from SSH_Connect import SSH
import getpass
import difflib


def compare_run_start(device_address, device_uname, device_pass, secret=""):
    # Setup Remote Connection
    network_device = SSH(device_address, device_uname, device_pass, secret=secret)
    network_device.connect()
    print("Getting device configuration")
    network_device.send_command("enable")
    start_conf = network_device.send_command("show start").split("\n")
    run_conf = network_device.send_command("show run").split("\n")

    # Use difflib to return list of differences
    return list(difflib.context_diff(start_conf, run_conf))


# For testing purposes only
if __name__ == "__main__":
    for i in compare_run_start("192.168.1.2", "admin", "cisco", secret="cisco"):
        print(i)
