from SSH_Connect import SSH

#the function named for OSPF Configuration
def configure_ospf(ip_address, username, password):
    #Starts SSH Connection for device
    configure_ospf = SSH(ip_address,username,password)
    #Should create secure connection
    configure_ospf.connect()
    
    configure_ospf.send_configuaration(from_file=True, configuration="OSPF_Config")
    
#example function for test
configure_ospf("192.168.0.1", "admin", "cisco")
configure_ospf("192.168.0.2", "admin", "cisco")