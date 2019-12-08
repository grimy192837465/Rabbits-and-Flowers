from SSH_Connect import SSH

# function that can be called to configure the vlans on switches
def configure_switch_vlan(ip_address, username, password):
    # creates the ssh connection and saves it to a variable
    vlan_config = SSH(ip_address, username, password)
    # connects to the device
    vlan_config.connect()

    vlan_config.send_configuration(from_file=True, configuration="Multi_switch_conf")


# test function
configure_switch_vlan("192.168.0.1", "admin", "cisco")
configure_switch_vlan("192.168.0.2", "admin", "cisco")
