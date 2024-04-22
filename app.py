from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# Replace these values with your PostgreSQL credentials
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "karimi2018"
DB_HOST = "localhost"
DB_PORT = "5432"

# Database connection function
def connect_db():
    return psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to display real estate properties
@app.route('/properties', methods=['GET'])
def show_properties():
    try:
        # Connect to the database
        connection = connect_db()
        cursor = connection.cursor()

        # Query to retrieve real estate properties
        query = "SELECT * FROM realestate.real_estate_properties;"
        cursor.execute(query)

        # Fetch all records
        properties = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return render_template('properties.html', properties=properties)

    except Exception as e:
        return str(e)

# Route to add a new real estate property (GET and POST)
@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'GET':
        return render_template('add_property.html')
    elif request.method == 'POST':
        try:
            # Connect to the database
            connection = connect_db()
            cursor = connection.cursor()

            # Get form data
            property_name = request.form['property_name']
            property_type = request.form['property_type']
            price = request.form['price']
            description = request.form['description']

            # Insert new property into the database
            query = "INSERT INTO realestate.real_estate_properties (property_name, property_type, price, description) " \
                    "VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (property_name, property_type, price, description))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Redirect to the properties page after adding the new property
            return redirect(url_for('show_properties'))

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)
