import exifread
from PIL import Image
from datetime import datetime
from GPSPhoto import gpsphoto
import glob
import os, os.path


def read_img_and_get_exif_DateTime(path):
    """
    Get image's EXIF and find the DateTime of image
    path: an Object image
    return: the values DateTime of image
    """
    tags = {}
    with open(path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        DateTime = tags["Image DateTime"]
        return DateTime.values


def get_correct_time(image, timedelta):
    """Get the correct time of image base on image's datetime and timedelta
    image: an Object image
    timedelta: time that self given
    return: the interger of correct_time
    """
    date_time = read_img_and_get_exif_DateTime(image)

    # conver everything to second
    x = datetime.strptime(date_time.split(',')[0],"%Y:%m:%d %H:%M:%S")

    timestamp = datetime.timestamp(x)

    # convert timestamp from second to milisecond
    correct_time = (timestamp * 1000) + timedelta
    return int(correct_time)


def get_cordinate(image, route_data, timedelta):
    """
    Find location("latitude", "longitude") from the correct_time and "fix_time"
    image: an Object image need to get correct_time(interger)
    route_data: an Json file that contain "fix_time", "latitude", longtitude,...(all values is interger)
    return: Cordinate of location in image
    """
    if route_data==[]:
        print("route_data is empty")
    else:
        correct_time = get_correct_time(image, timedelta)
        for fragments in route_data:
            # Get coordinate from the suitable data(data that have closest time with correct_time) base on fix_time
            suitable_data = min(fragments, key=lambda x:abs(x['fix_time']-(correct_time)))
            return (suitable_data['latitude'], suitable_data['longitude'], suitable_data['altitude'])


def edit_GPS_image(absolute_path_to_photos, ignored_photo, route_data, timedelta):
    """
    Modify coordinates to exif data of image
    absolute_path_to_photos: the path that content object images
    ignored_photo: image that will be ignored
    route_data: a data from database
    time_delta: time milisecond
    return: an Object image with modified exif data
    """
    dirname= absolute_path_to_photos + "/new_exif_GPS"

    images = glob.glob(absolute_path_to_photos + '/*.*')


    n=0
    for image in images:
        with open(image, 'rb') as file:
            try:
                if image == ignored_photo:
                    print('Image: {} is ignored'.format(image))
                    pass
                else:
                    latitude, longitude, altitude = get_cordinate(image, route_data, timedelta)
                    photo = gpsphoto.GPSPhoto(image)

                    # Create GPSInfo Data Object
                    info = gpsphoto.GPSInfo((latitude, longitude), alt=int(altitude))

                    # Create folder if not exitsts
                    if not os.path.exists(dirname):
                        os.mkdir(dirname)
                        print("Directory " , dirname ,  " Created ")
                    else:
                        pass

                    # Modify GPS Data and save multiple images
                    photo.modGPSData(info, absolute_path_to_photos + '/new_exif_GPS/GPS_{}.jpg'.format(n))
                    n += 1
            except FileNotFoundError:
                    print("Wrong file or file path")
            except:
                    pass
