#import lib.thermal as thermal
import lib.error_signaling as error_signaling
import lib.rfid_reader as rfid_reader
#import lib.database as database
from time import sleep

def main() -> None:
    tags = []

    error_signaling.setGreen()

    while True:
        db_check = input("Pass database check y/n: ").lower() == 'y'
        people_inside_range = int(input("Number of people inside range: "))

        print("Getting Thermal data")
        #people_inside_range, people_outside_range = thermal.get_frame_data()

        print(f"People inside range: {people_inside_range}")

        if people_inside_range > 0:
            print("People detected")
            tags = rfid_reader.call_reader()
            print(f"Tags detected: {tags}")
            #if len(tags) == people_inside_range and readTicketList(tags):
            if len(tags) == people_inside_range and db_check:
                sleep(2)
                print("Successful loop!\n")
            else:
                print("Error detected\n")
                error_signaling.errorFlash()

main()
