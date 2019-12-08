"""
Needs Testing
PRNE Lab Fri 27th This should be done
"""
from SSH_Connect import SSH
import getpass
import difflib
import platform
import subprocess


def compare_run_start(device_address, device_uname, device_pass, enable_pass):
    # Setup Remote Connection
    network_device = SSH(device_address, device_uname, device_pass, secret=enable_pass)
    network_device.connect()
    print("Getting device configuration")
    start_conf = network_device.send_command("show startup-config")
    run_conf = network_device.send_command("show running-config")

    # Get OS Name to find out which difference finding program to run

    start_conf_ls = start_conf.split("\n")
    run_conf_ls = run_conf.split("\n")
    # Differences - stores running configuration version of diff
    diffs = set()
    # Find shorter configuration
    if len(start_conf_ls) != len(run_conf_ls):
        start_is_shorter = True if len(start_conf_ls) < len(run_conf_ls) else False
    for i in range(len(start_conf_ls if start_is_shorter else run_conf_ls)):
        if start_conf_ls[i] != run_conf_ls[i]:
            print(
                f"Startup Configuration: {start_conf_ls[i]} != Running Configuration: {run_conf_ls[i]}"
            )
            diffs.add(run_conf_ls[i])

    # Could start_conf be longer than run_conf
    if start_is_shorter is not None:
        if start_is_shorter:
            for i in run_conf_ls[len(start_conf_ls[i]) :]:
                diffs.add(i)
    network_device.close()
    return diffs


if __name__ == "__main__":
    compare_run_start("192.168.1.1", "admin2", "admin", "admin")
