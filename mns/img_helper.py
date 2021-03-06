from django.conf import settings
from PIL import Image, ExifTags
#import logging
import os

import boto
from boto.s3.key import Key


def prepare(data):
    img = autorotate(Image.open(data))
    return square_crop(img)
    pass


def square_crop(img):
    # if not RGB, convert
    if img.mode not in ("L", "RGB"):
        img = img.convert("RGB")

    x = img.size[0]
    y = img.size[1]

    if x > y:
        x = y
    elif x < y:
        y = x

    #get orginal image ratio
    img_ratio = float(img.size[0]) / img.size[1]
    resize_ratio = float(x) / y

    # get output with and height to do the first crop
    if(img_ratio > resize_ratio):
        output_width = x * img.size[1] / y
        output_height = img.size[1]
        originX = img.size[0] / 2 - output_width / 2
        originY = 0
    else:
        output_width = img.size[0]
        output_height = y * img.size[0] / x
        originX = 0
        originY = img.size[1] / 2 - output_height / 2

    #crop
    cropBox = (originX, originY, originX + output_width, originY + output_height)
    img = img.crop(cropBox)
    return img


def autorotate(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180)
        elif exif[orientation] == 6:
            image = image.rotate(270)
        elif exif[orientation] == 8:
            image = image.rotate(90)

        return image

        #image.thumbnail((THUMB_WIDTH, THUMB_HIGHT), Image.ANTIALIAS)
        #image.save(os.path.join(path, fileName))

    except:
        #traceback.print_exc()
        return image


def save_thumbnail(name, img, size):
    img.thumbnail([size, size], Image.ANTIALIAS)
    filename = "%s-%s.jpg" % (name, size)
    directory = os.path.join(settings.PROJECT_ROOT, "static", "images", "users")
    if not os.path.exists(directory):
        os.makedirs(directory)
    pathname = os.path.join(directory, filename)
    imagefile = open(pathname, "w")
    img.save(imagefile, "JPEG", quality=80)
    if not settings.DEBUG:
        #logging.getLogger('boto').setLevel(logging.CRITICAL)
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                    settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        k = Key(bucket)
        k.key = "images/users/%s" % filename
        #if k.exists():
        #    k.delete()
        k.set_contents_from_filename(pathname)
        k.make_public()
        os.remove(pathname)
    return "images/users/%s" % filename
