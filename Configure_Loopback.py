from SSH_Connect import SSH


def configure_loopback(
    device_address, username, password, lo_address, netmask, lo_num=1, enable_pass=""
):
    """
    :param device_address: Router Address
    :param username: Administrator Username
    :param password: Administrator Password - Recommended to be passed in via getpass
    :param lo_address: Loopback Address
    :param netmask: Subnet Mask
    :param lo_num: Loopback interface number - defaults to 1
    :param enable_pass: Enable password
    :return: Status Code
    """
    remote_device = SSH(device_address, username, password, secret=enable_pass)
    remote_device.connect()

    # Create configuration list to send to router
    configuration = [
        f"int lo{lo_num}",
        f"ip address {lo_address} {netmask}",
        "description Configured Remotely using Python",
    ]
    remote_device.send_command("enable")
    remote_device.send_configuration(configuration=configuration)


# For testing purposes only
if __name__ == "__main__":
    configure_loopback(
        "192.168.1.1", "admin", "admin", "10.10.10.2", "255.0.0.0", enable_pass="admin"
    )
