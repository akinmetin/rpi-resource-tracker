import psutil as _psutil
import time as _time
import os as _os
from datetime import datetime as _dt
import random as _random
import string as _string
import json as _json


def _get_running_processes() -> list:
    '''
    Get running process sorted by the memory usage

    Returns:
        List of running process info
    '''
    process_details = []
    for proc in _psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            process_details.append(pinfo)
        except (
                _psutil.NoSuchProcess,
                _psutil.AccessDenied,
                _psutil.ZombieProcess):
            pass
    process_details = sorted(
        process_details, key=lambda proc: proc['vms'], reverse=True)
    return process_details


def get_random_alphanumeric_string() -> str:
    """
    Generate a random alphanumeric string for unique logging

    Returns:
        10 digits alphanumeric string
    """
    letters_and_digits = _string.ascii_letters + _string.digits
    return ''.join(
        (_random.choice(letters_and_digits) for i in range(10)))


def _write_event_log(event_type: str, event_id: str) -> None:
    """
    Log the high memory usage state changes into the date named log file

    Args:
        type: Event type (START or END)
        event_id: Random event identifier
    """
    now = _dt.now()
    file_name = now.strftime("%d-%m-%Y")
    current_datetime = now.strftime("%d-%m-%Y %H:%M:%S")

    with open("/var/log/memorymonitor/{}.txt".format(file_name),
              "a") as text_file:
        text_file.write(
            "[{}] High Memory Usage started at {}, detailed  process log in "
            "'{}'".format(event_type, current_datetime, event_id))
        text_file.write("\n")


# regular memory tracking
def start_memory_tracking(buffer_time: int = 15) -> None:
    """
    Start tracking the memory usage

    Args:
        buffer_time: Seconds to wait before logging the event
    """
    counter = 0
    event_ended = False
    while True:
        if _psutil.virtual_memory().percent > 80:
            if counter == buffer_time - 1:
                id = get_random_alphanumeric_string()
                _write_event_log("START", id)

                _os.chdir("/var/log/memorymonitor/processes")
                with open("{}.txt".format(id), "a") as text_file:
                    process_list = _get_running_processes()
                    for process in process_list:
                        _json.dump(process, text_file)
                        text_file.write("\n")
                event_ended = True
            counter += 1
            _time.sleep(1)
        elif event_ended:
            _write_event_log("END", id)
            event_ended = False
            counter = 0
    raise RuntimeError("Unexpected error caused the monitoring crash!")


if __name__ == "__main__":
    # initialize log folders
    if not _os.path.isdir("/var/log/memorymonitor"):
        _os.mkdir("/var/log/memorymonitor")

    if not _os.path.isdir("/var/log/memorymonitor/processes"):
        _os.mkdir("/var/log/memorymonitor/processes")

    start_memory_tracking()
