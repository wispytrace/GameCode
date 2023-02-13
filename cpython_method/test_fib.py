from test_fib import fib
import time

def fib_a(n):
    if n in [1, 2]:
        return 1
    
    return fib(n-1) + fib(n-2)



start = time.time()
fib_a(40)
end = time.time()

print(end-start)


start = time.time()
fib(40)
end = time.time()

print(end-start)