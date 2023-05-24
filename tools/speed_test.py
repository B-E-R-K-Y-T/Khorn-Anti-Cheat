import time 



def trace_speed(func):
    def wrapper(*args, **kwargs):
        start = time.time() 
        res = func(*args, **kwargs)
        end = time.time() 

        with open(f'trace_speed_function_{func.__name__}.txt', 'w') as f:
            f.write(f'NAME FUNCTION={func.__name__}\nTIME={end - start}')
        
        return res
        
    return wrapper

if __name__ == '__main__':
    @trace_speed
    def test():
        time.sleep(1)

    
    test()
