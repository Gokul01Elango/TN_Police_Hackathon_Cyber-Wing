# Detection of Pornographic Digital Images
# YCbCr Model
# input:the dir of an image
from PIL import Image
import sys


def image_ifo():
    try:
        img = Image.open(r"image22.JPEG")
    except Exception as e:
        print("Can not open the image!")
    print('Image Mode:%s,Image Size:%s,Image Format:%s' % (img.mode, img.size, img.format))
    return img


def preprocessed_image():
    img = image_ifo()
    if not img.mode == 'YCbCr':
        img = img.convert('YCbCr')
    return img


def detector():
    img = preprocessed_image()
    ycbcr_data = img.getdata()
    W, H = img.size
    THRESHOLD = 0.3
    count = 0
    for i, ycbcr in enumerate(ycbcr_data):
        y, cb, cr = ycbcr
        if 80 <= cb <= 120 and 133 <= cr <= 173:
        #if 86 <= cb <= 127 and 130 <= cr < 168:
            count += 1
    if count > THRESHOLD * W * H:
        print('The image is not pornographic!')
    else:
        print('The image is  pornographic!')


if __name__ == '__main__':
    image = sys.argv[-1]
    print('Detector is working on it,please wait a second...')
    detector()
    print('Detecting is done!')
