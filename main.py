import lib.thermal as thermal
import lib.error_signaling as error_signaling
import lib.rfid_reader as rfid_reader
import lib.database as database
from time import sleep
from concurrent.futures import ProcessPoolExecutor

# Defines length of time to wait before checking
# process status. Set to 5ms for now
POLLING_DELAY = 0.005

def get_best_of_five() -> int:
  return thermal.get_best_of_x(5)

def main() -> None:
    error_signaling.setGreen()
    
    people_count = 0
    tags = []

    with ProcessPoolExecutor(max_workers=2) as executor:
        while True:
            # TODO: This is super messy and seriously needs to be redone but
            # it should work for now. Circle back for improvement
            # if it actually does work.
            frame_data_future = executor.submit(get_best_of_five)
            rfid_data_future = executor.submit(rfid_reader.call_reader)

            while True:
                if rfid_data_future.done():
                    tags = rfid_data_future.result()

                    # Always check this first since this data is always available
                    if any(x == False for x in database.readTicketList(tags)):
                        print(f"Error detected: Invalid/Used tag!")
                        error_signaling.errorFlash()
                    
                    # Then check this
                    elif len(tags) != frame_data_future.result():
                        print(f"Error detected: Number of tags does not match number of people!")
                        error_signaling.errorFlash()
                    
                    break

                else:
                    sleep(POLLING_DELAY)

main()
