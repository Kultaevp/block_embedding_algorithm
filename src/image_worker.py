import time

def get_channel(picture, width, height):
    '''
    Извлечение red канала изображения
    Для алгоритма используются только
    полутоновые изображения, поэтому все
    компоненты (R, G, B) одинаковые, поэтому
    имеет смысл работать только с одной цветовой
    компонентой
    '''
    red_channel = list()
    buffer_channel = list()
    time.sleep(2)
    for x in range(0, height):
        for y in range(0, width):
            channels = picture.getpixel((y, x))
            try:
                red, green, blue, alpha = channels
            except ValueError:
                red, green, blue = channels
            buffer_channel.append(red)
        red_channel.append(buffer_channel)
        buffer_channel = []

    return red_channel


def save_picture(picture, width, height, photo):
    for i in range(width):
        for j in range(height):
            red = int(picture[i][j])
            photo.putpixel((j, i), (red, red, red))
    return photo

