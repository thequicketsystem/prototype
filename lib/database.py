import mariadb
import sys

def helloDB():
    #set up our db connection
    try:
        conn = mariadb.connect(
        user="root",
        password="quicket",
        host="localhost",
        database="quicketsystem")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
        
    return conn

#function to read out incoming tickets
def readTicket(incomingID):
    conn = helloDB()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT used FROM guests WHERE ticketID=%d;", (int(incomingID),))
        result = cur.fetchall()[0][0]
        print(result)
        print(type(result))
        if result == 0:
        #working - sets used bit to 1
            cur.execute("UPDATE guests SET used=1 WHERE ticketID=%d AND used=0;", (int(incomingID),))
            conn.commit()
            print(incomingID, "has been set to USED.")

        #try to check if it's already used
        #cur.execute("SELECT ROW_COUNT();")
        #result = cur.fetchall()[0][0]
        #if result == 0:
        #    print(incomingID, "has been set to USED.")
        else:
            print(f"ERROR: DUPLICATE TICKET ENTRY")
    except mariadb.Error as e:
        print(f"Error updating ticket: {e}")
        sys.exit(1)
    print(f"returning")
    conn.close()


#function to set all used fields to 0 for testing purposes
def clearUsed():
    conn = helloDB()
    cur = conn.cursor()
    
    values = [123,234,345,456,567]
    
    try:
        for item in values:
            cur.execute("UPDATE guests SET used=0 WHERE ticketID=?",(item,))
            conn.commit()
            print(f"ID reset: {item}")
    except mariadb.Error as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)
        
    conn.close()


#lists the current state of thetable. not working.
def listGuests():
    conn = helloDB()
    cur = conn.cursor()
    print(f"The state of this table is: ")
    query = "SELECT * FROM guests;"
    rows = []
    try:
        cur.execute(query)
        #print([x[0] for x in cur.description])
        rows = cur.fetchall()
        #for line in rows:
        #    print(line)
        #while True:
            #if not rows:
            #    conn.close()
            #print(row)
    except mariadb.Error as e:
        print(f"Error displaying table: {e}")
        sys.exit(1)

    print(f"Returning to main.")
    conn.close()
    return rows


def main():
    #conn = helloDB()

    #establish our cursor
    #print("We have connected to the", conn.database, "database.")
    #print("Server is", conn.server_name)
    #cur = conn.cursor()

    #loop to continuously check tickets against the db
    while True:
        #get an incoming ticket. later this will be real
        incomingID = input("Simlulated ticket is: ")
        
        if (incomingID == "exit") or (incomingID == "end"):
            #LET ME OOOOOOOOOOUT AAAAAAHHHHHHHH
            break
        elif (incomingID == "wipe") or (incomingID == "reset") or (incomingID == "clear"):
            clearUsed()
        elif (incomingID == "show") or (incomingID == "display") or (incomingID == "state"):
            rows = listGuests()
            print(rows)
            #for each in rows:
            #    print(each,"\n")
        #otherwise, read the ticket
        else:
            readTicket(incomingID)

    return

main()
        
