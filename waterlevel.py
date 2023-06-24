from flask import Flask, render_template
from DFRobot_RaspberryPi_A02YYUW import DFRobot_A02_Distance as Board
import statistics
import sqlite3
import datetime
import threading
import time
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Connect to the SQLite database
conn = sqlite3.connect('wasser_level.db')
cursor = conn.cursor()

# Create a table to store the sensor data if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS wasser_level_14d (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value REAL,
                    timestamp TEXT
                )''')

# Initialize the sensor board
board = Board()
dis_min = 10
dis_max = 2800
board.set_dis_range(dis_min, dis_max)

def measure_and_save_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('wasser_level.db')
    cursor = conn.cursor()
    while True:
        start_time = time.time()  # Record the start time
        # Measure the sensor value x times
        measurements = []
        for _ in range(12):
            # Code to measure the sensor value and append it to the list
            measurement = board.getDistance()
            measurements.append(measurement)
            time.sleep(0.7)

        # Calculate the median of the measurements
        median = statistics.median(measurements)

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert the median value and timestamp into the database
        cursor.execute('INSERT INTO wasser_level_14d (value, timestamp) VALUES (?, ?)', (median, timestamp))
        conn.commit()

        elapsed_time = time.time() - start_time
        if elapsed_time < 10:
            time.sleep(10 - elapsed_time)  # Wait for the remaining time to reach 5 seconds

        start_time = time.time()  # Reset the start time for the next measurement cycle

# Start the sensor measurement thread
sensor_thread = threading.Thread(target=measure_and_save_data)
sensor_thread.daemon = True
sensor_thread.start()

def plot_water_level():
    # Connect to the SQLite database
    conn = sqlite3.connect('wasser_level.db')
    cursor = conn.cursor()

    # Retrieve water level data for the last 14 days
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=13)
    end_date = today + datetime.timedelta(days=1)  # Add 1 day to include today's data
    cursor.execute('SELECT timestamp, value FROM wasser_level_14d WHERE timestamp BETWEEN ? AND ?', (start_date, end_date))
    data = cursor.fetchall()

    # Separate timestamps and values into separate lists
    timestamps = [row[0] for row in data]
    values = [row[1] for row in data]

    # Convert timestamps to datetime objects
    timestamps = [datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') for timestamp in timestamps]

    # Calculate the percentage of the water level
    percentages = [(600 - value) / 6 for value in values]

    # Plot the water level percentages over time
    plt.plot(timestamps, percentages)
    plt.xlabel('Date')
    plt.ylabel('Water Level Percentage')
    plt.title('Water Level Over the Last 14 Days')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a PNG file
    #plt.savefig(plot_filename)
    # Save the plot as a PNG file
    plot_filename = 'water_level_plot.png'
    plot_filepath = os.path.join(os.path.dirname(__file__), plot_filename)
    plt.savefig(plot_filepath)
    # Close the SQLite connection
    conn.close()

    return plot_filepath

@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('wasser_level.db')
    cursor = conn.cursor()
    # Retrieve the most recent water level value from the database
    cursor.execute('SELECT value FROM wasser_level_14d ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    if result:
        distance = result[0]
        percent = round((600 - distance) / 6, 2)
        if percent > 100:
            percent = 100
        elif percent < 0:
            percent = 0

    return render_template('index.html', water_level=percent, water_distance=distance)

@app.route('/recap')
def recap():
    # Generate the water level plot and get the filename
   # plot_filename = plot_water_level()
    plot_filepath = plot_water_level()
    return render_template('recap.html', plot_filepath=plot_filepath)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
