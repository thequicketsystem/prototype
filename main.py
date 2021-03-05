import thermal
import error_signaling
import rfid_reader

def placeholder_database_check(tags) -> int:
    return 0

def main() -> None:
    tags = []

    input("Press enter to start")

    print("Start of main loop")
    while True:
        print("Getting Thermal data")
        #people_inside_range, people_outside_range = thermal.get_frame_data()
        people_inside_range = 2
        people_outside_range = 2

        print(f"People inside range: {people_inside_range}\nPeople outside range: {people_outside_range}")

        if people_inside_range > 0:
            print("People detected")
            tags = rfid_reader.call_reader()
            print(f"Tags detected: {tags}")
            #if len(tags) != people_inside_range or not placeholder_database_check(tags):
            if len(tags) != people_inside_range
                print("Error Detected, tags != people inside range!")
                error_signaling.errorFlash()
            if placeholder_database_check(tags):
                print("Error Detected, tags invalid or used!")
                error_signaling.errorFlash()

            print("Successful loop")

if '__name__' == '__main__':
    main()
