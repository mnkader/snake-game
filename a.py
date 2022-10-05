import time

start = time.perf_counter()

time.sleep(1.2)
end = 0
while True:
    if (end-start) > 1:
        print('stuck')
        break
    end = time.perf_counter()

print(f'{end-start}')