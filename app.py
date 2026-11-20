from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'enter-password',
    'database': 'shoestoredb'
}

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Shoe Store Management Portal</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 860px; margin: 30px auto; line-height: 1.5; color: #222; }
        .card { border: 1px solid #ccc; padding: 16px; margin-bottom: 18px; border-radius: 5px; }
        h2 { margin-top: 0; font-size: 18px; }
        input { padding: 6px; margin: 4px 6px 4px 0; }
        button { padding: 6px 14px; cursor: pointer; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #999; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .msg { padding: 10px; background: #eef6ff; border-left: 4px solid #0066cc; margin-top: 10px; }
        .err { padding: 10px; background: #ffecec; border-left: 4px solid #cc0000; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>Shoe Store Management Portal</h1>

    <div class="card">
        <h2>Employee Directory Lookup</h2>
        <form method="POST" action="/search_employees">
            <label>Hired On or After:</label>
            <input type="date" name="hire_date" value="{{ hire_date or '2021-01-01' }}" required>
            <button type="submit">Search Employees</button>
        </form>
        {% if emp_err %}<p class="err">{{ emp_err }}</p>{% endif %}
        {% if employees is defined and employees is not none %}
            {% if employees %}
                <table>
                    <tr><th>Employee ID</th><th>Full Name</th><th>Hire Date</th><th>Department</th><th>Floor</th></tr>
                    {% for row in employees %}
                    <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}</td><td>{{ row[4] }}</td></tr>
                    {% endfor %}
                </table>
            {% else %}
                <p class="msg">No employees found hired on or after {{ hire_date }}.</p>
            {% endif %}
        {% endif %}
    </div>

    <div class="card">
        <h2>Register New Customer</h2>
        <form method="POST" action="/add_customer">
            <input type="number" name="customer_id" value="2999" required placeholder="Customer ID">
            <input type="text" name="fname" value="Jordan" required placeholder="First Name">
            <input type="text" name="lname" value="Taylor" required placeholder="Last Name">
            <input type="text" name="phone" value="817-555-2999" placeholder="Phone">
            <input type="email" name="email" value="jordan.taylor@example.com" placeholder="Email">
            <button type="submit">Add Customer</button>
        </form>
        {% if add_msg %}<p class="{{ 'err' if add_err else 'msg' }}">{{ add_msg }}</p>{% endif %}
    </div>

    <div class="card">
        <h2>Update Customer Email</h2>
        <form method="POST" action="/update_email">
            <input type="number" name="customer_id" value="2999" required placeholder="Customer ID">
            <input type="email" name="new_email" value="jtaylor.updated@uta.edu" required placeholder="New Email">
            <button type="submit">Update Email</button>
        </form>
        {% if upd_msg %}<p class="{{ 'err' if upd_err else 'msg' }}">{{ upd_msg }}</p>{% endif %}
        {% if customer %}
            <table>
                <tr><th>Customer ID</th><th>First Name</th><th>Last Name</th><th>Phone</th><th>Email</th></tr>
                <tr><td>{{ customer[0] }}</td><td>{{ customer[1] }}</td><td>{{ customer[2] }}</td><td>{{ customer[3] }}</td><td>{{ customer[4] }}</td></tr>
            </table>
        {% endif %}
    </div>

    <div class="card">
        <h2>Remove Customer Record</h2>
        <form method="POST" action="/delete_customer">
            <input type="number" name="customer_id" value="2999" required placeholder="Customer ID">
            <button type="submit">Delete Customer</button>
        </form>
        {% if del_msg %}<p class="{{ 'err' if del_err else 'msg' }}">{{ del_msg }}</p>{% endif %}
    </div>
</body>
</html>
"""

def get_db():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template_string(html)

@app.route('/search_employees', methods=['POST'])
def search_employees():
    hire_date = request.form['hire_date']
    try:
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT e.Emp_ID, CONCAT(e.Fname, ' ', e.Lname), e.Hire_Date, d.Dept_Name, d.Floor_No
            FROM EMPLOYEE e
            JOIN DEPARTMENT d ON e.Dept_ID = d.Dept_ID
            WHERE e.Hire_Date >= %s
            ORDER BY e.Hire_Date
        """
        cursor.execute(query, (hire_date,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template_string(html, employees=rows, hire_date=hire_date)
    except mysql.connector.Error as err:
        return render_template_string(html, emp_err=f"Database Error: {err}", hire_date=hire_date)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    cid = request.form['customer_id']
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    email = request.form['email']
    try:
        conn = get_db()
        cursor = conn.cursor()
        query = "INSERT INTO CUSTOMER (Customer_ID, Fname, Lname, Phone, Email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (cid, fname, lname, phone, email))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template_string(html, add_msg=f"Customer {cid} ({fname} {lname}) has been added.")
    except mysql.connector.Error as err:
        return render_template_string(html, add_msg=f"Database Error: {err}", add_err=True)

@app.route('/update_email', methods=['POST'])
def update_email():
    cid = request.form['customer_id']
    new_email = request.form['new_email']
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE CUSTOMER SET Email = %s WHERE Customer_ID = %s", (new_email, cid))
        conn.commit()
        cursor.execute("SELECT Customer_ID, Fname, Lname, Phone, Email FROM CUSTOMER WHERE Customer_ID = %s", (cid,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()
        if record:
            return render_template_string(html, upd_msg=f"Email updated for Customer ID {cid}.", customer=record)
        return render_template_string(html, upd_msg=f"No customer found with ID {cid}.", upd_err=True)
    except mysql.connector.Error as err:
        return render_template_string(html, upd_msg=f"Database Error: {err}", upd_err=True)

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    cid = request.form['customer_id']
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CUSTOMER WHERE Customer_ID = %s", (cid,))
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        if deleted > 0:
            return render_template_string(html, del_msg=f"Customer ID {cid} has been deleted from the database.")
        return render_template_string(html, del_msg=f"Customer ID {cid} does not exist.", del_err=True)
    except mysql.connector.Error as err:
        return render_template_string(html, del_msg=f"Database Error: {err}", del_err=True)

if __name__ == '__main__':
    app.run(port=5050, debug=True)
