import time

# 1 普通写法
start_time_1 = time.time()
arr = []
for i in range(100000):
    arr.append(i)
delta_time_1 = time.time() - start_time_1
print(delta_time_1)


# 2 生成表达式写法
start_time_2 = time.time()
arr = [i for i in range(100000)]
delta_time_2 = time.time() - start_time_2
print(delta_time_2)

print(delta_time_2 - delta_time_1)

# 对于像python这种的脚本编译型语言来说,语言上的语法更能达到优化性能的作用,有时候会比逻辑更重要