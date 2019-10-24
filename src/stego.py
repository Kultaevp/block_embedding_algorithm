import consts
import PSNR
import functools
from src import Automata
from src import wavelet

quant = consts.QUANT_SIZE


def get_matrix_weight(picture, i_width, i_height, block_sum):
    '''
    Вычисление матрицы весов коэффициентов.
    Нужна для неравномерного распределения
    энергии внутри блока
    '''
    matrix_weight = list()
    for o in range(consts.BLOCK_HEIGHT):
        if block_sum == 0:
            matrix_weight.append(abs(picture[i_width][i_height + o]) / 1)
        else:
            matrix_weight.append(abs(picture[i_width][i_height + o]) / block_sum)
    return matrix_weight


def get_coefficients(block_sum):
    '''
    Вычисление двух вспомогательных коэффициентов
    для встаривания. а0 используется для встраивания
    нулевого бита, а1 - ждя единичного
    '''
    a0 = int(block_sum / quant) * quant + (quant / 4)
    a1 = int(block_sum / quant) * quant + (quant / 4 * 3)
    return a0, a1


@functools.lru_cache(maxsize=None)
def energy_distribution(start_block, embedded_block,
                        probability_a, probability_b, probability_change):
    cache = list()
    while True:
        start_transform = wavelet.CDF.iwt97(start_block, 1, len(start_block))
        embedded_transform = wavelet.CDF.iwt97(embedded_block, 1, len(embedded_block))
        psnr_start = PSNR.psnr(start_transform, embedded_transform)
        for i in range(embedded_block):
            if probability_a > probability_b:
                embedded_block[i] = embedded_block[i] - 1
                flag = i
                for i in range(embedded_block):
                    if flag != i:
                        embedded_block[i] = embedded_block[i] + 1/len(embedded_block)
            else:
                embedded_block[i] = embedded_block[i] + 1
                flag = i
                for i in range(embedded_block):
                    if flag != i:
                        embedded_block[i] = embedded_block[i] - 1 / len(
                            embedded_block)

            start_transform = wavelet.CDF.iwt97(start_block, 1,
                                                len(start_block))
            embedded_transform = wavelet.CDF.iwt97(embedded_block, 1,
                                                   len(embedded_block))
            psnr_finish = PSNR.psnr(start_transform, embedded_transform)
            if psnr_start < psnr_finish:
                probability_a += probability_change
                probability_b -= probability_change
                psnr_start = psnr_finish
            else:
                probability_b += probability_change
                probability_a -= probability_change
                psnr_start = psnr_finish
        cache.append(psnr_finish)
        if len(cache) > 2:
            cache.remove(1)
        if all(psnr_finish == value for value in cache):
            return embedded_block


# Функция встраивания
def embedding(picture, enclosure, width, height, automata=None):
    '''
    Функция встраивания. На входе изображение,
    вложение. На выходе изображение со встроенной
    в него информацией
    '''
    count = 0
    for i in range(0, int(width/2), consts.BLOCK_WIDTH):
        for j in range(int(height/2), height, consts.BLOCK_HEIGHT):
            block_sum = 0
            for o in range(consts.BLOCK_HEIGHT):
                block_sum += abs(picture[i][j + o])
            matrix_weight = get_matrix_weight(picture, i, j, block_sum)
            a0, a1 = get_coefficients(block_sum)

            cur_ebm = int(enclosure[count])
            cur_value = cur_ebm * a1 + (1 - cur_ebm) * a0 - block_sum
            for o in range(consts.BLOCK_HEIGHT):
                matrix_weight[o] *= cur_value
            for o in range(consts.BLOCK_HEIGHT):
                try:
                    distributed_block = energy_distribution(start_block=picture,
                                                        embedded_block=cur_value,
                                                        probability_a=consts.PROBABILITY_A,
                                                        probability_b=consts.PROBABILITY_B,
                                                        probability_change=consts.PROBABILITY_CNAHGE)
                except TypeError:
                    distributed_block = ''
                Automata.embedding(distributed_block)
                picture[i][j+o] = abs(picture[i][j+o]) + matrix_weight[o]
            matrix_weight.clear()
            count += 1
            if count == len(enclosure):
                break
        if count == len(enclosure):
            break
    return picture


# Функция извлечения
def extract(picture, width, height, extraction, enclosure_len):
    '''
    Функция для извлечения. На входе изображение
    с вложением, на выходе вложение.
    Извлекаемый бит зависит от суммы блока
    и параметра квантования, являющегося константой
    '''
    for i in range(0, int(width / 2), consts.BLOCK_WIDTH):
        for j in range(int(height/2), height, consts.BLOCK_HEIGHT):
            block_sum = 0
            for o in range(consts.BLOCK_HEIGHT):
                block_sum += abs(picture[i][j + o])
            if block_sum % quant < quant / 2:
                extraction += '0'
            else:
                extraction += '1'
            if len(extraction) == enclosure_len:
                break
        if len(extraction) == enclosure_len:
            break
    return extraction
