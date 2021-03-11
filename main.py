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
            
            if len(tags) != people_count:
                print(f"Error detected: Number of tags does not match number of people!")
                error_signaling.errorFlash()
            
            if any(x == False for x in database.readTicketList(tags)):
                print(f"Error detected: Invalid tag!")
                error_signaling.errorFlash()
                
            else:
                print("Successful loop!\n")

main()
