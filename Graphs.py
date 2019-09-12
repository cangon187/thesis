import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os, sys
from os import walk
from scipy.stats import sem, t
from urllib.parse import unquote


def graph_memory(files, collectors, workload):
    memory_cms(files[0] + '/jvm.log', workload, collectors[0])
    memory_g1(files[1] + '/jvm.log', workload, collectors[1])
    memory_shenandoah(files[2] + '/jvm.log', workload, collectors[2])
    memory_zgc(files[3] + '/jvm.log', workload, collectors[3])


def memory_cms(file, workload, collector):
    fig, ax = plt.subplots()
    before = []
    after = []
    time = []
    with open(file, 'r') as f:
        for line in f:
            if 'M->' in line:
                for element in line.split(' '):
                    if 'info' in element:
                        t = element.split(']')[0][1:len(element.split(']')[0]) - 1]
                        t = float(t.replace(',', '.'))
                        time.append(t)
                    if '->' in element:
                        before.append(int(element.split('M')[0]))
                        after.append(int(element.split('M')[1][2:]))

    for i in range(len(before)):
        plt.plot([time[i], time[i]], [0, before[i]], 'lightcoral')
        plt.plot([time[i], time[i]], [0, after[i]], 'c')

    plt.xlabel('Time (s)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100)
    # plt.show()
    plt.close(fig)


def memory_g1(file, workload, collector):
    fig, ax = plt.subplots()
    before = []
    after = []
    time = []
    with open(file, 'r') as f:
        for line in f:
            if 'Pause Young (Normal) (G1 Evacuation Pause) ' in line:
                for element in line.split(' '):
                    if '->' in element:
                        before.append((int(element.split('M')[0])))
                        after.append((int(element.split('M')[1][2:])))
                    if 'info' in element:
                        t = element.split(']')[0][1:len(element.split(']')[0]) - 1]
                        t = float(t.replace(',', '.'))
                        time.append(t)

    for i in range(len(before)):
        plt.plot([time[i], time[i]], [0, before[i]], 'lightcoral')
        plt.plot([time[i], time[i]], [0, after[i]], 'c')

    plt.xlabel('Time (s)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100)
    # plt.show()
    plt.close(fig)


def memory_shenandoah(file, workload, collector):
    fig, ax = plt.subplots()
    initial = 0
    before = []
    after = []
    time = []
    with open(file, 'r') as f:
        temp = []
        for line in f:
            if ', size: ' in line:
                initial = int(line.split(' ')[5])
            if '] Free:' in line:
                for element in line.split(' '):
                    if 'M' in element:
                        temp.append(initial - int(element[:len(element) - 1]))
                        break;
                if 'info' in line:
                    t = line.split(']')[0][1:len(line.split(']')[0]) - 1]
                    t = float(t.replace(',', '.'))
                    time.append(t)

    correct_time = []

    for i in range(len(temp)):
        if i % 2 == 0:
            before.append(temp[i])
        else:
            after.append(temp[i])
            correct_time.append(time[i])

    for i in range(len(before)):
        plt.plot([correct_time[i], correct_time[i]], [0, before[i]], 'lightcoral')
        plt.plot([correct_time[i], correct_time[i]], [0, after[i]], 'c')

    plt.xlabel('Time (s)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100)
    # plt.show()
    plt.close(fig)


def memory_zgc(file, workload, collector):
    fig, ax = plt.subplots()
    before = []
    after = []
    time = []
    with open(file, 'r') as f:
        for line in f:
            if 'Used:' in line:
                temp = []
                for element in line.split(' '):
                    if 'M' in element:
                        temp.append(element)
                before.append(int(temp[0][:len(temp[0]) - 1]))
                after.append(int(temp[3][:len(temp[3]) - 1]))
                if 'info' in line:
                    t = line.split(']')[0][1:len(line.split(']')[0]) - 1]
                    t = float(t.replace(',', '.'))
                    time.append(t)

    for i in range(len(before)):
        plt.plot([time[i], time[i]], [0, before[i]], 'lightcoral')
        plt.plot([time[i], time[i]], [0, after[i]], 'c')

    plt.xlabel('Time (s)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100)
    # plt.show()
    plt.close(fig)


def graph_latency(files, collectors, workload):
    latency(files[0] + '/jvm.log', workload, collectors[0])
    latency(files[1] + '/jvm.log', workload, collectors[1])
    latency(files[2] + '/jvm.log', workload, collectors[2])
    latency(files[3] + '/jvm.log', workload, collectors[3])


def latency(file, workload, collector):
    fig, ax = plt.subplots()
    data = []
    with open(file, 'r') as f:
        for line in f:
            if 'Total time for which application threads were stopped:' in line:
                inc = 1
                for element in line.split(' '):
                    if element != 'stopped:':
                        inc += 1
                    else:
                        data.append(float(line.split(' ')[inc].replace(',', '.')) * 1000)
                        break
    binwidth = 1
    plt.hist(data, bins=np.arange(0, max(data) + binwidth, binwidth), edgecolor='k')

    plt.xlabel('Time (ms)')
    plt.ylabel('Count')

    plt.title('latency_workload_' + workload + ' ' + collector, loc='right')

    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/latency_' + collector, dpi=100)
    # plt.show()
    plt.close(fig)


def mean_confidence_interval(data, confidence):
    n = len(data)
    std_err = sem(data)
    h = std_err * t.ppf((1 + confidence) / 2, n - 1)
    return h


def throughput(file, ax, boxplot_data, boxplot_errors, collector):
    operations = []
    with open(file, 'r') as f:
        for line in f:
            if 'Throughput:' in line:
                element = line.split(' ')[2]
                operations.append(element[:len(element) - 1])
    data = np.char.replace(operations, ',', '.')
    data = data.astype(np.float)
    data = data.astype(np.int)

    new_data = []
    for i in range(10, len(data), 10):
        new_data.append(data[i-10:i].sum())
    x = np.arange(0, len(new_data), 1)
    x = np.divide(x,10)

    if collector is 'cms':
        ax.plot(x, new_data, label=collector, color='b')
    if collector is 'g1':
        ax.plot(x, new_data, label=collector, color='lightcoral')
    if collector is 'shenandoah':
        ax.plot(x, new_data, label=collector, color='c')
    if collector is 'zgc':
        ax.plot(x, new_data, label=collector, color='gray')

    ax.ticklabel_format(style='plain')

    boxplot_data.append(new_data)
    boxplot_errors.append(mean_confidence_interval(new_data, 0.95))


def graph_throughput(files, collectors, workload):
    boxplot_data = []
    boxplot_errors = []
    fig = plt.figure()
    ax = fig.add_subplot(511)
    ax1 = fig.add_subplot(512)
    ax2 = fig.add_subplot(513)
    ax3 = fig.add_subplot(514)
    bp = fig.add_subplot(515)

    throughput(files[0] + '/microbench.log', ax, boxplot_data, boxplot_errors, collectors[0])
    throughput(files[1] + '/microbench.log', ax1, boxplot_data, boxplot_errors, collectors[1])
    throughput(files[2] + '/microbench.log', ax2, boxplot_data, boxplot_errors, collectors[2])
    throughput(files[3] + '/microbench.log', ax3, boxplot_data, boxplot_errors, collectors[3])

    boxplot_mean = [np.mean(boxplot_data[0]), np.mean(boxplot_data[1]), np.mean(boxplot_data[2])
                    ,np.mean(boxplot_data[3])]
    bp.errorbar(boxplot_mean, [1, 2, 3, 4], xerr=boxplot_errors, fmt='o')

    plt.yticks((1, 2, 3, 4), collectors)
    bp.yaxis.set_label_position('right')
    plt.title('throughput_workload_' + workload, loc='right')
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    ax3.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    fig.set_size_inches((18, 9), forward=False)
    plt.subplots_adjust(hspace=0.5)
    plt.savefig('graphs/' + workload + '/throughput', dpi=100)
    #plt.show()
    plt.close(fig)

def get_array_percent(percent):
    result_dir = []
    main_dir = []
    for (dir_path, dir_names, file_names) in walk('results/'):
        main_dir.extend(dir_names)
        break

    for sub_dir in main_dir:
        if sub_dir.split('-')[4] == percent:
            result_dir.append('results/' + sub_dir)

    return result_dir

def get_array_heap_size(heap_size):
    result_dir = []
    main_dir = []
    for (dir_path, dir_names, file_names) in walk('results/'):
        main_dir.extend(dir_names)
        break

    for sub_dir in main_dir:
        if sub_dir.split('-')[1] == heap_size:
            if sub_dir.split('-')[4] != '100':
                result_dir.append('results/' + sub_dir)
            else:
                tmp = 'results/' + sub_dir
    result_dir.append(tmp)

    return result_dir

def throughput_per_percent(array, percent):
    ind = np.arange(len(array))
    ind_name = []
    cms_array = []
    g1_array = []
    shenandoah_array = []
    zgc_array = []
    cms_array_std = []
    g1_array_std = []
    shenandoah_array_std = []
    zgc_array_std = []
    width = 0.10
    width_pos = [ind-width*1.5, ind-width/2, ind+width/2, ind+width*1.5]
    fig, ax = plt.subplots()
    for sub_dir in array:
        ind_name.append(sub_dir.split('-')[1])
        for gc in garbageCollectors:
            result = throughput_per_percent_extra(sub_dir + '/' + gc)
            if gc is 'cms':
                cms_array.append(result[0])
                cms_array_std.append(result[1])
            if gc is 'g1':
                g1_array.append(result[0])
                g1_array_std.append(result[1])
            if gc is 'shenandoah':
                shenandoah_array.append(result[0])
                shenandoah_array_std.append(result[1])
            if gc is 'zgc':
                zgc_array.append(result[0])
                zgc_array_std.append(result[1])

    ax.bar(width_pos[0], cms_array, width, yerr=cms_array_std, label='CMS')
    ax.bar(width_pos[1], g1_array, width, yerr=g1_array_std, label='G1')
    ax.bar(width_pos[2], shenandoah_array, width, yerr=shenandoah_array_std, label='SHENANDOAH')
    ax.bar(width_pos[3], zgc_array, width, yerr=zgc_array_std, label='ZGC')

    ax.set_ylabel('Operations')
    ax.set_xticks(ind)
    ax.set_xticklabels(ind_name)
    ax.set_title(percent + '% Reads on ' + array[0].split('-')[5] + ' Operations')
    ax.legend()
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/throughput_percent_' + percent, dpi=100)

def throughput_per_heap_size(array, heap_size):
    ind = np.arange(len(array)) # 7
    ind_name = []
    cms_array = []
    g1_array = []
    shenandoah_array = []
    zgc_array = []
    cms_array_std = []
    g1_array_std = []
    shenandoah_array_std = []
    zgc_array_std = []
    width = 0.10
    width_pos = [ind-width*1.5, ind-width/2, ind+width/2, ind+width*1.5]
    fig, ax = plt.subplots()
    for sub_dir in array:
        ind_name.append(sub_dir.split('-')[4] + '%')
        for gc in garbageCollectors:
            result = throughput_per_percent_extra(sub_dir + '/' + gc)
            if gc is 'cms':
                cms_array.append(result[0])
                cms_array_std.append(result[1])
            if gc is 'g1':
                g1_array.append(result[0])
                g1_array_std.append(result[1])
            if gc is 'shenandoah':
                shenandoah_array.append(result[0])
                shenandoah_array_std.append(result[1])
            if gc is 'zgc':
                zgc_array.append(result[0])
                zgc_array_std.append(result[1])

    ax.bar(width_pos[0], cms_array, width, yerr=cms_array_std, label='CMS')
    ax.bar(width_pos[1], g1_array, width, yerr=g1_array_std, label='G1')
    ax.bar(width_pos[2], shenandoah_array, width, yerr=shenandoah_array_std, label='SHENANDOAH')
    ax.bar(width_pos[3], zgc_array, width, yerr=zgc_array_std, label='ZGC')

    ax.set_ylabel('Operations')
    ax.set_xticks(ind)
    ax.set_xticklabels(ind_name)
    ax.set_title(array[0].split('-')[5] + ' Operations on a ' + heap_size + ' Max Heap Size')
    ax.legend()
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/throughput_heap_size_' + heap_size, dpi=100)

def throughput_per_percent_extra(path):
    result = []
    operations = []
    with open(path + '/microbench.log', 'r') as f:
        for line in f:
            if 'Throughput:' in line:
                element = line.split(' ')[2]
                operations.append(element[:len(element) - 1])
    operations = [ float(x) for x in operations ]
    operations = [ int(x) for x in operations]
    data = operations[30:len(operations)]

    result.append(np.mean(data))
    result.append(np.std(data))
    return result


garbageCollectors = ['cms', 'g1', 'shenandoah', 'zgc']

maindir = []
for (dirpath, dirnames, filenames) in walk('results/'):
    maindir.extend(dirnames)
    break
for f in maindir:
    subsubdir = []
    for (dirpath, dirnames, filenames) in walk('results/' + f):
        subsubdir.extend(dirnames)
        break
    read_stdout = []
    for final in subsubdir:
        read_stdout.append('results/' + f + '/' + final)
    workload = unquote(unquote(f))
    workload = workload.replace(':','-')
    #s.mkdir('graphs/' + workload)
    #graph_memory(read_stdout, garbageCollectors, workload)
    #graph_latency(read_stdout, garbageCollectors, workload)
    #graph_throughput(read_stdout, garbageCollectors, workload)

heap_sizes = ['4g', '6g', '8g']
percentages = ['0', '10', '30', '50', '70', '90', '100']

for heap_size in heap_sizes:
    throughput_per_heap_size(get_array_heap_size(heap_size), heap_size)
for percent in percentages:
    throughput_per_percent(get_array_percent(percent), percent)
