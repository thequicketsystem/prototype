import serial
import time

# /dev/ttyUSB0 corresponds to the top USB3 port on the rPi 4
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout =.1)

def call_reader():
    tag_IDs = [""]
    first = arduino.write(b'1')
    write2 = 0
    end = 0

    time_start = time.time()

    while end == 0:

        time_now = time.time()

        time_diff = time_now - time_start

        if time_diff > 9:
            break
              
        data = arduino.readline()

        if data:

            proper = data.decode()
        
            if proper == "1234":                # check for message signaling end of read
                print("Reading over")
                break

            if proper[:3] == "e20":                 ## check to see if our tag

                tag_IDs.append((proper[:-2]))

    return tag_IDs[1:]
