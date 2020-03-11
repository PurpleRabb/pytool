import os
import re
import sys

import matplotlib.pyplot as plt

max_mem_lists = []
min_mem_lists = []
max_vm_lists = []
min_vm_lists = []

warning_list = []


def parse_meminfo(filename):
    memlists = []
    vmlists = []
    with open(filename, 'r') as meminfo:
        for line in meminfo.readlines():
            items = line.strip().split(':');
            for item in items:
                if item.strip() == 'MemAvailable':
                    memlists.append(items[-1].replace('kB', '').strip())
                if item.strip() == 'VmSize':
                    vmlists.append(items[-1].replace('kB', '').strip())
    if len(memlists) > 0:
        max1 = int(max(memlists))
        min1 = int(min(memlists))
        max_mem_lists.append(max1)
        min_mem_lists.append(min1)
        print('{0} ==> max available: {1} MB,min available {2} MB'.format(filename, max1 / 1000,
                                                                          min1 / 1000))
        if int(min(memlists)) / 1000 < 500:
            print("###########WARNING AVAIL MEM###############")
            warning_list.append(filename)
    if len(vmlists) > 0:
        _max = int(max(vmlists))
        _min = int(min(vmlists))
        max_vm_lists.append(_max)
        min_vm_lists.append(_min)
        print('{0} ==> max vmsize: {1} GB,min vmsize {2} GB'.format(filename, _max / 1000000,
                                                                    _min / 1000000))
        if int(max(vmlists)) / 1000000 > 3.0:
            print("###########WARNING VMSIZE#################")
            warning_list.append(filename)


def find_files(root_path):
    for item in os.listdir(root_path):
        path = os.path.join(root_path, item)
        if os.path.isfile(path):
            if item == 'proc_meminfo.txt':
                parse_meminfo(path)
            if re.match('proc_status', item):
                parse_meminfo(path)
        else:
            find_files(path)

if __name__ == "__main__":
    _mdir = sys.argv[1]

    if not os.path.isdir(_mdir):
        print('illegal directory')
        exit(-1)

    find_files(_mdir)

    plt.subplot(221)
    plt.title('max_vmsize(KB)')
    xValue = list(range(0, len(max_vm_lists)))
    plt.scatter(xValue, max_vm_lists, s=20, c="#12ff12", marker='o')

    plt.subplot(222)
    plt.title('min_vmsize(KB)')
    xValue = list(range(0, len(min_vm_lists)))
    plt.scatter(xValue, min_vm_lists, s=20, c="#ff1212", marker='o')

    plt.subplot(223)
    plt.title('max_avail_mem(KB)')
    xValue = list(range(0, len(max_mem_lists)))
    plt.scatter(xValue, max_mem_lists, s=20, c="#001212", marker='o')

    plt.subplot(224)
    plt.title('min_avail_mem(KB)')
    xValue = list(range(0, len(min_mem_lists)))
    plt.scatter(xValue, min_mem_lists, s=20, c="#ff12ff", marker='o')

    print(warning_list)
    plt.show()
