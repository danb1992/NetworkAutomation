from netmiko import ConnectHandler
from getpass import getpass


# Device List for 'show' commands

device_list_sh = [
    "192.168.0.27", # S1-2960
    "192.168.0.223", # R1-11006G
    "192.168.0.166", # R2-4331
]

# Device List for 'config' commands
# ISR 1100-6G is excluded from 'device_list_cfg' because it is an SD-WAN cEdge Router
# with different config syntax

device_list_cfg = [
    "192.168.0.27", # S1-2960
    "192.168.0.166", # R2-4331
]

login_info = {
    "username": input("Username: "),
    "password": getpass("Password: "),
}

# S1-2960X Loopback10 Configuration

s1_loopback_cfg = [
    "interface Loopback10",
    "description Configured with Netmiko - MultiDevice Config",
    "ip address 10.0.0.1 255.255.255.255",
    "no shutdown"
]

# R2-4331 Loopback10 Configuration

r2_loopback_cfg = [
    "interface Loopback10",
    "description Configured with Netmiko - MultiDevice Config",
    "ip address 10.0.0.3 255.255.255.255",
    "no shutdown"
]

# For loop for 'configuration' commands

for device in device_list_cfg:

    connection = ConnectHandler(
        ip = device,
        device_type = "cisco_ios",
        username = login_info["username"],
        password = login_info["password"],
        port = 22
    )

    if device == "192.168.0.27":

        print("\nConfiguring Loopback10 Interface for 'S1-2960X'...")
        output = connection.send_config_set(s1_loopback_cfg)
        print(connection.find_prompt(),output)

    elif device == "192.168.0.166":

        print("\nConfiguring Loopback10 Interface for 'R2-4331'...")
        output = connection.send_config_set(r2_loopback_cfg)
        print(connection.find_prompt(),output)

    else:

        print("\nMismatched IP address")


# For loop for 'show' commands

for device in device_list_sh:

    connection = ConnectHandler(
        ip = device,
        device_type = "cisco_ios",
        username = login_info["username"],
        password = login_info["password"],
        port = 22
    )

    print("\nPrinting IP Interfaces...")
    output = connection.send_command("show ip int br | exc unassigned",strip_command=False)
    print(connection.find_prompt(),output)

    connection.save_config()

    connection.disconnect()