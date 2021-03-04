import thermal
import error_signaling

def main() -> None:
    while True:
        print(thermal.get_frame_data())

if '__name__' == '__main__':
    main()
    
    

