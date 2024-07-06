import re
import os


def get_indentation(line):
    return len(line) - len(line.lstrip(' '))


def insert_ssid_password(new_ssid, new_password, input_file_path="/etc/netplan/50-cloud-init.yaml", output_file_path="/home/ubuntu/50-cloud-init.yaml.new"):
    with open(input_file_path, 'r') as file:
        config_lines = file.readlines()

    access_points_line_index = -1
    for i, line in enumerate(config_lines):
        if 'access-points:' in line:
            access_points_line_index = i
            break

    if access_points_line_index == -1:
        raise ValueError("The 'access-points' line was not found in the configuration.")

    access_points_indentation = get_indentation(config_lines[access_points_line_index])

    new_ssid_line = f"{' ' * (access_points_indentation + 4)}{new_ssid}:\n"
    new_password_line = f"{' ' * (access_points_indentation + 8)}password: {new_password}\n"

    new_config_lines = []
    inserted = False
    skip_password_line = False

    for line in config_lines:
        if skip_password_line:
            skip_password_line = False
            continue

        if re.match(r'^\s*' + re.escape(new_ssid) + r':\s*$', line):
            next_line = config_lines[config_lines.index(line) + 1]
            if "password" in next_line:
                skip_password_line = True
                continue

        new_config_lines.append(line)
        if 'access-points:' in line and not inserted:
            new_config_lines.append(new_ssid_line)
            new_config_lines.append(new_password_line)
            inserted = True


    with open(output_file_path, 'w') as file:
        file.writelines(new_config_lines)

    return {"ssid": new_ssid, "password": new_password}


import argparse

def main():
    parser = argparse.ArgumentParser(description='Update Wi-Fi credentials')

    parser.add_argument('--ssid', type=str, required=True, help='New SSID for Wi-Fi')

    parser.add_argument('--passwd', type=str, required=True, help='New password for Wi-Fi')

    parser.add_argument('--input', type=str, default='/home/ubuntu/net.yaml',
                        help='Path to the Netplan configuration file')

    parser.add_argument('--output', type=str, default='/home/ubuntu/net.yaml.new',
                        help='Path to the Netplan configuration file')
    args = parser.parse_args()

    #update_wifi_credentials(args.ssid, args.passwd, args.path)
    insert_ssid_password(args.ssid, args.passwd, args.input, args.output)

if __name__ == "__main__":
    main()
