import argparse

from io import StringIO
import markdown

from textwrap import dedent
import pandas as pd


def parse_table(markdown_text):
    html_table = StringIO(markdown.markdown(markdown_text, extensions=["tables"]))
    data = pd.read_html(html_table)[0]
    data.set_index("name", inplace=True)
    data = data.groupby("type")
    return data


def generate_commands(data):
    commands = ""

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
                    commands = commands + dedent(
                        f"""
                        interface {row['out_port']}
                        ip address {row['first_usable_address']} {row['subnet_mask']}
                        no shutdown
                        exit

                        ip dhcp pool {index}
                        network {row['network_address']} {row['subnet_mask']}
                        default-router {row['first_usable_address']}
                        exit

                        router rip
                        network {row['network_address']}
                        exit
                        """
                    )

                commands = commands + dedent(
                    f"""
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
                    commands = commands + dedent(
                        f"""
                        interface {row['out_port']}
                        ip address {row['first_usable_address']} {row['subnet_mask']}
                        no shutdown
                        exit

                        interface {row['in_port']}
                        ip address {row['second_usable_address']} {row['subnet_mask']}
                        no shutdown
                        exit

                        router rip
                        network {row['network_address']}
                        exit
                        """
                    )

                commands = commands + dedent(
                    f"""
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
        "filename", help="input markdown file. should contain only the input table"
    )
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        markdown_text = f.read()
    data = parse_table(markdown_text)
    commands = generate_commands(data)
    print(commands)


if __name__ == "__main__":
    main()
