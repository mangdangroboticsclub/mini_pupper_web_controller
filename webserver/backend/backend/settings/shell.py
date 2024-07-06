import subprocess
import logging

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(e.stderr)

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s',
        level=logging.INFO
    )

    while True:
        user_input = input("input shell command or 'exit': ").strip().lower()
        
        if user_input == 'exit':
           logging.info("Exit!")
           break
        else:
            execute_command(user_input)



if __name__ == '__main__':
    main()
