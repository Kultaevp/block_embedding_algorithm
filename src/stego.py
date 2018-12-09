import consts

quant = consts.QUANT_SIZE


def get_matrix_weight(picture, i_width, i_height, block_sum):
    '''
    Вычисление матрицы весов коэффициентов.
    Нужна для неравномерного распределения
    энергии внутри блока
    '''
    matrix_weight = list()
    for o in range(consts.BLOCK_HEIGHT):
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


# Функция встраивания
def embedding(picture, enclosure, width, height):
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
