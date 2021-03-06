import copy

from consts import COEFFICIENT_PACKAGE, COEFFICIENT_UN_PACKAGE


def sort_pixels(pixels, width, height):
    '''
    Сортировка пикселей по областям высоких
    и низких частот после проведения вейвлет-преобразования.
    На вход изображение после преобразования, на выходе
    отсортированное изображение
    '''
    k1 = COEFFICIENT_PACKAGE['k1']
    k2 = COEFFICIENT_PACKAGE['k2']
    temp_bank = copy.deepcopy(pixels)

    for row in range(height):
        for col in range(width):
            if row % 2 == 0:
                temp_bank[col][int(row/2)] = k1 * pixels[row][col]
            else:
                new_row = row / 2 + height / 2
                temp_bank[col][int(new_row)] = k2 * pixels[row][col]
    for row in range(width):
        for col in range(height):
            pixels[row][col] = temp_bank[row][col]
    return pixels


def inverse_sort_pixels(pixels, width, height):
    '''
    Обратная сортировка для проведения обратного
    вейвлет-преобразования. На входе отсортированное
    изображение, на выходе неотсортированное изображение
    '''
    k1 = COEFFICIENT_UN_PACKAGE['k1']
    k2 = COEFFICIENT_UN_PACKAGE['k2']
    temp_bank = copy.deepcopy(pixels)

    for col in range(int(width / 2)):
        for row in range(height):
            new_temp = k1 * pixels[row][col]
            temp_bank[col * 2][row] = new_temp
            new_temp = k2 * pixels[row][int(col + width / 2)]
            temp_bank[col * 2 + 1][row] = new_temp
    for row in range(width):
        for col in range(height):
            pixels[row][col] = temp_bank[row][col]
    return pixels


class CDF:

    def __init__(self, input_picture):
        self.pixels = input_picture

    def __transformation_pixels(self, coef, start_point, finish_point, col):
        '''
        Один круг вейвлет преобразования.
        Всего кругов 4, для каждого из коэффициентов
        из JPEG2000 (alpha, beta, gamma, delta).
        '''
        for row in range(start_point, finish_point, 2):
            previous_px = self.pixels[row - 1][col]
            next_px = self.pixels[row + 1][col]
            transf_px = coef * (previous_px + next_px)
            self.pixels[row][col] += transf_px

    def fwt97(self, width, height):
        '''
        Прямое вейвлет-преобразование для одномерного
        изображения (строки пикселей). На вход
        исходное изображение, на выходе изображение,
        разделенное на области различных частот
        '''
        alpha = COEFFICIENT_PACKAGE['alpha']
        beta = COEFFICIENT_PACKAGE['beta']
        gamma = COEFFICIENT_PACKAGE['gamma']
        delta = COEFFICIENT_PACKAGE['delta']

        for col in range(height):
            CDF.__transformation_pixels(self, alpha, 1, height-1, col)
            transf_px = 2 * alpha * self.pixels[height - 2][col]
            self.pixels[height-1][col] += transf_px
            CDF.__transformation_pixels(self, beta, 2, height, col)
            self.pixels[0][col] += 2 * beta * self.pixels[1][col]
            CDF.__transformation_pixels(self, gamma, 1, height-1, col)
            new_value = 2 * gamma * self.pixels[height-2][col]
            self.pixels[height-1][col] += new_value
            CDF.__transformation_pixels(self, delta, 2, height, col)
            self.pixels[0][col] += 2 * delta * self.pixels[1][col]
        return sort_pixels(self.pixels, width, height)

    def fwt97_2d(self, num_of_levels, width, height):
        '''
        Прямое вейлет преобразование для двумерного
        изображения. num_of_levels - количество
        кругов преобразования. Одним кругом является
        проведения преобразования и сортировки
        '''
        wave = CDF(self.pixels)
        for i in range(num_of_levels):
            self.pixels = wave.fwt97(width, height)
            self.pixels = wave.fwt97(width, height)
            width /= 2
            height /= 2

    def iwt97(self, width, height):
        '''
        Обратное вейвлет-преобразование
        для одномерного изображения
        '''
        alpha = COEFFICIENT_UN_PACKAGE['alpha']
        beta = COEFFICIENT_UN_PACKAGE['beta']
        gamma = COEFFICIENT_UN_PACKAGE['gamma']
        delta = COEFFICIENT_UN_PACKAGE['delta']

        self.pixels = inverse_sort_pixels(self.pixels, width, height)
        for col in range(width):
            CDF.__transformation_pixels(self, delta, 2, height, col)
            self.pixels[0][col] += 2 * delta * self.pixels[1][col]
            CDF.__transformation_pixels(self, gamma, 1, height-1, col)
            new_value = 2 * gamma * self.pixels[height-2][col]
            self.pixels[height-1][col] += new_value
            CDF.__transformation_pixels(self, beta, 2, height, col)
            self.pixels[0][col] += 2 * beta * self.pixels[1][col]
            CDF.__transformation_pixels(self, alpha, 1, height-1, col)
            new_value = 2 * alpha * self.pixels[height-2][col]
            self.pixels[height-1][col] += new_value

    def iwt97_2d(self, num_of_levels, width, height):
        '''
        Обратное вейвлет-преобразование
        для двумерного изображения
        '''
        wave = CDF(self.pixels)
        for i in range(num_of_levels-1):
            height /= 2
            width /= 2
        for i in range(num_of_levels):
            wave.iwt97(width, height)
            wave.iwt97(width, height)
            width *= 2
            height *= 2
