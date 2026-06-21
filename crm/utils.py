from datetime import datetime

def log_error(error):
    with open("error_log.txt", "a") as file:
        file.write(
            f"{datetime.now()} : {type(error).__name__} : {str(error)}\n"
        )