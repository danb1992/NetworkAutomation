from netmiko import ConnectHandler
from getpass import getpass


# Netmiko Boilerplate

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.0.26",
    "username": input("Enter username: "),
    "password": getpass("Enter password: ",echo_char="*"),
    "secret": getpass("Enter enable secret: ",echo_char="#"),
    "port": 22,
    "session_log": "session_log.txt"
}

connection = ConnectHandler(**device)

# Enter Priv EXEC Mode

connection.enable()

