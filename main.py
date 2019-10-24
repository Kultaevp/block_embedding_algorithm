from src import stego
from src import wavelet
from src import image_worker
from src import sensetive_areas
from src import decorators
import consts
import time

from PIL import Image


def send_message(wavelet, enclosure, width, height):
    '''
    Функция, описывающая действия человека, отправляющего
    изображение. Выполняется прямое преобразование, встраивание
    и обратное преобразование
    '''
    wavelet.fwt97_2d(1, width, height)
    wavelet.pixels = stego.embedding(channel, enclosure, width, height)
    wavelet.iwt97_2d(1, width, height)
    return wavelet.pixels


def receive_message(wavelet, width, height):
    '''
    Функция, описывющая действия человека, принимающего
    изображение. Прямое преобразование и извлечение
    '''
    wavelet.fwt97_2d(1, width, height)
    extraction_empty = ''
    extraction = stego.extract(channel, width, height,
                               extraction_empty, len(enclosure))
    return extraction


@decorators.program_time
def main():
    pass


if __name__ == "__main__":
    start_time = time.time()
    photo = Image.open('Images/Image3.png')
    enclosure = consts.ENCLOSURE  # Вложение
    enc_l = len(enclosure)
    photo_width = photo.size[0]
    photo_height = photo.size[1]

    '''
    Ниже весь процесс передачи и приема изображения 
    со встроенной информацией
    '''
    channel = image_worker.get_channel(photo, photo_width, photo_height)
    wavelet = wavelet.CDF(channel)
    areas_list = sensetive_areas.SensetiveAreas(channel)
    channel = send_message(wavelet, enclosure, photo_width, photo_height)
    photo = image_worker.save_picture(channel, photo_width, photo_height, photo)
    photo.save('Images/Clock_stego.png', 'PNG')  # Изображение с вложением
    extraction = receive_message(wavelet, photo_width, photo_height)
    print("--- %s seconds ---" % (time.time() - start_time + 1))
    a = 0
