from flask import Flask, request, render_template, redirect, url_for, session, flash
import pyodbc

# Connection settings
server = 'LAPTOP-QAGIH0DN'
database = 'HOSPITALITY_MANAGEMENT_SYSTEM'
driver = '{SQL Server}'

# Connect to the database
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database}')
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_login(username, password):
            session['username'] = username
            return redirect(url_for('menu2'))
        else:
            flash("Invalid Username or Password!")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_new_user(username, password)
        flash("User registered successfully!")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/menu2')
def menu2():
    if 'username' in session:
        return render_template('menu2.html')
    return redirect(url_for('login'))

@app.route('/check_availability', methods=['POST'])
def check_availability():
    room_id = int(request.form['room_id'])
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = check_room_availability(room_id, start_date, end_date)
    if status == 0:
        message = 'Room Available for Reservation!'
    else:
        message = 'Already Booked! Room Not Available for Reservation.'
    return render_template('menu2.html', message=message)

@app.route('/make_reservation', methods=['POST'])
def make_reservation_route():
    room_id = int(request.form['room_id'])
    user_name = session['username']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = check_room_availability(room_id, start_date, end_date)
    if status == 0:
        rows_affected = make_reservation(room_id, user_name, start_date, end_date)
        message = f"Reservation successful, {rows_affected} row(s) affected"
    else:
        message = "Room Already Booked."
    return render_template('menu2.html', message=message)

@app.route('/generate_bill', methods=['POST'])
def generate_bill_route():
    user_id = int(request.form['user_id'])
    total = generate_bill(user_id)
    return render_template('menu2.html', message=f"Total Amount Payable: {total}")

@app.route('/register_room', methods=['POST'])
def register_room_route():
    admin_username = request.form['admin_username']
    admin_password = request.form['admin_password']
    if admin_username == 'Admin' and admin_password == 'admin@123':
        hotel_name = request.form['hotel_name']
        room_number = request.form['room_number']
        room_type = request.form['room_type']
        price = int(request.form['price'])
        room = register_room(hotel_name, room_number, room_type, price)
        if room == 0:
            message = "Entry Not Made!"
        else:
            message = "Room Registered Successfully!"
    else:
        message = "Invalid Admin Credentials."
    return render_template('menu2.html', message=message)

@app.route('/check_in', methods=['POST'])
def check_in_route():
    reservation_id = int(request.form['reservation_id'])
    check_in_date = request.form['check_in_date']
    check_in(reservation_id, check_in_date)
    return render_template('menu2.html', message="Check-in date updated successfully.")

@app.route('/check_out', methods=['POST'])
def check_out_route():
    reservation_id = int(request.form['reservation_id'])
    check_out_date = request.form['check_out_date']
    check_out(reservation_id, check_out_date)
    return render_template('menu2.html', message="Check-Out date updated successfully.")

# Utility functions (adapted from the original script)

def check_room_availability(room_id, start_date, end_date):
    cursor.execute("{CALL AVAILABILITY_CHECK (?, ?, ?)}", room_id, start_date, end_date)
    result = cursor.fetchone()
    return result[0] if result else "Error checking availability"

def make_reservation(room_id, user_name, start_date, end_date):
    cursor.execute("{CALL MAKE_RESERVATION (?, ?, ?, ?)}", room_id, user_name, start_date, end_date)
    conn.commit()
    return cursor.rowcount

def generate_bill(user_id):
    cursor.execute("{ CALL GENERATEBILL (?) }", user_id)
    bill = cursor.fetchall()
    return bill[0][0]

def register_room(hotel_name, room_number, room_type, price):
    cursor.execute("{CALL REGISTERROOM (?,?,?,?)}", hotel_name, room_number, room_type, price)
    conn.commit()
    return cursor.rowcount

def validate_login(username, password):
    cursor.execute("{ CALL UserLogin (?, ?) }", username, password)
    b = cursor.fetchone()
    return b[0] == 0

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

if __name__ == '__main__':
    app.run(debug=True)
