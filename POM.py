import streamlit as st
import sqlite3
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import io

# Connect to SQLite3 database
conn = sqlite3.connect('kplc_database.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    latitude REAL,
    longitude REAL,
    outage_report TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS kplc_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    latitude REAL,
    longitude REAL,
    status TEXT,
    resolution_time TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS meters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    latitude REAL,
    longitude REAL,
    meter_id TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS poles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    latitude REAL,
    longitude REAL,
    pole_id TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS power_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_location TEXT,
    start_latitude REAL,
    start_longitude REAL,
    end_location TEXT,
    end_latitude REAL,
    end_longitude REAL,
    line_id TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS transformers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    latitude REAL,
    longitude REAL,
    transformer_id TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS power_stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    latitude REAL,
    longitude REAL,
    station_id TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS contact_center (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    customer_contact TEXT,
    message TEXT,
    response TEXT
)
''')
conn.commit()

# Function to add customer report
def add_customer_report(name, location, latitude, longitude, outage_report):
    c.execute('''
    INSERT INTO customers (name, location, latitude, longitude, outage_report)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, location, latitude, longitude, outage_report))
    conn.commit()

# Function to add KPLC data
def add_kplc_data(location, latitude, longitude, status, resolution_time):
    c.execute('''
    INSERT INTO kplc_data (location, latitude, longitude, status, resolution_time)
    VALUES (?, ?, ?, ?, ?)
    ''', (location, latitude, longitude, status, resolution_time))
    conn.commit()

# Function to add meters
def add_meter(location, latitude, longitude, meter_id):
    c.execute('''
    INSERT INTO meters (location, latitude, longitude, meter_id)
    VALUES (?, ?, ?, ?)
    ''', (location, latitude, longitude, meter_id))
    conn.commit()

# Function to add poles
def add_pole(location, latitude, longitude, pole_id):
    c.execute('''
    INSERT INTO poles (location, latitude, longitude, pole_id)
    VALUES (?, ?, ?, ?)
    ''', (location, latitude, longitude, pole_id))
    conn.commit()

# Function to add power lines
def add_power_line(start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id):
    c.execute('''
    INSERT INTO power_lines (start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id))
    conn.commit()

# Function to add transformers
def add_transformer(location, latitude, longitude, transformer_id):
    c.execute('''
    INSERT INTO transformers (location, latitude, longitude, transformer_id)
    VALUES (?, ?, ?, ?)
    ''', (location, latitude, longitude, transformer_id))
    conn.commit()

# Function to add power stations
def add_power_station(location, latitude, longitude, station_id):
    c.execute('''
    INSERT INTO power_stations (location, latitude, longitude, station_id)
    VALUES (?, ?, ?, ?)
    ''', (location, latitude, longitude, station_id))
    conn.commit()

# Function to add contact center message
def add_contact_center_message(customer_name, customer_contact, message):
    c.execute('''
    INSERT INTO contact_center (customer_name, customer_contact, message, response)
    VALUES (?, ?, ?, ?)
    ''', (customer_name, customer_contact, message, ""))
    conn.commit()

# Function to respond to contact center message
def respond_to_message(message_id, response):
    c.execute('''
    UPDATE contact_center
    SET response = ?
    WHERE id = ?
    ''', (response, message_id))
    conn.commit()

# Function to get data
def get_data(table_name):
    return pd.read_sql_query(f'SELECT * FROM {table_name}', conn)

# Function to delete customer report
def delete_customer_report(id):
    c.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()

# Function to delete KPLC data
def delete_kplc_data(id):
    c.execute('DELETE FROM kplc_data WHERE id = ?', (id,))
    conn.commit()

# Function to delete meter
def delete_meter(id):
    c.execute('DELETE FROM meters WHERE id = ?', (id,))
    conn.commit()

# Function to delete pole
def delete_pole(id):
    c.execute('DELETE FROM poles WHERE id = ?', (id,))
    conn.commit()

# Function to delete power line
def delete_power_line(id):
    c.execute('DELETE FROM power_lines WHERE id = ?', (id,))
    conn.commit()

# Function to delete transformer
def delete_transformer(id):
    c.execute('DELETE FROM transformers WHERE id = ?', (id,))
    conn.commit()

# Function to delete power station
def delete_power_station(id):
    c.execute('DELETE FROM power_stations WHERE id = ?', (id,))
    conn.commit()

# Function to handle CSV uploads
def handle_csv_upload(file, table_name):
    df = pd.read_csv(file)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    st.success(f'Data uploaded to {table_name} successfully.')

# Function to delete all data from a table
def delete_all_data(table_name):
    c.execute(f'DELETE FROM {table_name}')
    conn.commit()
    st.success(f'All data from {table_name} deleted successfully.')

# Streamlit App
st.title('KPLC Power Outage Management')

# Choose section to fill
st.sidebar.header('Choose Section to Fill')
sections = ['Customers', 'KPLC Data', 'Meters', 'Poles', 'Power Lines', 'Transformers', 'Power Stations', 'Contact Center']
selected_section = st.sidebar.selectbox('Section', sections)

if selected_section == 'Customers':
    st.header('Customer Section')
    with st.form(key='customer_form'):
        name = st.text_input('Name')
        location = st.text_input('Location')
        latitude = st.number_input('Latitude', format="%.6f")
        longitude = st.number_input('Longitude', format="%.6f")
        outage_report = st.text_area('Outage Report')
        submit_button = st.form_submit_button(label='Submit Report')
        if submit_button:
            add_customer_report(name, location, latitude, longitude, outage_report)
            st.success('Report submitted successfully')

elif selected_section == 'KPLC Data':
    st.header('KPLC Section')
    with st.form(key='kplc_form'):
        location = st.text_input('Location')
        latitude = st.number_input('Latitude', format="%.6f")
        longitude = st.number_input('Longitude', format="%.6f")
        status = st.selectbox('Status', ['Pending', 'Resolved'])
        resolution_time = st.text_input('Resolution Time')
        submit_button = st.form_submit_button(label='Submit Data')
        if submit_button:
            add_kplc_data(location, latitude, longitude, status, resolution_time)
            st.success('Data submitted successfully')

elif selected_section == 'Meters':
    st.header('Meters Section')
    with st.form(key='meter_form'):
        location = st.text_input('Meter Location')
        latitude = st.number_input('Meter Latitude', format="%.6f")
        longitude = st.number_input('Meter Longitude', format="%.6f")
        meter_id = st.text_input('Meter ID')
        submit_button = st.form_submit_button(label='Submit Meter')
        if submit_button:
            add_meter(location, latitude, longitude, meter_id)
            st.success('Meter submitted successfully')

elif selected_section == 'Poles':
    st.header('Poles Section')
    with st.form(key='pole_form'):
        location = st.text_input('Pole Location')
        latitude = st.number_input('Pole Latitude', format="%.6f")
        longitude = st.number_input('Pole Longitude', format="%.6f")
        pole_id = st.text_input('Pole ID')
        submit_button = st.form_submit_button(label='Submit Pole')
        if submit_button:
            add_pole(location, latitude, longitude,pole_id)
            st.success('Pole submitted successfully')

elif selected_section == 'Power Lines':
    st.header('Power Lines Section')
    with st.form(key='power_line_form'):
        start_location = st.text_input('Start Location')
        start_latitude = st.number_input('Start Latitude', format="%.6f")
        start_longitude = st.number_input('Start Longitude', format="%.6f")
        end_location = st.text_input('End Location')
        end_latitude = st.number_input('End Latitude', format="%.6f")
        end_longitude = st.number_input('End Longitude', format="%.6f")
        line_id = st.text_input('Line ID')
        submit_button = st.form_submit_button(label='Submit Power Line')
        if submit_button:
            add_power_line(start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id)
            st.success('Power Line submitted successfully')

elif selected_section == 'Transformers':
    st.header('Transformers Section')
    with st.form(key='transformer_form'):
        location = st.text_input('Transformer Location')
        latitude = st.number_input('Transformer Latitude', format="%.6f")
        longitude = st.number_input('Transformer Longitude', format="%.6f")
        transformer_id = st.text_input('Transformer ID')
        submit_button = st.form_submit_button(label='Submit Transformer')
        if submit_button:
            add_transformer(location, latitude, longitude, transformer_id)
            st.success('Transformer submitted successfully')

elif selected_section == 'Power Stations':
    st.header('Power Stations Section')
    with st.form(key='power_station_form'):
        location = st.text_input('Power Station Location')
        latitude = st.number_input('Power Station Latitude', format="%.6f")
        longitude = st.number_input('Power Station Longitude', format="%.6f")
        station_id = st.text_input('Power Station ID')
        submit_button = st.form_submit_button(label='Submit Power Station')
        if submit_button:
            add_power_station(location, latitude, longitude, station_id)
            st.success('Power station submitted successfully')

elif selected_section == 'Contact Center':
    st.header('Contact Center Section')
    st.subheader('Customer Contact')
    with st.form(key='customer_contact_form'):
        customer_name = st.text_input('Customer Name')
        customer_contact = st.text_input('Customer Contact')
        message = st.text_area('Message')
        submit_button = st.form_submit_button(label='Submit Message')
        if submit_button:
            add_contact_center_message(customer_name, customer_contact, message)
            st.success('Message submitted successfully')

    st.subheader('KPLC Response')
    with st.form(key='kplc_response_form'):
        message_id = st.number_input('Message ID', min_value=1)
        response = st.text_area('Response')
        submit_button = st.form_submit_button(label='Submit Response')
        if submit_button:
            respond_to_message(message_id, response)
            st.success('Response submitted successfully')

# Data Display and Download Section
st.header('Data Display and Download Section')

data_table = st.selectbox('Select the table to display and download:', ['Customers', 'KPLC Data', 'Meters', 'Poles', 'Power Lines', 'Transformers', 'Power Stations', 'Contact Center'])
if data_table:
    table_name = data_table.lower().replace(" ", "_")
    data = get_data(table_name)
    st.write(data)

    # Download data as CSV
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{table_name}.csv">Download {table_name} as CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Map visualization
    st.header('Map Visualization')

    if not data.empty:
        if table_name == 'power_lines':
            # Ensure there are no NaNs in latitude and longitude columns for power lines
            data = data.dropna(subset=['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude'])

            if not data.empty:
                map_center = [data['start_latitude'].mean(), data['start_longitude'].mean()]
                m = folium.Map(location=map_center, zoom_start=10)

                for _, row in data.iterrows():
                    folium.PolyLine(
                        locations=[(row['start_latitude'], row['start_longitude']), (row['end_latitude'], row['end_longitude'])],
                        color='blue',
                        weight=2.5,
                        opacity=1
                    ).add_to(m)

                st_folium(m, width=700, height=500)
            else:
                st.error("No valid data to display on the map.")
        else:
            # Ensure there are no NaNs in latitude and longitude columns for other data
            data = data.dropna(subset=['latitude', 'longitude'])

            if not data.empty:
                map_center = [data['latitude'].mean(), data['longitude'].mean()]
                m = folium.Map(location=map_center, zoom_start=10)

                for _, row in data.iterrows():
                    folium.Marker(
                        location=(row['latitude'], row['longitude']),
                        popup=f"{row['location']} ({row['latitude']}, {row['longitude']})"
                    ).add_to(m)

                st_folium(m, width=700, height=500)
            else:
                st.error("No valid data to display on the map.")
    else:
        st.error("No data available to display.")

# Delete Section
st.header('Delete Data Section')
delete_table = st.selectbox('Select the table to delete data from:', ['Customers', 'KPLC Data', 'Meters', 'Poles', 'Power Lines', 'Transformers', 'Power Stations', 'Contact Center'])
if delete_table:
    delete_option = st.selectbox('Delete options:', ['Delete Specific Row', 'Delete All Data'])
    if delete_option == 'Delete Specific Row':
        row_id = st.number_input('Enter the ID of the row to delete:', min_value=1)
        if st.button('Delete Row'):
            if delete_table == 'Customers':
                delete_customer_report(row_id)
            elif delete_table == 'KPLC Data':
                delete_kplc_data(row_id)
            elif delete_table == 'Meters':
                delete_meter(row_id)
            elif delete_table == 'Poles':
                delete_pole(row_id)
            elif delete_table == 'Power Lines':
                delete_power_line(row_id)
            elif delete_table == 'Transformers':
                delete_transformer(row_id)
            elif delete_table == 'Power Stations':
                delete_power_station(row_id)
            elif delete_table == 'Contact Center':
                delete_contact_center_message(row_id)
            st.success('Row deleted successfully.')
    elif delete_option == 'Delete All Data':
        if st.button('Delete All Data'):
            delete_all_data(delete_table.lower().replace(" ", "_"))

# CSV Upload Section
st.header('CSV Upload Section')
uploaded_file = st.file_uploader('Upload CSV File', type=['csv'])
if uploaded_file:
    upload_table = st.selectbox('Select the table to upload data to:', ['Customers', 'KPLC Data', 'Meters', 'Poles', 'Power Lines', 'Transformers', 'Power Stations', 'Contact Center'])
    if st.button('Upload CSV'):
        handle_csv_upload(uploaded_file, upload_table.lower().replace(" ", "_"))

# Close the connection
conn.close()

