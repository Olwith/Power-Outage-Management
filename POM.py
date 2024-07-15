import streamlit as st
import pandas as pd
import sqlite3
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import requests

# Database connection
conn = sqlite3.connect('kplc.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    location TEXT,
    meter_serial_number TEXT
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

# Helper functions
def get_data(table_name):
    return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

def add_customer(name, location, meter_serial_number):
    c.execute("INSERT INTO customers (name, location, meter_serial_number) VALUES (?, ?, ?)",
              (name, location, meter_serial_number))
    conn.commit()

def add_meter(location, latitude, longitude, meter_id):
    c.execute("INSERT INTO meters (location, latitude, longitude, meter_id) VALUES (?, ?, ?, ?)",
              (location, latitude, longitude, meter_id))
    conn.commit()

def add_pole(location, latitude, longitude, pole_id):
    c.execute("INSERT INTO poles (location, latitude, longitude, pole_id) VALUES (?, ?, ?, ?)",
              (location, latitude, longitude, pole_id))
    conn.commit()

def add_power_line(start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id):
    c.execute("INSERT INTO power_lines (start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (start_location, start_latitude, start_longitude, end_location, end_latitude, end_longitude, line_id))
    conn.commit()

def add_transformer(location, latitude, longitude, transformer_id):
    c.execute("INSERT INTO transformers (location, latitude, longitude, transformer_id) VALUES (?, ?, ?, ?)",
              (location, latitude, longitude, transformer_id))
    conn.commit()

def add_power_station(location, latitude, longitude, station_id):
    c.execute("INSERT INTO power_stations (location, latitude, longitude, station_id) VALUES (?, ?, ?, ?)",
              (location, latitude, longitude, station_id))
    conn.commit()

def add_contact_center_message(customer_name, customer_contact, message):
    c.execute("INSERT INTO contact_center (customer_name, customer_contact, message) VALUES (?, ?, ?)",
              (customer_name, customer_contact, message))
    conn.commit()

def respond_to_message(message_id, response):
    c.execute("UPDATE contact_center SET response = ? WHERE id = ?", (response, message_id))
    conn.commit()

def handle_csv_upload(file, table_name):
    df = pd.read_csv(file)
    df.to_sql(table_name, conn, if_exists='append', index=False)

def delete_data_by_id(table_name, record_id):
    c.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
    conn.commit()

def delete_all_data(table_name):
    c.execute(f"DELETE FROM {table_name}")
    conn.commit()

def send_sms(message, recipients):
    # Replace with actual API call to send SMS
    api_url = "https://uwazi.mobile/api/v1/sms"
    api_key = "your_api_key"  # Replace with your actual API key
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"message": message, "recipients": recipients}
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

# Streamlit app
st.title('KPLC Power Outage Management System')

# Sidebar navigation
selected_section = st.sidebar.selectbox('Select Section', 
                                        ['Customer Section', 'KPLC Section', 'Contact Center', 'Query Tables'])

if selected_section == 'Customer Section':
    st.header('Customer Section')
    with st.form(key='customer_form'):
        name = st.text_input('Name')
        location = st.text_input('Location')
        meter_serial_number = st.text_input('Meter Serial Number')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            add_customer(name, location, meter_serial_number)
            st.success('Customer submitted successfully')

    st.header('Contact Center')
    with st.form(key='contact_form'):
        customer_name = st.text_input('Customer Name')
        customer_contact = st.text_input('Customer Contact')
        message = st.text_area('Message')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            add_contact_center_message(customer_name, customer_contact, message)
            st.success('Message submitted successfully')

elif selected_section == 'KPLC Section':
    sub_section = st.selectbox('Select Sub-Section', ['Meters', 'Poles', 'Power Lines', 'Transformers', 'Power Stations'])

    if sub_section == 'Meters':
        st.header('Meters Section')
        with st.form(key='meters_form'):
            location = st.text_input('Location')
            latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
            longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
            meter_id = st.text_input('Meter ID')
            submit_button = st.form_submit_button(label='Submit Meter')
            if submit_button:
                add_meter(location, latitude, longitude, meter_id)
                st.success('Meter submitted successfully')

    elif sub_section == 'Poles':
        st.header('Poles Section')
        with st.form(key='poles_form'):
            location = st.text_input('Location')
            latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
            longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
            pole_id = st.text_input('Pole ID')
            submit_button = st.form_submit_button(label='Submit Pole')
            if submit_button:
                add_pole(location, latitude, longitude, pole_id)
                st.success('Pole submitted successfully')

    elif sub_section == 'Power Lines':
        st.header('Power Lines Section')
        with st.form(key='power_lines_form'):
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

    elif sub_section == 'Transformers':
        st.header('Transformers Section')
        with st.form(key='transformers_form'):
            location = st.text_input('Location')
            latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
            longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
            transformer_id = st.text_input('Transformer ID')
            submit_button = st.form_submit_button(label='Submit Transformer')
            if submit_button:
                add_transformer(location, latitude, longitude, transformer_id)
                st.success('Transformer submitted successfully')

    elif sub_section == 'Power Stations':
        st.header('Power Stations Section')
        with st.form(key='power_stations_form'):
            location = st.text_input('Location')
            latitude = st.number_input('Latitude', format="%.10f", step=0.0000000001)
            longitude = st.number_input('Longitude', format="%.10f", step=0.0000000001)
            station_id = st.text_input('Station ID')
            submit_button = st.form_submit_button(label='Submit Power Station')
            if submit_button:
                add_power_station(location, latitude, longitude, station_id)
                st.success('Power Station submitted successfully')

    st.header('Contact Center')
    with st.form(key='contact_form_kplc'):
        customer_name = st.text_input('Customer Name')
        customer_contact = st.text_input('Customer Contact')
        message = st.text_area('Message')
        response = st.text_area('Response')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            add_contact_center_message(customer_name, customer_contact, message)
            st.success('Message submitted successfully')
            if response:
                respond_to_message(customer_name, response)
                st.success('Response submitted successfully')

elif selected_section == 'Contact Center':
    st.header('Contact Center Messages')
    contact_center_data = get_data('contact_center')
    st.dataframe(contact_center_data)

    with st.form(key='response_form'):
        message_id = st.number_input('Message ID', min_value=1)
        response = st.text_area('Response')
        submit_button = st.form_submit_button(label='Submit Response')
        if submit_button:
            respond_to_message(message_id, response)
            st.success('Response submitted successfully')

elif selected_section == 'Query Tables':
    table_to_query = st.selectbox('Select Table to Query', ['customers', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations', 'contact_center'])
    if table_to_query:
        data = get_data(table_to_query)
        columns = data.columns.tolist()
        column_to_filter = st.selectbox('Select Column to Filter', columns)
        unique_values = data[column_to_filter].unique().tolist()
        value_to_filter = st.selectbox('Select Value to Filter', unique_values)
        filtered_data = data[data[column_to_filter] == value_to_filter]
        st.dataframe(filtered_data)

# Map Section
st.header('Map')
map_center = [0.4256, 36.7552]  # Center of Kenya
m = folium.Map(location=map_center, zoom_start=7, tiles='OpenStreetMap', attr='Map data © OpenStreetMap contributors')

# Add Esri basemap
esri_tile = folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    name='Esri World Imagery'
).add_to(m)

# Add layers to the map
for table in ['meters', 'poles', 'power_lines', 'transformers', 'power_stations']:
    data = get_data(table)
    if table == 'power_lines':
        for _, row in data.iterrows():
            folium.PolyLine([(row['start_latitude'], row['start_longitude']), (row['end_latitude'], row['end_longitude'])],
                            color='blue', weight=2.5, opacity=1).add_to(m)
    else:
        for _, row in data.iterrows():
            folium.Marker([row['latitude'], row['longitude']], popup=row['location']).add_to(m)

# Layer control
folium.LayerControl().add_to(m)
st_data = st_folium(m, width=700, height=500)

# Display data tables
st.header('Data Tables')
table_to_display = st.selectbox('Select Table to Display', ['customers', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations', 'contact_center'])
data = get_data(table_to_display)
st.dataframe(data)

# CSV upload and download
st.header('Upload CSV')
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
table_to_upload = st.selectbox('Select Table to Upload Data', ['customers', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations', 'contact_center'])
if uploaded_file is not None:
    handle_csv_upload(uploaded_file, table_to_upload)
    st.success('Data uploaded successfully')

st.header('Download Data')
table_to_download = st.selectbox('Select Table to Download Data', ['customers', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations', 'contact_center'], key='download')
data_to_download = get_data(table_to_download)
csv = data_to_download.to_csv(index=False)
st.download_button(label='Download CSV', data=csv, mime='text/csv', file_name=f'{table_to_download}.csv')


# Delete data by ID
st.header('Delete Data by ID')
table_to_delete_from = st.selectbox('Select Table to Delete Data From', ['customers', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations', 'contact_center'], key='delete')
record_id = st.number_input('Record ID to Delete', min_value=1)
delete_button = st.button('Delete Record')
if delete_button:
    delete_data_by_id(table_to_delete_from, record_id)
    st.success('Record deleted successfully')

# Delete all data from a table
st.header('Delete All Data from Table')
table_to_delete_all = st.selectbox('Select Table to Delete All Data From', ['customers', 'meters', 'poles', 'power_lines', 'transformers', 'power_stations', 'contact_center'], key='delete_all')
delete_all_button = st.button('Delete All Data')
if delete_all_button:
    delete_all_data(table_to_delete_all)
    st.success('All data deleted successfully')

