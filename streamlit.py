import streamlit as st
import mysql.connector
import pandas as pd

#connecting to MySQL database and fetch data
def fetch_data_from_mysql(query, host="localhost", user="root", password="root", database="stockmarket"):
    """
    Fetch data from MySQL database.
    """
    #connecting to the database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    #executing the query
    cursor.execute(query)
    
    #fetching all results
    results = cursor.fetchall()
    
    #getting column names from the cursor description
    columns = [column[0] for column in cursor.description]
    
    #converting results to a dataframe
    df = pd.DataFrame(results, columns=columns)
    
    #closing the connection
    cursor.close()
    conn.close()
    
    return df

#streamlit UI
st.title("Investors' Dashboard")

#displaying the list of tables in the database
st.header("Tables in the stockmarket database:")
tables_query = "SHOW TABLES;"
tables_df = fetch_data_from_mysql(tables_query)
st.write(tables_df)

#allowing the user to select a table to view
selected_table = st.selectbox("Select a table to view:", tables_df.iloc[:, 0])

#fetching and displaying the data from the selected table
st.header(f"Data from {selected_table}:")
data_query = f"SELECT * FROM {selected_table} LIMIT 20;"  
data_df = fetch_data_from_mysql(data_query)
st.dataframe(data_df) 

