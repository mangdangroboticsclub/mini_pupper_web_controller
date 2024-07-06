import subprocess
import sys

from backend.settings import shell, wifi

def exe_setting(command, params):
    if command == "shell_cmd":
        exe_cmd = f"sudo {params}"
        shell.execute_command(exe_cmd)
    else: ## set wifi ssid and passwd
        config_path = "/etc/netplan/50-cloud-init.yaml"
        wifi.insert_ssid_password(command, params, config_path, config_path)

    return {"command": command, "params": params}


def main():
    import logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
        level=logging.INFO
    )

    while True:
        user_input = input("input <ssid passwd> or 'shell_cmd <command>' or 'exit': ").strip().lower()
         
        if not user_input:
            continue
        if user_input == 'exit':
            logging.info("Exit!")
            break
        inputs = user_input.split("20%")
        if len(inputs) <= 1:
            logging.info("at least 2 words")
            continue
        command = inputs[0]
        params = ' '.join(inputs[1:])
        exe_setting(command, params)



if __name__ == '__main__':
    main()
