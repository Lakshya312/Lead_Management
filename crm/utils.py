from datetime import datetime
import traceback

def log_error(error):

    tb = traceback.extract_tb(
        error.__traceback__
    )[-1]

    with open(
        "error_log.txt",
        "a"
    ) as f:

        f.write(
            f"\n{'=' * 60}\n"
            f"Time        : {datetime.now()}\n"
            f"Error Type  : {type(error).__name__}\n"
            f"Message     : {str(error)}\n"
            f"File        : {tb.filename}\n"
            f"Function    : {tb.name}\n"
            f"Line Number : {tb.lineno}\n"
            f"{'=' * 60}\n"
        )