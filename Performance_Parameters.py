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
import timeloop
from datetime import timedelta


def extract_metrics(device_address, device_uname, device_pass, enable_pass):
    """
    Function used to get performance metrics from network devices
    """
    # Connect to device
    network_device = ssh.SSH(device_address, device_uname, device_pass)
    network_device.connect()

    # Get performance metrics
    routing_table = network_device.send_command("show ip route")
    vlan_db = network_device.send_command("show vlan brief")
    syslogs = network_device.send_command("show logging")
    version = network_device.send_command("show version")
    # Return them
    return {
        "routing_table": routing_table,
        "vlan_db": vlan_db,
        "syslogs": syslogs,
        "version": version,
    }


def update_db(db_address, mysql_uname, mysql_pass, device_name, db_name="metrics"):

    # Connect to MySQL DB
    # Get performance metrics
    metrics = extract_metrics()

    # connects to the database
    mydb = mysql.connector.connect(
        host=db_address, user=mysql_uname, passwd=mysql_pass, db_name=db_name
    )
    mycursor = mydb.cursor()

    # commands to execute on the database
    mycursor.execute(
        "INSERT INTO performance (device_name, routing_table, vlan_db, syslogs, version) VALUES({}, {}, {}, {}, {})".format(
            device_name,
            metrics["routing_table"],
            metrics["vlan_db"],
            metrics["syslogs"],
            metrics["version"],
        )
    )

    return


def update_performance_metrics(
    timeout, db_address, mysql_uname, mysql_pass, device_name, db_name="metrics"
):
    loop = timeloop()

    @loop.job(interval=timedelta(timeout))
    def schedule_update():
        update_db(db_address, mysql_uname, mysql_pass, device_name, db_name="metrics")


if __name__ == "__main__":
    update_db()
