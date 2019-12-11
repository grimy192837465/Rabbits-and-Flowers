from SSH_Connect import SSH


# Function is called to configure the routers
def RIP_Configurations(ip_address, username, password, secret=""):
    # creates the ssh connection which then saves it to a variable
    rip_config = SSH(ip_address, username, password, secret=secret)

    # connects to the router
    rip_config.connect()

    # configurations from the rip_routers_config file
    rip_config.send_configuration(
        from_file=True, configuration="rip_configurations.txt"
    )


if __name__ == "__main__":
    # test the rip function
    RIP_Configurations("192.168.0.1", "admin", "cisco")
    RIP_Configurations("192.168.0.2", "admin", "cisco")
