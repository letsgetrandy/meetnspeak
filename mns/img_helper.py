from django.conf import settings
from PIL import Image
import os


def prepare(data):
    img = Image.open(data)
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


def save_thumbnail(name, img, size):
    img.thumbnail([size, size], Image.ANTIALIAS)
    filename = "%s-%s.jpg" % (name, size)
    if settings.DEBUG:
        pathname = os.path.join(settings.PROJECT_ROOT, "static",
                "images", "users", filename)
        imagefile = open(pathname, "w")
        img.save(imagefile, "JPEG", quality=60)
    else:
        pass
    return "images/users/%s" % filename
