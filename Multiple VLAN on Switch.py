from SSH_Connect import SSH

def configure_switch_vlan(ip_address, username, password):
    vlan_config = SSH(ip_address,username,password)
    vlan_config.connect()

    vlan_config.send_command("en")
    vlan_config.send_command("conf t")
    vlan_config.send_command("vlan 10")
    vlan_config.send_command("name IT")
    vlan_config.send_command("vlan 20")
    vlan_config.send_command("name Sales")
    vlan_config.send_command("vlan 30")
    vlan_config.send_command("name Marketing")
    vlan_config.send_command("end")

configure_switch_vlan("192.168.0.1", "admin", "cisco")