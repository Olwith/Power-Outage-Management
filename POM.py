import streamlit as st
import pandas as pd
import sqlite3
import folium
import base64
from streamlit_folium import st_folium

# Database setup
conn = sqlite3.connect('kplc_data.db')
c = conn.cursor()

# Function to create tables
def create_tables():
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            meter_serial_number TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS kplc_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            latitude REAL,
            longitude REAL,
            issue TEXT,
            resolved INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS meters (
            id INTEGER PRIMARY KEY,
            location TEXT,
            latitude REAL,
            longitude REAL,
            meter_id TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS poles (
            id INTEGER PRIMARY KEY,
            location TEXT,
            latitude REAL,
            longitude REAL,
            pole_id TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS power_lines (
            id INTEGER PRIMARY KEY,
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
            id INTEGER PRIMARY KEY,
            location TEXT,
            latitude REAL,
            longitude REAL,
            transformer_id TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS power_stations (
            id INTEGER PRIMARY KEY,
            location TEXT,
            latitude REAL,
            longitude REAL,
            station_id TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS contact_center (
            id INTEGER PRIMARY KEY,
            customer_name TEXT,
            customer_contact TEXT,
            message TEXT,
            response TEXT
        )
    ''')
    conn.commit()

# Function to add a customer report
def add_customer_report(name, location, meter_serial_number):
    c.execute('INSERT INTO customers (name, location, meter_serial_number) VALUES (?, ?, ?)', 
              (name, location, meter_serial_number))
    conn.commit()

# Function to add a KPLC data report
def add_kplc_data(name, latitude, longitude, issue):
    c.execute('INSERT INTO kplc_data (name, latitude, longitude, issue) VALUES (?, ?, ?, ?)', 
              (name, latitude, longitude, issue))
    conn.commit()

# Functions to add data to respective tables
def add_meter(location, latitude, longitude, meter_id):
    c.execute('INSERT INTO meters (location, latitude, longitude, meter_id) VALUES (?, ?, ?, ?)', 
              (location, latitude, longitude, meter_id))
    conn.commit()

def add_pole(location, latitude, longitude, pole_id):
    c.execute('INSERT INTO poles (location, latitude, longitude, pole_id) VALUES (?, ?, ?, ?)', 
              (location, latitude, longitude, pole_id))
    conn.commit()

def add_power_line(start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id):
    c.execute('INSERT INTO power_lines (start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id) VALUES (?, ?, ?, ?, ?, ?, ?)', 
              (start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id))
    conn.commit()

def add_transformer(location, latitude, longitude, transformer_id):
    c.execute('INSERT INTO transformers (location, latitude, longitude, transformer_id) VALUES (?, ?, ?, ?)', 
              (location, latitude, longitude, transformer_id))
    conn.commit()

def add_power_station(location, latitude, longitude, station_id):
    c.execute('INSERT INTO power_stations (location, latitude, longitude, station_id) VALUES (?, ?, ?, ?)', 
              (location, latitude, longitude, station_id))
    conn.commit()

def add_contact_center_message(customer_name, customer_contact, message):
    c.execute('INSERT INTO contact_center (customer_name, customer_contact, message) VALUES (?, ?, ?)', 
              (customer_name, customer_contact, message))
    conn.commit()

def respond_to_message(message_id, response):
    c.execute('UPDATE contact_center SET response = ? WHERE id = ?', (response, message_id))
    conn.commit()

# Function to fetch data
def get_data(table_name):
    return pd.read_sql_query(f'SELECT * FROM {table_name}', conn)

# Function to delete data by ID
def delete_data_by_id(table_name, row_id):
    c.execute(f'DELETE FROM {table_name} WHERE id = ?', (row_id,))
    conn.commit()

# Function to delete all data
def delete_all_data(table_name):
    c.execute(f'DELETE FROM {table_name}')
    conn.commit()

# Function to handle CSV upload
def handle_csv_upload(uploaded_file, table_name):
    data = pd.read_csv(uploaded_file)
    data.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()

# Create tables
create_tables()

# Streamlit app layout
st.title('KPLC Power Outage Management System')

st.sidebar.title('Navigation')
selected_section = st.sidebar.selectbox('Select Section', 
                                        ['Customer Section', 'KPLC Data', 'Meters', 'Poles', 'Power Lines', 'Transformers', 'Power Stations', 'Contact Center', 'Query Tables'])

if selected_section == 'Customer Section':
    st.header('Customer Report Section')
    with st.form(key='customer_report_form'):
        name = st.text_input('Name')
        location = st.text_input('Location')
        meter_serial_number = st.text_input('Meter Serial Number')
        submit_button = st.form_submit_button(label='Submit Report')
        if submit_button:
            add_customer_report(name, location, meter_serial_number)
            st.success('Report submitted successfully')

elif selected_section == 'KPLC Data':
    st.header('KPLC Data Report Section')
    with st.form(key='kplc_data_form'):
        name = st.text_input('Name')
        latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
        longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
        issue = st.text_area('Issue')
        submit_button = st.form_submit_button(label='Submit Report')
        if submit_button:
            add_kplc_data(name, latitude, longitude, issue)
            st.success('Report submitted successfully')

elif selected_section == 'Meters':
    st.header('Meters Section')
    with st.form(key='meter_form'):
        location = st.text_input('Location')
        latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
        longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
        meter_id = st.text_input('Meter ID')
        submit_button = st.form_submit_button(label='Submit Meter')
        if submit_button:
            add_meter(location, latitude, longitude, meter_id)
            st.success('Meter submitted successfully')

elif selected_section == 'Poles':
    st.header('Poles Section')
    with st.form(key='pole_form'):
        location = st.text_input('Location')
        latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
        longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
        pole_id = st.text_input('Pole ID')
        submit_button = st.form_submit_button(label='Submit Pole')
        if submit_button:
            add_pole(location, latitude, longitude, pole_id)
            st.success('Pole submitted successfully')

elif selected_section == 'Power Lines':
    st.header('Power Lines Section')
    with st.form(key='power_line_form'):
        start_location = st.text_input('Start Location')
        start_latitude = st.number_input('Start Latitude', format="%.10f", step=0.0000000001)
        start_longitude = st.number_input('Start Longitude', format="%.10f", step=0.0000000001)
        end_location = st.text_input('End Location')
        end_latitude = st.number_input('End Latitude', format="%.10f", step=0.0000000001)
        end_longitude = st.number_input('End Longitude', format="%.10f", step=0.0000000001)
        line_id = st.text_input('Line ID')
        submit_button = st.form_submit_button(label='Submit Power Line')
        if submit_button:
            add_power_line(start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id)
            st.success('Power Line submitted successfully')

elif selected_section == 'Transformers':
    st.header('Transformers Section')
    with st.form(key='transformer_form'):
        location = st.text_input('Location')
        latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
        longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
        transformer_id = st.text_input('Transformer ID')
        submit_button = st.form_submit_button(label='Submit Transformer')
        if submit_button:
            add_transformer(location, latitude, longitude, transformer_id)
            st.success('Transformer submitted successfully')

elif selected_section == 'Power Stations':
    st.header('Power Stations Section')
    with st.form(key='power_station_form'):
        location = st.text_input('Location')
        latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
        longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
        station_id = st.text_input('Station ID')
        submit_button = st.form_submit_button(label='Submit Power Station')
        if submit_button:
            add_power_station(location, latitude, longitude, station_id)
            st.success('Power Station submitted successfully')

elif selected_section == 'Contact Center':
    st.header('Contact Center')
    with st.form(key='contact_center_form'):
        customer_name = st.text_input('Customer Name')
        customer_contact = st.text_input('Customer Contact')
        message = st.text_area('Message')
        submit_button = st.form_submit_button(label='Submit Message')
        if submit_button:
            add_contact_center_message(customer_name, customer_contact, message)
            st.success('Message submitted successfully')

    st.header('Respond to Messages')
    messages = get_data('contact_center')
    for idx, row in messages.iterrows():
        st.write(f"ID: {row['id']}, Customer Name: {row['customer_name']}, Contact: {row['customer_contact']}, Message: {row['message']}")
        response = st.text_area(f"Response to Message ID {row['id']}", key=f'response_{row["id"]}')
        if st.button(f'Submit Response to ID {row["id"]}', key=f'submit_response_{row["id"]}'):
            respond_to_message(row['id'], response)
            st.success(f'Response to Message ID {row["id"]} submitted successfully')

# Displaying the map and data visualization
st.header('Map and Data Visualization')

# Select the layers to display
selected_layers = st.multiselect('Select Layers to Display', 
                                 ['Customers', 'KPLC Data', 'Meters', 'Poles', 'Power Lines', 'Transformers', 'Power Stations'])

map_center = [0.0236, 37.9062]  # Center of Kenya
m = folium.Map(location=map_center, zoom_start=7, tiles="CartoDB positron")

# Add ESRI basemap
esri_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
folium.TileLayer(tiles=esri_url, attr='ESRI').add_to(m)

# Add selected layers to the map
if 'Customers' in selected_layers:
    customers = get_data('customers')
    for idx, row in customers.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Name: {row['name']}<br>Location: {row['location']}<br>Meter Serial Number: {row['meter_serial_number']}").add_to(m)

if 'KPLC Data' in selected_layers:
    kplc_data = get_data('kplc_data')
    for idx, row in kplc_data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Name: {row['name']}<br>Issue: {row['issue']}<br>Resolved: {row['resolved']}").add_to(m)

if 'Meters' in selected_layers:
    meters = get_data('meters')
    for idx, row in meters.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Location: {row['location']}<br>Meter ID: {row['meter_id']}").add_to(m)

if 'Poles' in selected_layers:
    poles = get_data('poles')
    for idx, row in poles.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Location: {row['location']}<br>Pole ID: {row['pole_id']}").add_to(m)

if 'Power Lines' in selected_layers:
    power_lines = get_data('power_lines')
    for idx, row in power_lines.iterrows():
        folium.PolyLine(locations=[[row['start_latitude'], row['start_longitude']], 
                                   [row['end_latitude'], row['end_longitude']]], 
                        popup=f"Start Location: {row['start_location']}<br>End Location: {row['end_location']}<br>Line ID: {row['line_id']}").add_to(m)

if 'Transformers' in selected_layers:
    transformers = get_data('transformers')
    for idx, row in transformers.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Location: {row['location']}<br>Transformer ID: {row['transformer_id']}").add_to(m)

if 'Power Stations' in selected_layers:
    power_stations = get_data('power_stations')
    for idx, row in power_stations.iterrows():
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Location: {row['location']}<br>Station ID: {row['station_id']}").add_to(m)

# Display the map
st_folium(m, width=700, height=500)

# CSV Upload Section
st.header('Upload Data as CSV')

uploaded_file = st.file_uploader('Upload CSV', type='csv')
if uploaded_file:
    table_name = st.selectbox('Select Table to Upload Data', 
                              ['customers', 'kplc_data', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations'], key='upload_table')
    if st.button('Upload', key='upload_button'):
        handle_csv_upload(uploaded_file, table_name)
        st.success('Data uploaded successfully')

# Display Data and Download Option
st.header('Data Table and Download Option')

selected_table = st.selectbox('Select Table to View and Download', 
                              ['customers', 'kplc_data', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations'], key='view_table')

data = get_data(selected_table)
st.write(data)

# Delete data by ID
delete_id = st.number_input(f'Enter ID to Delete from {selected_table}', min_value=0, step=1)
if st.button(f'Delete by ID in {selected_table}', key='delete_by_id_button'):
    delete_data_by_id(selected_table, delete_id)
    st.success(f'Data with ID {delete_id} deleted successfully')

# Delete all data button
if st.button(f'Delete All Data in {selected_table}', key='delete_all_button'):
    delete_all_data(selected_table)
    st.success('All data deleted successfully')

# Function to download data as CSV
def download_csv(data, filename):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

st.markdown(download_csv(data, f'{selected_table}.csv'), unsafe_allow_html=True)

# Query Tables Section
if selected_section == 'Query Tables':
    st.header('Query Tables')
    
    query_table = st.selectbox('Select Table to Query', 
                               ['customers', 'kplc_data', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations'], key='query_table')
    
    query_column = st.text_input(f'Enter Column Name to Query in {query_table}')
    query_value = st.text_input(f'Enter Value to Query in {query_column}')
    
    if st.button('Query', key='query_button'):
        query_result = pd.read_sql_query(f'SELECT * FROM {query_table} WHERE {query_column} = ?', conn, params=(query_value,))
        st.write(query_result)

