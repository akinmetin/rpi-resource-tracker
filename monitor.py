import psutil
import time
import os
from os import path
from datetime import datetime
import random
import string
import json


def getDate():
    now = datetime.now()
    date_string = now.strftime("%d-%m-%Y")
    return date_string


def getDateTime():
    now = datetime.now()
    date_time_string = now.strftime("%d-%m-%Y %H:%M:%S")
    return date_time_string


def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            # Append dict to list
            listOfProcObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects


def get_random_alphanumeric_string():
    # generate 10 digits random id
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(10)))
    return result_str


# regular memory tracking
def trackMemory():
    counter = 1
    event_ended = False
    while True:
        if psutil.virtual_memory().percent > 80:
            if counter == 15:
                date_string = getDate()
                date_time_string = getDateTime()
                id = get_random_alphanumeric_string()

                # change working dir to /var/log/memorymonitor
                os.chdir("/var/log/memorymonitor")

                print("started")
                # log the beginning of high memory usage
                with open("{}.txt".format(date_string), "a") as text_file:
                    text_file.write("[START] High Memory Usage started at {}, process_log={}".format(date_time_string, id))
                    text_file.write("\n")

                # log running processes according to descending memory usage
                os.chdir("/var/log/memorymonitor/processes")
                with open("{}.txt".format(id), "a") as text_file:
                    process_list = getListOfProcessSortedByMemory()
                    for process in process_list:
                        json.dump(process, text_file)
                        # text_file.write(process)
                        text_file.write("\n")

                event_ended = True

            counter += 1
            time.sleep(1)

        elif event_ended is True:
            date_string = getDate()
            date_time_string = getDateTime()

            # write end date and time
            os.chdir("/var/log/memorymonitor")
            with open("{}.txt".format(date_string), "a") as text_file:
                text_file.write("[END] High Memory Usage ended at {}, process_log={}".format(date_time_string, id))
                text_file.write("\n")

            event_ended = False
            counter = 0


if __name__ == "__main__":
    # initialize log folders
    if not path.isdir("/var/log/memorymonitor"):
        os.mkdir("/var/log/memorymonitor")

    if not path.isdir("/var/log/memorymonitor/processes"):
        os.mkdir("/var/log/memorymonitor/processes")

    trackMemory()
