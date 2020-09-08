import base64
import os
from cryptography.fernet import Fernet
import hashlib
import cv2
import pyzbar.pyzbar as pyzbar
import requests
import exifread
import datetime
import json
from find_image_location import edit_GPS_image
from getpass import getpass


def get_time_different(this_time_timestamp, that_time_string):
    """
    @return: int: time difference (in second) between 2 dates
    """
    this_datetime = datetime.datetime.fromtimestamp(int(this_time_timestamp)/1000)
    that_datetime = datetime.datetime.strptime(that_time_string, '%Y:%m:%d %H:%M:%S')
    return int((this_datetime - that_datetime).total_seconds())


def read_exif(path_to_image):
    """
    Read exif tags of an image

    @return: dict: of image's tags and value
    """
    # Open image file for reading (binary mode)
    opened_file = open(path_to_image, 'rb')

    # Return Exif tags
    tags = exifread.process_file(opened_file)
    return tags


def get_route_from_server(route_UUID):
    """
    Call API to get the route from server

    @route_UUID - String:shorten UUID of the route on server

    @return: String: encrypted route data
    """

    url = "https://jnz5ygxmkf.execute-api.us-east-1.amazonaws.com/api/v1/routes/%s" % route_UUID

    # Call API
    response = requests.get(url)
    # Return status code and response message
    return response.json()['route_data']


def decrypt_data(encrypted_data, password):
    """
    Decrypt the encrypted data using Fernet and a password

    @encrypted_data: encrypted data (Fernet algo)
    @password: the password used to encrypt the data

    @return: string: raw data
    """
    hashed = hashlib.md5(password.encode())
    key = base64.urlsafe_b64encode(hashed.hexdigest().encode()) # Can only use kdf once
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_data.encode())
    return decrypted.decode()


def get_qr_value(qr_image):
    """
    Detect and get the QR value

    @qr_image: path to image
    """
    img = cv2.imread(qr_image)
    decodedObjects = pyzbar.decode(img)
    data = str()
    for obj in decodedObjects:
        data = obj.data
    return data.decode("utf-8")


def promt_message_to_get_input(message):
    """
    Ask for user input again and again until they input some value
    @message: message to display to console

    @return: value - string: user input
    """
    value = ''
    is_first = True
    while not value:
        if is_first:
            value = input(message)
            is_first = False
        else:
            value = input("(Try again) " + message)

    return value


def read_input():
    """
    Read user input from terminal

    @return: Strings: corresponding inputs from user
    """
    print('\033[1m' + "╔═══════════════════════════════════════════════════════════════════════════════╗" + '\033[0m')
    print('\033[1m' + "║                                                                               ║" + '\033[0m')
    print('\033[1m' + "║  Welcome to DCPG, please follow the instruction below (press CRTL-C to quit)  ║" + '\033[0m')
    print('\033[1m' + "║                                                                               ║" + '\033[0m')
    print('\033[1m' + "╚═══════════════════════════════════════════════════════════════════════════════╝" + '\033[0m')
    print()

    path_to_folder = promt_message_to_get_input('1. Enter the absolute path to your photo folder:')
    qr_image_name = promt_message_to_get_input('2. Enter the name of the QR code photo (including its extension):')
    route_UUID = promt_message_to_get_input('3. Enter the route identification (UUID):')
    # passphrase = promt_message_to_get_input('4. Enter the passphrase:')
    passphrase = getpass(prompt='4. Enter the passphrase: ', stream=None)

    return path_to_folder, qr_image_name, route_UUID, passphrase


def main():
    path_to_folder, qr_image_name, route_UUID, passphrase = read_input()
    path_to_image = path_to_folder + "/" + qr_image_name
    qr_value = get_qr_value(path_to_image)
    qr_raw_value = decrypt_data(qr_value, passphrase)
    qr_timestamp, nonce = qr_raw_value.split("-")
    qr_exif_tags = read_exif(path_to_image)
    qr_exif_time = str(qr_exif_tags['Image DateTime'])
    time_delta = get_time_different(qr_timestamp, qr_exif_time)
    encrypted_route_data = get_route_from_server(route_UUID)
    # decrypt data and get the data in json format
    raw_data = decrypt_data(encrypted_route_data, nonce)
    # json format to list
    raw_data_to_list = json.loads(raw_data)
    edit_GPS_image(path_to_folder, qr_image_name, raw_data_to_list, time_delta)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("Bad request! Make sure you follow the instruction OR the route doesn't match with the image folder")
