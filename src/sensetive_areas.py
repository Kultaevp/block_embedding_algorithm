import consts
import numpy


class SensetiveAreas:

    def __init__(self, input_picture):
        self.pixels = input_picture

    def _fft2(self):
        return

    def __fft2(self, area_size):
        areas_list = list()
        fourier = []
        full = area_size ** 2
        while True:
            for i in range(area_size):
                for j in range(area_size):
                    fourier = numpy.fft2(self.pixels, s=None, axes=(-2, -1))
            temp_max = max(fourier)
            for w in range(area_size):
                for h in range(area_size):
                    fourier[w][h] = fourier[w][h] / temp_max * 255
                    if fourier[w][h] < consts.THRESHOLD:
                        fourier[w][h] = 0
            count = 0
            for w in range(area_size):
                for h in range(area_size):
                    if fourier[w][h] != 0:
                        count += 1
            class_of_area = count / full * 100
            if class_of_area < consts.LOW_INTENS:
                areas_list.append(1)
            elif class_of_area < consts.MEDIUM_INTENS:
                areas_list.append(2)
            else:
                areas_list.append(3)
            if i + len(area_size) >= len(self.pixels):
                break
        return areas_list


