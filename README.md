# DCPG: CLI
    This program is used to add the GPS data to the photos taken by user, by getting these data from the API server.

# Installation Guide:

## Requirement:

    Python 3.7+

## For regular users:
### &emsp; &emsp; Step 1 - Download the app:

    Base on the OS you are using, download the corresponding application:

    Download link (Google Drive):
    https://drive.google.com/drive/folders/1eBu9xSe4D2Ee4V0hpdtZbHs9kxC0R26-?usp=sharing

### &emsp; &emsp; Step 2 - Run app:

    Double click on the executable file, of which name is cli_program

    Wait for the program to be ready, then follow the instruction on the screen

## For developers:
### &emsp; &emsp; Step 1 - Download/ clone the source code:

    Open terminal and run the command:

    git clone https://github.com/intek-training-jsc/digital-camera-photo-geolocation-khang_tran_khang_vu.git
    << ENTER YOUR ACCOUNT FROM INTEK INSTITUTE >>

    cd << PATH_TO_DIR >>/digital-camera-photo-geolocation-restful-api-server-khang_tran_khang_vu

    git checkout develop

### &emsp; &emsp; Step 2 - Install requirement libs and modules from file requirement.txt:

    On terminal, run the command:

    pip3 install -r requirement.txt

    Note: you might need to manually install zbar or pyzbar.

### &emsp; &emsp; Step 3 - Run app:

    On terminal, run the command:

    python3 cli_program.py

    Follow the instruction on the screen
