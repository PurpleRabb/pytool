import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import os

m_list = []
m_list_Java_Heap = []
m_list_total = []
m_list_private_dirty = []

with open("meminfo-ptt.txt", 'r') as f_mem:
    for line in f_mem.readlines():
        if "Dalvik Heap" in line:
            # print(line)
            lists = line.split("    ")
            m_list.append(int(lists[2].strip()))
        if "TOTAL:" in line:
            lists = line.split("   ")
            m_list_total.append(int(lists[6].strip()))
        if "Java Heap:" in line:
            lists = line.split(":")
            # print(lists[1].strip())
            m_list_Java_Heap.append(int(lists[1].strip()))
        if "TOTAL   " in line:
            lists = line.split("   ")
            m_list_private_dirty.append(int(lists[4].strip()))

# print(m_list)
# print(np.array(m_list))
# print(m_list_total)

plt.figure(figsize=(9, 7))
# plt.subplot(4,1,1)
# plt.title("Dalvik Heap:",loc="left")
# plt.scatter(np.arange(0, len(m_list)), np.array(m_list), marker='x', linewidths=0.1)
# max_value = int(max(m_list))
# min_value = int(min(m_list))
# print(max_value, min_value)
# # plt.ylim(min_value, max_value)
# plt.yticks(np.linspace(min_value // 1000 * 1000, (max_value // 1000 + 1) * 1000, 10))

plt.subplot(2, 1, 1)
plt.title("Total:", loc="left")
x = np.arange(0, len(m_list_total))
y = np.array(m_list_total)
lr = LinearRegression()
lr.fit(x.reshape(-1, 1), y)
plt.plot(x, lr.coef_ * x + lr.intercept_, 'r-')
plt.scatter(np.arange(0, len(m_list_total)), np.array(m_list_total), marker='x', linewidths=0.1)
max_value = int(max(m_list_total))
min_value = int(min(m_list_total))
# print(max_value, min_value)
# plt.ylim(min_value, max_value)
plt.yticks(np.linspace(min_value // 1000 * 1000, (max_value // 1000 + 1) * 1000, 10))

# plt.subplot(4,1,3)
# plt.title("JAVA_HEAP:",loc="right")
# plt.scatter(np.arange(0, len(m_list_Java_Heap)), np.array(m_list_Java_Heap), marker='x', linewidths=0.1)
# max_value = int(max(m_list_Java_Heap))
# min_value = int(min(m_list_Java_Heap))
# print(max_value, min_value)
# # plt.ylim(min_value, max_value)
# plt.yticks(np.linspace(min_value // 1000 * 1000, (max_value // 1000 + 1) * 1000, 10))


plt.subplot(2, 1, 2)
plt.title("Private Dirty:", loc="left")
x = np.arange(0, len(m_list_private_dirty))
y = np.array(m_list_private_dirty)
lr = LinearRegression()
lr.fit(x.reshape(-1, 1), y)
plt.plot(x, lr.coef_ * x + lr.intercept_, 'r-')
plt.scatter(np.arange(0, len(m_list_private_dirty)), np.array(m_list_private_dirty), marker='x', linewidths=0.1)
max_value = int(max(m_list_private_dirty))
min_value = int(min(m_list_private_dirty))
# print(max_value, min_value)
# plt.ylim(min_value, max_value)
plt.yticks(np.linspace(min_value // 1000 * 1000, (max_value // 1000 + 1) * 1000, 10))


plt.show()
