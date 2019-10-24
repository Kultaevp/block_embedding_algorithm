import time


def program_time(function_to_decorate):
    def the_wrapper_around_the_original_function():
        start_time = time.time()
        function_to_decorate() # Сама функция
        print("--- %s seconds ---" % (time.time() - start_time))
    return the_wrapper_around_the_original_function
