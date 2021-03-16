import lib.thermal as thermal
import lib.error_signaling as error_signaling
import lib.rfid_reader as rfid_reader
import lib.database as database
from time import sleep
from concurrent.futures import ProcessPoolExecutor

def main() -> None:
    tags = []

    error_signaling.setGreen()

    with ProcessPoolExecutor(max_workers=1) as executor:
        frame_data_future = executor.submit(thermal.get_best_of_three)

        while True:
            people_count = frame_data_future.result()
            executor.submit(thermal.get_best_of_three)
            print(f"People count: {people_count}")

            if people_count > 0:
                tags = rfid_reader.call_reader()
                print(f"People detected, read tags: {tags}")
                
                if len(tags) != people_count:
                    print(f"Error detected: Number of tags does not match number of people!")
                    error_signaling.errorFlash()
                
                if any(x == False for x in database.readTicketList(tags)):
                    print(f"Error detected: Invalid/Used tag!")
                    error_signaling.errorFlash()
                    
                else:
                    print("Successful loop!\n")

main()
