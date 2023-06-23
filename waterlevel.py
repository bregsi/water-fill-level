from flask import Flask, render_template
from DFRobot_RaspberryPi_A02YYUW import DFRobot_A02_Distance as Board
import sys
import os
import time

app = Flask(__name__)


def print_distance(dis):
  if board.last_operate_status == board.STA_OK:
    print("Distance %d mm" %dis)
  elif board.last_operate_status == board.STA_ERR_CHECKSUM:
    print("ERROR")
  elif board.last_operate_status == board.STA_ERR_SERIAL:
    print("Serial open failed!")
  elif board.last_operate_status == board.STA_ERR_CHECK_OUT_LIMIT:
    print("Above the upper limit: %d" %dis)
  elif board.last_operate_status == board.STA_ERR_CHECK_LOW_LIMIT:
    print("Below the lower limit: %d" %dis)
  elif board.last_operate_status == board.STA_ERR_DATA:
    print("No data!")


@app.route('/')
def index():
    # Calculate the water level dynamically (percentage between 0 and 100)
    measured_level = 42
    board = Board()
    dis_min = 0
    dis_max = 45000
    board.set_dis_range(dis_min, dis_max)
    distance = board.getDistance()
    percent= (600-distance)/6
    if percent>100:
        percent = 100
    elif percent < 0:
        percent = 0
    return render_template('index.html', water_level=percent, water_distance=distance)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
