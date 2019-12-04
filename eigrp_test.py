#Imports the file called SSH_Connect into this script to be used for SSH conneciton
from SSH_Connect import SSH

#What I am naming the function for my eigrp configuration
def eigrp_configuration(ip_address, username, password):

    #Starts the SSH conneciton to the router
    eigrp_conf = SSH(ip_address, username, password)

    #Connects via a secure shell conneciton on port 22
    eigrp_conf.connect()

    #Calls the function within the SSH_Connect file called send_configuration which is meant for opening config files
    #Below line will open the config file for eigrp called EIGRP_Configs as set to True as by default in the SSH_Connect file it is set to false
    eigrp_conf.send_configuration(from_file=True, configuration="EIGRP_Configs.txt")

    #IP address, username and password for the router that is needed for the SSH conneciton to be successful
eigrp_configuration("192.168.1.1", "admin", "adminpass")
eigrp_configuration("192.168.1.2", "admin", "adminpass")

