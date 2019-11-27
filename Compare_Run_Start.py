"""
Needs Testing
PRNE Lab Fri 27th This should be done
"""
import SSH_Connect as ssh
import getpass

def compare_run_start(device_address, device_uname, device_pass, enable_pass):
    # Setup Remote Connection
    network_device = ssh.SSH(device_address, device_uname, device_pass)
    network_device.connect()
    print("Getting device configuration")
    network_device.send_command("enable", enable_pass)


    # Will be 2 big lists containing each line
    output, errors = network_device.send_command("show startup-config")
    start_conf = output.split("\n")
    output, errors = network_device.send_command("show running-config")
    run_conf = output.split('\n')
    # Differences - stores running configuration version of diff
    diffs = set()
    # Find shorter configuration
    if len(start_conf) != len(run_conf):
        start_is_shorter = True if len(start_conf) < len(run_conf) else False
    for i in range(len(start_conf if start_is_shorter else run_conf)):
        if start_conf[i] != run_conf[i]:
            print(f"Startup Configuration: {start_conf[i]} != Running Configuration: {run_conf[i]}")
            diffs.add(run_conf[i])

    # Could start_conf be longer than run_conf
    if start_is_shorter is not None:
        if start_is_shorter:
            for i in run_conf[len(start_conf[i]):]:
                diffs.add(i)
    network_device.close()
    return diffs
