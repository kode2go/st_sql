import streamlit as st
import psycopg2

# Database connection parameters
dbname = "testbd"
user = "postgres"
password = "user"  # Update this to the new password you've set
host = "localhost"
port = "5432"

# Streamlit app
def main():
    st.title("User Data Table")

    display_all = st.button("Display All Rows")

    try:
        # Establish a connection to the database
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        # Create a cursor
        cursor = connection.cursor()

        # Execute a SELECT query
        query = "SELECT * FROM users;"
        cursor.execute(query)

        # Fetch all the results
        #rows = cursor.fetchall()

        # Fetch all or the first 3 results based on the button click
        if display_all:
            rows = cursor.fetchall()
        else:
            rows = cursor.fetchmany(3)

        # Display the results in a Streamlit table
        st.table(rows)

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except Exception as e:
        st.error("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
