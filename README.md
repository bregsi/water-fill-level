# Fill Level Monitoring of an Underground Rainwater Tank with Ultrasonic Sensor

Development Stage with a prototype

This project focuses on monitoring the fill level of an underground rainwater tank using an ultrasonic sensor. The tank's location makes it difficult to access physically, necessitating a sensor-based solution for accurate measurement. The project involves installing an ultrasonic sensor that detects the water level and transmits the data to a web application. Users can conveniently access the web application on their smartphones to view the real-time fill level of the rainwater tank. This monitoring system aids in efficient water management, allowing users to gauge the tank's capacity and plan water usage effectively.

## Hardware Setup
- Raspberry Pi 3b+
- A02YYUW Waterproof Ultrasonic Distance Sensor, DFRobot (https://www.dfrobot.com/product-1935.html?search=SEN0311&description=true) connected via UART

![Ultrasonic Sensor](https://github.com/DFRobot/DFRobot_RaspberryPi_A02YYUW/blob/master/resources/images/SEN0311.png)

![Raspberry 3b+](https://github.com/bregsi/water-fill-level/blob/main/test-setup/rasp-3b.jpg)

## Software
- `waterlevel.py`
- 2 very simple HTML template files, for usage with Flask
- DFRobot_RaspberryPi_A02YYUW.py (slightly edited Sensor Library from manfacturer))

  index.html
  ![index.html](https://github.com/bregsi/water-fill-level/blob/main/test-setup/index.html.jpg)
  
  recap.html
  ![recap.html](https://github.com/bregsi/water-fill-level/blob/main/test-setup/recap.html.jpg)

## Testing
Setup idea which needed to be tested first (it does not work!!!):

![Final_Setup_Idea](https://github.com/bregsi/water-fill-level/blob/main/test-setup/fuellstandsmessung_with_values.png)

The initial test measurements conducted with the tube have indicated that the ultrasonic sensor faces challenges when dealing with the narrow boundaries of the tube.
The measured distance through the tube was consistently inaccurate, ranging between 15cm and 30cm. Where distances should have been in the range of 1 to 3 meters. Therefore, the idea of using the tube had to be discarded.

### Test Setup

The following tests were conducted using a small barrel with a diameter of approximately 35 cm and a height of 60 cm.

![Test Setup](https://github.com/bregsi/water-fill-level/blob/main/test-setup/test_setup_s.jpg)

The barrel was filled with tap water, and the emptying process was carried out using the siphon principle.

#### Test 01

This test was conducted with a measurement repetition rate of 0.1 seconds for 1 second, followed by a pause of 4 seconds. From each set of 10 measurements, the median value was taken as the result and plotted accordingly.

![Test01-1](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test01/water_level_plot20230624_15_02.png)
![Test01-2](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test01/water_level_plot20230624_15_21.png)
![Test01-3](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test01/water_level_plot20230624_15_30.png)

As can be observed from the plots, the results are highly inconsistent and exhibit many peculiar jumps. After experimenting with the measurement repetition rate and setting it to over 0.6 seconds, unlike the default value in the demo file from the manufacturer's repository, the results showed a slight improvement.

#### Test 02

Sensor Modification

However, something still didn't quite align with the measurements, and the suspicion pointed in the same direction as the issue with the tube. The walls from which the sound is reflected are too close. Therefore, a modification of the sensors was attempted to address this problem.

![Sensor Mod](https://github.com/bregsi/water-fill-level/blob/main/test-setup/sensor_modification_s.jpg)

So, sections of corrugated tubing were used as attachments on the ultrasonic transmitter and receiver.

Results:

![Test02-1](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test02/water_level_plot20230624_16_37.png)
![Test02-2](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test02/water_level_plot20230624_17_01.png)
![Test02-3](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test02/water_level_plot20230624_17_10.png)

Based on the current results, one can be satisfied before proceeding with the installation in the underground water tank. To ensure accuracy, the test was repeated with a slight modification. Measurements were taken every 0.7 seconds, 11 times, and the median value was calculated for each set of measurements in Test 03 and Test 04. These measurement sets were then repeated every 10 seconds to gather the additional data.

Results Test 03

![Test03-1](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test03/water_level_plot20230627-test03.png)

Results Test 04

![Test04-2](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test04/water_level_plot_20230627-test04-A.png)
![Test04-1](https://github.com/bregsi/water-fill-level/blob/main/test-setup/Test04/water_level_plot20230627-test04.png)

## Results

Based on these results, one can be satisfied with the modification as it seems to work well with a barrel of 35 cm in diameter. Therefore, it can be assumed that it will also work with the larger underground water tank. However, it is still necessary to assess the duration of sound reverberation within the tank. Thus, a subsequent live test is unavoidable to gather further information.
