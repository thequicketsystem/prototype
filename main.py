import lib.thermal as thermal
import lib.error_signaling as error_signaling
import lib.rfid_reader as rfid_reader
import lib.database as database
from time import sleep

def main() -> None:
    tags = []

    error_signaling.setGreen()

    while True:

        print("Getting Thermal data")
        people_count = thermal.get_frame_data()

        print(f"People count: {people_count}")

        if people_count > 0:
            print("People detected")
            tags = rfid_reader.call_reader()
            print(f"Tags detected: {tags}")
            # Right now this is inefficient but later we will probably use the
            #  list from readTicketList() to determine *which* tag is invalid 
            if len(tags) == people_count and all(x == True for x in database.readTicketList(tags)):
                print("Successful loop!\n")
                sleep(2)
            else:
                print("Error detected\n")
                error_signaling.errorFlash()

main()
