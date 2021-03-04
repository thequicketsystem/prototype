import thermal
import error_signaling

def placeholder_database_and_rfid_stuff() -> int:
    return 2

def main() -> None:
    while True:
        people_inside_range, people_outside_range = thermal.get_frame_data()

        if people_inside_range != placeholder_database_and_rfid_stuff():
            error_signaling.errorFlash()

if '__name__' == '__main__':
    main()
