import re
import os


def get_indentation(line):
    return len(line) - len(line.lstrip(' '))


def _yaml_single_quote(value):
    # YAML single-quoted scalar escaping: single quote becomes doubled.
    return "'" + value.replace("'", "''") + "'"


def _entry_key_from_line(line):
    stripped = line.strip()
    if not stripped.endswith(':'):
        return None
    key = stripped[:-1].strip()
    if len(key) >= 2 and key[0] == "'" and key[-1] == "'":
        return key[1:-1].replace("''", "'")
    if len(key) >= 2 and key[0] == '"' and key[-1] == '"':
        return key[1:-1].replace('\\"', '"')
    return key


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

    entry_indent = access_points_indentation + 4
    password_indent = access_points_indentation + 8

    quoted_ssid = _yaml_single_quote(new_ssid)
    quoted_password = _yaml_single_quote(new_password)
    new_ssid_line = f"{' ' * entry_indent}{quoted_ssid}:\n"
    new_password_line = f"{' ' * password_indent}password: {quoted_password}\n"

    new_config_lines = []
    inserted = False

    i = 0
    while i < len(config_lines):
        line = config_lines[i]

        if i == access_points_line_index:
            new_config_lines.append(line)
            if not inserted:
                new_config_lines.append(new_ssid_line)
                new_config_lines.append(new_password_line)
                inserted = True
            i += 1
            continue

        indent = get_indentation(line)
        key = _entry_key_from_line(line)
        if indent == entry_indent and key == new_ssid:
            # Skip the existing SSID block so we can replace it with the latest credentials.
            i += 1
            while i < len(config_lines):
                next_line = config_lines[i]
                if next_line.strip() == '':
                    i += 1
                    continue
                if get_indentation(next_line) <= entry_indent:
                    break
                i += 1
            continue

        new_config_lines.append(line)
        i += 1


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
