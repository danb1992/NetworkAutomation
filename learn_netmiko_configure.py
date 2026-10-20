from netmiko import ConnectHandler
from getpass import getpass
import os


"""
Netmiko Boilerplate
"""

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.0.26",
    "username": input("Enter username: "),
    "password": getpass("Enter password: ",echo_char="*"),
    "port": 22,
    "session_log": "session_log_configure.txt" # Uses different log file than 'session_log.txt' to have one log file per Python script
}

connection = ConnectHandler(**device)

"""
Explicitly calls the directory where the 'configure_loopback2.txt' file is located
instead of specifying the full path
"""

directory = os.path.dirname(os.path.abspath(__file__)) 

"""
Send Configuration to Device using Python List
'config_loopback_1' variable is a list, containing the lines to configure interface Loopback1
'send_config_set()' method allows multiple configuration lines to be sent, instead of using 'send_command()' multiple times
"""

loopback_1_config = [
    "interface Loopback1",
    "description Configured using Netmiko send_config_set() method",
    "ip address 10.0.0.1 255.255.255.255",
    "no shutdown"
]

print("\nConfiguring Loopback1 using Python list...")
configure_loopback_1 = connection.send_config_set(loopback_1_config)
print(configure_loopback_1)

"""
Send Configuration to Device using File
'send_config_from_file()' method calls a file containing pre-written configuration
"""

loopback_2_config = os.path.join(directory,"configure_loopback2.txt")

print("\nConfiguring Loopback2 using File...")
configure_loopback_2 = connection.send_config_from_file(loopback_2_config)
print(configure_loopback_2)

"""
Verify configurations
"""

print("\nVerifying configuration...")
verify_loopback1 = connection.send_command("show run interface Loopback1")
print(verify_loopback1)

verify_loopback2 = connection.send_command("show run interface Loopback2")
print(verify_loopback2)

"""
Save configuration
"""

print("\n Saving configuration...")
print(connection.save_config())

"""
Gracefully close SSH connection
"""

connection.disconnect()