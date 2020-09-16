import psutil
import time
import os
from os import path


# track the length of high memeory usage
def trackOccurance():
    
    while True:
        if psutil.virtual_memory().percent > 80:
        break

# regular memory tracking
def trackMemory():
    while True:
        counter = 0
        # you can have the percentage of used RAM eg. 79.2
        if psutil.virtual_memory().percent > 80:
            if counter == 10:
                
            counter += 1
            time.sleep(1)

if __name__ == "__main__":
    # initialize var/log folder
    if not path.isdir("/var/log/memorymonitor"):
        os.mkdir("/var/log/memorymonitor")
    trackMemory()