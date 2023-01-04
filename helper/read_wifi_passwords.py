import subprocess
from rich.console import Console
from rich.table import Table

def find_networks():
    raw_output = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles'])
    result = parse_output(raw_output, "All User Profile")
    return result


def find_passwords(networks):
    network_passwords = {}
    for network in networks:
        raw_output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles', network, 'key=clear'])
        result = parse_output(raw_output, "Key Content")

        if len(result) == 1:
            network_passwords[network] = result[0]
        else:
            network_passwords[network] = "***missing***"

    return network_passwords


def parse_output(raw_output, identifier):
    output = raw_output.decode('cp1252', errors="backslashreplace")
    lines = output.split('\n')

    matches = []

    for line in lines:
        if identifier in line:
            parts = line.split(":")
            value = parts[1][1:-1]
            matches.append(value)
            
    return matches


def display_networks(passwords):
    table = Table(title="Wi-Fi network passwords")

    table.add_column("Network")
    table.add_column("Password")

    for key, value in passwords.items():
        table.add_row(key, value)

    console = Console()
    console.print(table)

if __name__ == '__main__':
    networks = find_networks()
    passwords = find_passwords(networks)
    display_networks(passwords)
