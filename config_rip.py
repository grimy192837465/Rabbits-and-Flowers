from SSH_Connect3 import SSH

# Function is called to configure the routers
def configure_rip(ip_address, username, password):
    # creates the ssh connection which then saves it to a variable
    rip_config = SSH(ip_address, username, password)

    # connects to the router
    rip_config.connect()

    # configurations from the rip_routers_config file
    rip_config.send_configuration(
        from_file=True, configuration="rip_routers_config.txt"
    )


# test the rip function
configure_rip("192.168.0.1", "admin", "cisco")
configure_rip("192.168.0.2", "admin", "cisco")
