class Timer:
    def __init__(self, option='real'):
        assert option in ('real', 'process')
        
        if option == 'real':
            from time import get_clock_info, clock as time
            res = get_clock_info('clock').resolution
        elif option == 'process':
            from time import process_time as time
            res = 1/64
            
        self.time = time
        self.res = res
        self.last = 0
        print(f'Finest resolution is {res} seconds.')

    def get(self, integer=False):
        now = self.time()
        delay = round((now - self.last)/self.res)
        self.last = now
        return delay if integer else delay*self.res

def measure(count=1, option='real'):
    timer = Timer(option)
    res = timer.res
    def factory(func):
        if count != 1:
            from matplotlib import pyplot as plt
            def timed_func(*args, **kwargs):
                times = []
                for i in range(count):
                    timer.get()
                    ret = func(*args, **kwargs)
                    times.append(timer.get(integer=True))
                fig, ax = plt.subplots(figsize=(16, 3))
                left, right = min(times)-1, max(times)
                bins = [(i+0.5)*res for i in range(left, right, (right-left-1)//20+1)]
                plt.hist([delay*res for delay in times], bins=bins)
                ax.set_xticks([(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)])
                plt.xlabel('milliseconds')
                plt.ylabel('count')
                print(f'{func.__name__}: {sum(times)/len(times)*res*1000:.4f} milliseconds (averaged over {count} samples)')
                plt.show()
                return ret
        else:
            def timed_func(*args, **kwargs):
                timer.get()
                ret = func(*args, **kwargs)
                print(f'{func.__name__}: {timer.get()*1000:.4f} milliseconds (averaged over {count} samples)')
                return ret
        return timed_func
    return factory
        
        