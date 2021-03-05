import thermal
import error_signaling
import rfid_reader

def placeholder_database_check() -> int:
    return 2

def main() -> None:

    tags = []

    input("Press enter to start")

    while True:
        people_inside_range, people_outside_range = thermal.get_frame_data()

        if people_inside_range > 0:
            tags = rfid_reader.call_reader()
            if len(tags) != people_inside_range or not placeholder_database_check(tags):
                error_signaling.errorFlash()

if '__name__' == '__main__':
    main()
