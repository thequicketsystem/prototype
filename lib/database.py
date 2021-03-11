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

#function to read single ticket
def readTicket(incomingID: str) -> bool:
    conn = helloDB()
    cur = conn.cursor()

    result = None
    
    try:
        cur.execute("SELECT used FROM guests WHERE ticketID=%s;", (incomingID,))
        result = cur.fetchall()[0][0]
        if result == 0:
            #working - sets used bit to 1
            cur.execute("UPDATE guests SET used=1 WHERE ticketID=%s;", (incomingID,))
            conn.commit()
            result = True

        else:
            result = False

    except mariadb.Error as e:
        print(f"Error updating ticket: {e}")
        conn.close()
        sys.exit(1)

    conn.close()
    return result

def readTicketList(incomingIDs: list) -> None:
    results = []
    for each in incomingIDs:
        results.append(readTicket(each))

    return results
