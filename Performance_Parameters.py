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
import SSH_Connect as ssh
import mysql.connector
import multiprocessing
import getpass
import time
from socket import inet_aton


def extract_metrics(device_address, device_uname, device_pass, secret=""):
    """
    Function used to get performance metrics from network devices
    """
    # Connect to device
    network_device = ssh.SSH(device_address, device_uname, device_pass, secret=secret)
    network_device.connect()

    # Get performance metrics
    routing_table = network_device.send_command("show ip route")
    vlan_db = network_device.send_command("show vlans")
    syslogs = network_device.send_command("show logging")
    version = network_device.send_command("show version")

    network_device.close()
    # Return them
    return {
        "routing_table": routing_table,
        "vlan_db": vlan_db,
        "syslogs": syslogs,
        "version": version,
    }


def get_mysql_info():
    """
    Gets mysql database information
    :return list: Contains a list comprised of: Database Address, MySQL Username, MySQL Password
    """
    print("Getting MySQL info..")
    while True:
        db_address = input("Enter Database Server address: ")
        try:
            inet_aton(db_address)
            break
        except OSError:
            print("Incorrect address given: Be sure to specify an IP Address!")
            continue

    mysql_username = input("Enter database username: ")

    while True:
        mysql_pass = getpass.getpass("Enter database account password: ")
        if mysql_pass != getpass.getpass("Confirming password: "):
            print("Passwords dont match!")
            continue
        else:
            break

    return [db_address, mysql_username, mysql_pass]


def update_db(device_address, device_uname, device_pass, db_address, mysql_uname, mysql_pass,  db_name="metrics", secret=""):
    # Get performance metrics
    metrics = extract_metrics(device_address, device_uname, device_pass, secret=secret)

    mydb = mysql.connector.connect(host=db_address, user=mysql_uname, passwd=mysql_pass, database=db_name)
    mycursor = mydb.cursor()

    # commands to execute on the database
    mycursor.execute("USE metrics;")
    mycursor.execute(
        "INSERT INTO performance (device_name, routing_table, vlan_db, syslogs, version) VALUES(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\");".format(
            device_address,
            metrics["routing_table"].replace("\"", ""),
            metrics["vlan_db"].replace("\"", ""),
            metrics["syslogs"].replace("\"", ""),
            metrics["version"].replace("\"", "")
        )
    )

    mydb.commit()

    return


def update_performance_metrics(device_address, device_uname, device_pass, secret=""):
    # Get MySQL info
    db_address, mysql_uname, mysql_pass = get_mysql_info()

    while True:
        try:
            timeout = int(input("Please specify a timeout in seconds: "))
            if timeout < 60:
                print("Specify a timeout of at least 60s")
                continue
            else:
                break
        except TypeError:
            print("Please input a number")
            continue

    def set_timeout(device_address, device_uname, device_pass, db_address, mysql_uname, mysql_pass, timeout, secret=""):
        while True:
            update_db(device_address, device_uname, device_pass, db_address, mysql_uname, mysql_pass, secret=secret)
            time.sleep(timeout)

    proc = multiprocessing.Process(target=set_timeout, args=(device_address, device_uname, device_pass, db_address, mysql_uname, mysql_pass, timeout))
    proc.start()

    return ("Kill this proc when finished", proc)


if __name__ == "__main__":
    print("Scheduling update")
    update_performance_metrics("192.168.0.1", "admin", "cisco")
