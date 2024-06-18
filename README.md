# UZAY KT-U23 Ground Station Interface

UZAY KT-U23 Ground Station Interface is developed for the Teknofest 8th Model Satellite Competition to act as a ground station. The project visualizes the data received every second from an ESP module. 
the task of Ground Station have to do:
- Visiualize the datas as graph, map, position simulation at least 2d dimension
- save telemetry datas as a csv file
- save camera record coming from the satellite
- send a video to satalite
- get back the video from the satellite

All the task is realized in this project. Project is written in Python. GUI is developed with Tkinter. Matplotlib have used for plotting the datas altitude of container and payload, pressure of container and payload, altitude difference, voltage, temperature, and speed. TkinterMapView is used for showing the payload location in a map view. OpenGL is used for 3d simulation of the payload position/standing in the air. OpenCV is used for displaying camera display coming from satellite and saving the record. Serial library is used for getting the telemetry data from esp32 via serial. FTP transportation protocol is used for sending and recieving a video file to sattelite payload asynchronously.

The program expects data from the serial port in the following format:
```bash
<counter>,<statu>,<aras>,<mission_time>,<container_pressure>,<payload_altitude>,<container_altitude>,<altitude_difference>,<speed>,<temperature>,<voltage>,<gps_latitude>,<gps_longitude>,<gps_altitude>,<pitch>,<roll>,<yaw>,<team_id>
```
Example Data
```bash
<5>,<3>,<10100>,<2023-06-18,12:34:56>,<1013.25>,<1012.78>,<500>,<450>,<50>,<25.4>,<3.7>,<-74.0060>,<40.7127>,<495>,<84.5>,<2.0>,<184.7>,<145812>
```
Here is the screenshot of the ground station interface
On the top there is mission time, team id, packet count num, aras, some command for payload as a button and battery display of the computer.
On the left side there is team logo, payload mission statu displaying area, serial port connection and csv handling area, asynchronously video transmission via ftp area, and on the bottom there is a area for recieving the video file back. 
On the second column of the top there is a camera displaying area, then map area and 3d position area. 
Lastly top right side ploting area and the bottom right side there is all telemetry displaying area. One of them is instant displaying and other one is table like displaying of all telemetry data.
![alt text](https://github.com/rai-shi/UZAY_KT-U23_Ground_Station/blob/master/ui8.png?raw=true)

## Technologies Used

- **Programming Language:** Python
- **GUI Design and Development:** Tkinter
- **Graphics:** Matplotlib
- **Satellite Position Animation:** OpenGL
- **Map View:** TkinterMapView
- **Camera Display and Recording:** OpenCV
- **Serial Data Communication:** serial
- **Asynchronous Video Streaming:** ftplib

## Installation Instructions

Ensure you have the following libraries installed:

```bash
pip install tkinter matplotlib pillow psutil pyserial opencv-python tkintermapview pygrabber PyOpenGL
```
## Usage Instructions
To run the project, execute the following file:
```bash
path\to\UZAY_KT-U23_Ground_Station\UZAY KT-U23 YER İSTASYONU\dist\UZAY_KT_U23_YER_İSTASYONU.exe
```
For development, use the following files:
```bash
path\to\UZAY_KT-U23_Ground_Station\UZAY KT-U23 YER İSTASYONU\UZAY_KT_U23_YER_İSTASYONU.py
path\to\UZAY_KT-U23_Ground_Station\UZAY KT-U23 YER İSTASYONU\functions.py
```
**UZAY_KT_U23_YER_İSTASYONU.py** file is for UI development and **functions.py** file is for backend development.

## Contributing
The project currently experiences performance issues and frequent program freezes after running for long time. The threading implementation needs improvement. It is more reliable then my previous one ([NeliA Ground Station](https://github.com/rai-shi/NEILA-Ground_Station)) but still is not perfect. Contributions focusing on threading and optimization are welcome.
Contact Information
For any inquiries or feedback, please contact: aysenurtak1@gmail.com
