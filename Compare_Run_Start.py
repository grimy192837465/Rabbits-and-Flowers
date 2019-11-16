"""
Needs Testing

"start_is_shorter" stuff needs revising - could start_conf be longer than run_conf?
efficient difference detection algorithm research -> currently has O(n) running time per device

"""
import Remote_Connection

def compare_run_start():
    # Setup Remote Connection
    connection = Remote_Connection("127.0.0.1", 22)
    connection.connect()
    print("Getting device configuration")
    connection.send_command("enable")

    # Will be 2 big lists containing each line
    start_conf = connection.send_command("show startup-config").split('\n')
    run_conf = connection.send_command("show running-config").split('\n')
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
    return diffs
