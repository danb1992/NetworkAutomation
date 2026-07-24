from netmiko import ConnectHandler
from getpass import getpass


# TODO:
# Create a dictionary w/ site-id:ip-address key-value pairs
# Utilize dictionary instead of needing to know device IP address
# Convert (if possible) lines 10-20 to a function or class

ip = input("IP Address: ")
username = input("Username: ")
password = getpass("Password: ",echo_char="*")

device = {
    "device_type": "cisco_ios",
    "ip": ip,
    "username": username,
    "password": password,
    "port": 22
}

def main():
    """
    Contains functions that gather outputs for baseline troubleshooting.
    """
    verify_control_connections() # Checks SD-WAN control connections to Manager (vManage) and Controller (vSmart)
    verify_ping_wan_to_google_dns() # Pings 8.8.8.8 from Transport VPN 0 interfaces
    verify_sig_tunnels() # Checks SIG tunnel status
    verify_overlay_default_route() # Checks where 0.0.0.0/0 route is learned from/routing to
    verify_overlay_arp_table() # Checks ARP entries for Service VPN

    """
    While Loop: Asks if user wants to perform additional CLI commands
    """
    while True:
        choice = str(input("Would you like to run any additional checks? [y/n] ")).strip().lower()
        if choice == "y":
            additional_commands() # Allows additional commands to be inputted
        elif choice == "n":
            print("Closing session...")
            break # Exits the program
        else:
            print("invalid input")


def verify_control_connections():
    print("Gathering SD-WAN control connection status...") # Prompts user on what step is being performed
    with ConnectHandler(**device) as net_connect:
        ctrl_connections = net_connect.send_command("show sdwan control connections")
        print(ctrl_connections)


def verify_ping_wan_to_google_dns():
    print("Please provide VPN 0 interface names...\n")
    intf_1 = str(input("First VPN 0 interface (ex: gi0/0/0): "))
    intf_2 = str(input("Second VPN 0 interface (ex: gi0/0/1): "))
    
    print("Pinging 8.8.8.8 from VPN 0 source interfaces...")
    with ConnectHandler(**device) as net_connect:
        ping_intf_1 = net_connect.send_command(f"ping 8.8.8.8 source {intf_1} repeat 20")
        print(ping_intf_1)
        ping_intf_2 = net_connect.send_command(f"ping 8.8.8.8 source {intf_2} repeat 20")
        print(ping_intf_2)


def verify_sig_tunnels():
    print("Gathering SIG tunnel status...")
    with ConnectHandler(**device) as net_connect:
        sig_status = net_connect.send_command("show sdwan secure-internet-gateway tunnels")
        print(sig_status)


def verify_overlay_default_route():
    print("Please provide Service VPN number...\n")
    service_vpn = str(input("Service VPN number (ex: 10): "))

    print(f"Validating default route for Service VPN {service_vpn}...")
    with ConnectHandler(**device) as net_connect:
        default_route = net_connect.send_command(f"show ip route vrf {service_vpn} 0.0.0.0")
        print(default_route)


def verify_overlay_arp_table():
    print("Please provide Service VPN number...\n")
    service_vpn = str(input("Service VPN number (ex: 10): "))

    print(f"Validating ARP entries for Service VPN {service_vpn}...")
    with ConnectHandler(**device) as net_connect:
        arp_service_vpn = net_connect.send_command(f"show ip route vrf {service_vpn} 0.0.0.0")
        print(arp_service_vpn)


def additional_commands():
    command = str(input("Please input 'show' command here: "))
    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command(command)
        print(output)


if __name__ == "__main__":
    main()