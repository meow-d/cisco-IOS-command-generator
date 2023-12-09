from textwrap import dedent
from io import StringIO
import ipaddress
import argparse
import math
import sys

import markdown
import pandas as pd
from bs4 import BeautifulSoup, Tag


def parse_table(markdown_text):
    html_table = StringIO(markdown.markdown(markdown_text, extensions=["tables"]))

    soup = BeautifulSoup(html_table.getvalue(), "html.parser")
    for element in soup.recursiveChildGenerator():
        if isinstance(element, Tag):
            if element.name not in ["table", "thead", "tbody", "tr", "th", "td"]:
                raise ValueError("Your markdown should contain only the table")

    data = pd.read_html(html_table)[0]
    data.set_index("name", inplace=True)
    data = data.groupby("type")
    return data


def generate_commands(data, provided_address):
    network_address = provided_address
    commands = ""

    # Sort data by device type
    data = sorted(data, key=lambda x: x[0] != "switch")

    for device_type, data_group in data:
        commands = commands + dedent(
            f"""
            ## {device_type}
            """
        )

        if device_type == "switch":
            for out_device, data_group in data_group.groupby("out_device"):
                commands = commands + dedent(
                    f"""
                    ### {out_device}
                    en
                    conf t

                    router rip
                    version 2
                    no auto-summary
                    exit
                    """
                )

                for index, row in data_group.iterrows():
                    # subnet calculations
                    hosts_count = int(row["hosts"])
                    min_power_of_2 = math.ceil(math.log2(hosts_count + 1))
                    network_size = int(2**min_power_of_2)
                    subnet_mask_bits = 32 - min_power_of_2
                    subnet_mask = (
                        ipaddress.ip_address("255.255.255.255") - network_size + 1
                    )

                    # address calculations
                    network = ipaddress.ip_network(
                        str(network_address) + "/" + str(subnet_mask_bits),
                        strict=False,
                    )
                    first_usable_address = next(network.hosts())
                    second_usable_address = next(network.hosts())

                    # for the next network
                    network_address = (
                        ipaddress.ip_address(network_address) + network_size
                    )

                    commands = commands + dedent(
                        f"""
                        interface {row['out_port']}
                        ip address {first_usable_address} {subnet_mask}
                        no shutdown
                        exit

                        ip dhcp pool {index}
                        network {network.network_address} {subnet_mask}
                        default-router {first_usable_address}
                        exit

                        router rip
                        network {network.network_address}
                        exit
                        """
                    )

                commands = commands + dedent(
                    """
                    exit
                    exit
                    """
                )

        elif device_type == "router":
            for out_device, data_group in data_group.groupby("out_device"):
                commands = commands + dedent(
                    f"""
                    ### {out_device}
                    en
                    conf t

                    line con 0
                    password cisco
                    login
                    exit

                    enable password cisco
                    service password-encryption
                    enable secret cisco

                    banner motd #Authorized personnel only#
                    """
                )

                for index, row in data_group.iterrows():
                    # subnet calculations
                    hosts_count = int(row["hosts"])
                    min_power_of_2 = math.ceil(math.log2(hosts_count + 1))
                    network_size = int(2**min_power_of_2)
                    subnet_mask_bits = 32 - min_power_of_2
                    subnet_mask = (
                        ipaddress.ip_address("255.255.255.255") - network_size + 1
                    )

                    # address calculations
                    network = ipaddress.ip_network(
                        str(network_address) + "/" + str(subnet_mask_bits),
                        strict=False,
                    )
                    first_usable_address = next(network.hosts())
                    second_usable_address = next(network.hosts())

                    # for the next network
                    network_address = (
                        ipaddress.ip_address(network_address) + network_size
                    )

                    commands = commands + dedent(
                        f"""
                        interface {row['out_port']}
                        ip address {first_usable_address} {subnet_mask}
                        no shutdown
                        exit

                        interface {row['in_port']}
                        ip address {second_usable_address} {subnet_mask}
                        no shutdown
                        exit

                        router rip
                        network {network.network_address}
                        exit
                        """
                    )

                commands = commands + dedent(
                    """
                    router rip
                    default-information originate
                    exit

                    exit
                    exit
                    """
                )

    return commands


def main():
    parser = argparse.ArgumentParser(
        description="Generates Cisco IOS commands to setup subnets, DHCP, and RIP"
    )
    parser.add_argument(
        "input_table",
        metavar="input-table",
        help="input markdown file. should contain only the input table",
    )
    parser.add_argument("address", help="the ip address space you're given. ipv4 only")
    args = parser.parse_args()

    try:
        with open(args.input_table, "r", encoding="utf-8") as f:
            markdown_text = f.read()
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

    try:
        data = parse_table(markdown_text)
    except ValueError as e:
        print(e)
        sys.exit(1)
    except ModuleNotFoundError as e:
        print(e)
        print(
            "If you get this error, your markdown likely contains something other than the table"
        )
        print("Your markdown should contain only the table")
        sys.exit(1)

    try:
        address = ipaddress.IPv4Address(args.address)
    except ValueError:
        print("Invalid IPv4 address")
        sys.exit(1)

    commands = generate_commands(data, address)
    print(commands)


if __name__ == "__main__":
    main()
