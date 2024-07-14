import pyodbc

# Connection settings
server = 'LAPTOP-QAGIH0DN'
database = 'HOSPITALITY_MANAGEMENT_SYSTEM'
driver = '{SQL Server}'

# Connect to the database
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database}')
cursor = conn.cursor()


def menu():
    print('Welcome to the Software!')
    print('Please select: ')
    print('1: Existing User\n2: New User')
    a = int(input('Enter your choice: '))
    if a == 1:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        log = login(username, password)
        if log == 0:
            print("Successfully Logged In!")
            print(f"Welcome {username}")
            menu2()
        else:
            print("Invalid Username or Password!")
    elif a == 2:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        add_new_user(username, password)
        menu()
    else:
        print('Invalid Input!')
        menu()


def menu2():
    print('1: Check Room Availability ')
    print('2: Make Reservation ')
    print('3: Generate Bill ')
    print('4: Register a Room in Database (*Only for Admin) ')
    print('5: Check In ')
    print('6: Check Out')
    print('7: Exit')
    choice = int(input("Enter choice: "))

    if choice == 1:
        room_id = int(input("Enter Room ID: "))
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")
        status = check_room_availability(room_id, start_date, end_date)
        if status == 0:
            print('Room Available for Reservation!')
        else:
            print('Already Booked!\nRoom Not Available for Reservation.')
        menu2()


    elif choice == 2:
        room_id = int(input("Enter Room ID: "))
        user_name = input("Enter User ID: ")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")
        status = check_room_availability(room_id, start_date, end_date)
        if status == 0:
            rows_affected = make_reservation(room_id, user_name, start_date, end_date)
            print(f"Reservation successful, {rows_affected} row(s) affected")
        else:
            print(f"Room Already Booked.")
        menu2()



    elif choice == 3:
        user_id = int(input("Enter the UserID: "))
        total = generate_bill(user_id)
        print("Total Amount Payable:", total)
        menu2()
    


    elif choice == 4:
        admin_username = input("Enter Admin Username: ")
        admin_password = input("Enter Admin Password: ")
        if admin_username == 'Admin' and admin_password == 'admin@123':
            hotel_name = input("Enter Hotel Name: ")
            room_number = input("Enter Room Number: ")
            room_type = input("Enter Room Type: ")
            price = int(input("Enter Price Per Day: "))
            room = register_room(hotel_name, room_number, room_type, price)
            if room == 0:
                print("Entry Not Made!")
            else:
                print('Room Registered Successfully!')
        else:
            print("Invalid Admin Credentials.")
        menu2()




    elif choice == 5:
        reservation_id = int(input("Enter Reservation ID: "))
        check_in_date = input("Enter Check In Date (YYYY-MM-DD): ")
        check_in(reservation_id, check_in_date)
        menu2()



    elif choice == 6:
        reservation_id = int(input("Enter Reservation ID: "))
        check_out_date = input("Enter Check Out Date (YYYY-MM-DD): ")
        check_out(reservation_id, check_out_date)
        menu2()

    
    elif choice==7: 
        print("Thank you!")
        exit()


    else:
        print('Invalid Input!')
        menu2()



#Function for checking room availability

def check_room_availability(room_id, start_date, end_date):
    cursor.execute("{CALL AVAILABILITY_CHECK (?, ?, ?)}", room_id, start_date, end_date)
    result = cursor.fetchone()
    return result[0] if result else "Error checking availability"



#Function for making a reservation

def make_reservation(room_id, user_name, start_date, end_date):
    cursor.execute("{CALL MAKE_RESERVATION (?, ?, ?, ?)}", room_id, user_name, start_date, end_date)
    conn.commit()
    return cursor.rowcount



#Function to generate bill amount

def generate_bill(user_id):
    cursor.execute("{ CALL GENERATEBILL (?) }", user_id)
    bill = cursor.fetchall()
    return bill[0][0]



#Function to register room

def register_room(hotel_name, room_number, room_type, price):
    cursor.execute("{CALL REGISTERROOM (?,?,?,?)}", hotel_name, room_number, room_type, price)
    conn.commit()
    return cursor.rowcount



#Function to login

def login(username, password):
    cursor.execute("{ CALL UserLogin (?, ?) }", username, password)
    b = cursor.fetchone()
    return b[0]



#Function to add new user

def add_new_user(username, password):
    try:
        cursor.execute("{ CALL ADDUSER (?, ?) }", (username, password))
        conn.commit()
        print("User added successfully.")
    except pyodbc.IntegrityError as err:
        if 'Violation of UNIQUE KEY constraint' in str(err):
            print(f"Error: The username '{username}' already exists.")
        else:
            print("Database integrity error:", err)
    except pyodbc.Error as err:
        print("Database error:", err)



#Functiont to check in

def check_in(reservation_id, check_in_date):
    try:
        cursor.execute("{ CALL CheckIn (?, ?) }", (reservation_id, check_in_date))
        conn.commit()
        print("Check-in date updated successfully.")
    except pyodbc.Error as err:
        if err.args[0] == 'HY000' and 'Reservation ID does not exist.' in str(err):
            print("Error: Reservation ID does not exist.")
        else:
            print("Database error:", err)



#Function to check out

def check_out(reservation_id, check_out_date):
    try:
        cursor.execute("{ CALL CheckOut (?, ?) }", (reservation_id, check_out_date))
        conn.commit()
        print("Check-Out date updated successfully.")
    except pyodbc.Error as err:
        if err.args[0] == 'HY000' and 'Reservation ID does not exist.' in str(err):
            print("Error: Reservation ID does not exist.")
        else:
            print("Database error:", err)







menu()
