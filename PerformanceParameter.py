"""
Extract
-Routing Table
-VLAN Database
-Syslog messages
--Show Logging
-IOS Version

Export to MySQL DB

Run at intervals
-Once an hour

"""
import time
import SSH_Connect as ssh
import mysql.connector


def extract_metrics(device_address, device_uname, device_pass, enable_pass):
    """
    Function used to get performance metrics from network devices
    """
    # Connect to device
    network_device = ssh.SSH(device_address, device_uname, device_pass)
    network_device.connect()
    network_device.send_command("enable", enable_pass)

    # Get performance metrics
    routing_table, errors = network_device.send_command("show ip route")
    vlan_db, errors = network_device.send_command("show vlan brief")
    syslogs, errors = network_device.send_command("show logging")
    version, errors = network_device.send_command("show version")
    # Return them
    return {"routing_table": routing_table, "vlan_db": vlan_db, "syslogs": syslogs, "version": version}


def update_db(db_address, mysql_uname, mysql_pass):

    # Connect to MySQL DB
    # Get performance metrics
    metrics = extract_metrics()

    # Insert into database

    return


def schedule_update(timeout):
    pass