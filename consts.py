# Коэффициенты из стандарта JPEG2000
COEFFICIENT_PACKAGE = {'alpha': -1.586134342,
                       'beta': -0.05298011854,
                       'gamma': 0.8829110762,
                       'delta': 0.4435068522,
                       'k1': 0.81289306611596146,
                       'k2': 0.61508705245700002}

COEFFICIENT_UN_PACKAGE = {'alpha': 1.586134342,
                          'beta': 0.05298011854,
                          'gamma': -0.8829110762,
                          'delta': -0.4435068522,
                          'k1': 1.230174104914,
                          'k2': 1.6257861322319229}
# Константы для встраивания
BLOCK_HEIGHT = 4
BLOCK_WIDTH = 1
QUANT_SIZE = 60
LOW_INTENS = 10
MEDIUM_INTENS = 20
BLOCK_LOW = [1, 10]
BLOCK_MEDIUM = [1, 6]
BLOCK_HIGH = [1, 4]
THRESHOLD = 120
AREA_SIZE = 64
PROBABILITY_A = 0.5
PROBABILITY_B = 0.5
PROBABILITY_CNAHGE = 0.1
ENCLOSURE = '1101110101110011011010011101011'
