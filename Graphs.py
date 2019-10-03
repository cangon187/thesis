import numpy as np
import matplotlib
import scipy
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
            if 'M->' in line and float(line[1:5]) > 30:
                for element in line.split(' '):
                    if 'info' in element:
                        t = element.split(']')[0][1:len(element.split(']')[0]) - 1]
                        t = float(t.replace(',', '.'))
                        time.append(t)
                    if '->' in element:
                        before.append(int(element.split('M')[0]))
                        after.append(int(element.split('M')[1][2:]))

    for i in range(len(time)):
        plt.plot([time[i], time[i]], [0, before[i]], 'lightcoral')
        plt.plot([time[i], time[i]], [0, after[i]], 'c')

    plt.xlabel('Time (s)', labelpad=20)
    plt.ylabel('Memory utilisation (MB)', labelpad=20)

    workload_split = workload.split('-')
    title = collector.upper()  + ' | ' + 'Heap Size ' + workload_split[1][:len(workload_split[1])-1] + 'GB' \
            + ' | ' + 'Data Size ' + workload_split[3][:len(workload_split[3])-1] + 'GB'\
            + ' | ' + 'Read Percentage ' + workload_split[4] + '%' \
            + ' | ' + 'Operations ' + workload_split[5]

    plt.title(title , loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector.upper() + ' before GC')
    after_patch = mpatches.Patch(color='c', label=collector.upper() + ' after GC')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102),
              edgecolor='black', fancybox=True,
              loc=1, ncol=2)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100, bbox_inches = 'tight', pad_inches = 0.5)
    # plt.show()
    plt.close(fig)


def memory_g1(file, workload, collector):
    fig, ax = plt.subplots()
    before = []
    after = []
    time = []
    with open(file, 'r') as f:
        for line in f:
            if 'Pause Young (Normal) (G1 Evacuation Pause) ' in line and float(line[1:5]) > 30:
                for element in line.split(' '):
                    if 'info' in element:
                        t = element.split(']')[0][1:len(element.split(']')[0]) - 1]
                        t = float(t.replace(',', '.'))
                        time.append(t)
                    if '->' in element:
                        before.append((int(element.split('M')[0])))
                        after.append((int(element.split('M')[1][2:])))

    for i in range(len(time)):
        plt.plot([time[i], time[i]], [0, before[i]], 'lightcoral')
        plt.plot([time[i], time[i]], [0, after[i]], 'c')

    plt.xlabel('Time (s)', labelpad=20)
    plt.ylabel('Memory utilisation (MB)', labelpad=20)

    workload_split = workload.split('-')
    title = collector.upper()  + ' | ' + 'Heap Size ' + workload_split[1][:len(workload_split[1])-1] + 'GB' \
            + ' | ' + 'Data Size ' + workload_split[3][:len(workload_split[3])-1] + 'GB'\
            + ' | ' + 'Read Percentage ' + workload_split[4] + '%' \
            + ' | ' + 'Operations ' + workload_split[5]

    plt.title(title , loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector.upper() + ' before GC')
    after_patch = mpatches.Patch(color='c', label=collector.upper() + ' after GC')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102),
              edgecolor='black', fancybox=True,
              loc=1, ncol=2)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100, bbox_inches = 'tight', pad_inches = 0.5)
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

    newTime = []
    newBefore = []
    newAfter = []

    iterator = 0
    while iterator < len(correct_time):
        if correct_time[iterator] > 30 :
            newTime.append(correct_time[iterator])
            newBefore.append(before[iterator])
            newAfter.append(after[iterator])
        iterator += 1

    for i in range(len(newTime)):
        plt.plot([newTime[i], newTime[i]], [0, newBefore[i]], 'lightcoral')
        plt.plot([newTime[i], newTime[i]], [0, newAfter[i]], 'c')

    plt.xlabel('Time (s)', labelpad=20)
    plt.ylabel('Memory utilisation (MB)', labelpad=20)

    workload_split = workload.split('-')
    title = collector.upper()  + ' | ' + 'Heap Size ' + workload_split[1][:len(workload_split[1])-1] + 'GB' \
            + ' | ' + 'Data Size ' + workload_split[3][:len(workload_split[3])-1] + 'GB'\
            + ' | ' + 'Read Percentage ' + workload_split[4] + '%' \
            + ' | ' + 'Operations ' + workload_split[5]

    plt.title(title , loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector.upper() + ' before GC')
    after_patch = mpatches.Patch(color='c', label=collector.upper() + ' after GC')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102),
              edgecolor='black', fancybox=True,
              loc=1, ncol=2)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100, bbox_inches = 'tight', pad_inches = 0.5)
    # plt.show()
    plt.close(fig)


def memory_zgc(file, workload, collector):
    fig, ax = plt.subplots()
    before = []
    after = []
    time = []
    with open(file, 'r') as f:
        for line in f:
            if 'Used:' in line and float(line[1:5]) > 30:
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

    for i in range(len(time)):
        plt.plot([time[i], time[i]], [0, before[i]], 'lightcoral')
        plt.plot([time[i], time[i]], [0, after[i]], 'c')

    plt.xlabel('Time (s)', labelpad=20)
    plt.ylabel('Memory utilisation (MB)', labelpad=20)

    workload_split = workload.split('-')
    title = collector.upper()  + ' | ' + 'Heap Size ' + workload_split[1][:len(workload_split[1])-1] + 'GB' \
            + ' | ' + 'Data Size ' + workload_split[3][:len(workload_split[3])-1] + 'GB'\
            + ' | ' + 'Read Percentage ' + workload_split[4] + '%' \
            + ' | ' + 'Operations ' + workload_split[5]

    plt.title(title , loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector.upper() + ' before GC')
    after_patch = mpatches.Patch(color='c', label=collector.upper() + ' after GC')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102),
              edgecolor='black', fancybox=True,
              loc=1, ncol=2)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/memory_' + collector, dpi=100, bbox_inches = 'tight', pad_inches = 0.5)
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
    plt.hist(data, bins=np.arange(0, max(data) + binwidth, binwidth), color='c', edgecolor='k')

    plt.xlabel('Time (ms)')
    plt.ylabel('Count')

    workload_split = workload.split('-')
    title = collector.upper()  + ' | ' + 'Heap Size ' + workload_split[1][:len(workload_split[1])-1] + 'GB' \
            + ' | ' + 'Data Size ' + workload_split[3][:len(workload_split[3])-1] + 'GB'\
            + ' | ' + 'Read Percentage ' + workload_split[4] + '%' \
            + ' | ' + 'Operations ' + workload_split[5]

    plt.title(title , loc='right')

    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('graphs/' + workload + '/latency_' + collector, dpi=100)
    # plt.show()
    plt.close(fig)


def mean_confidence_interval(data, confidence):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
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

    if collector is 'cms':
        ax.plot(x[30:], new_data[30:], label=collector.upper(), color='b')
    if collector is 'g1':
        ax.plot(x[30:], new_data[30:], label=collector.upper(), color='lightcoral')
    if collector is 'shenandoah':
        ax.plot(x[30:], new_data[30:], label=collector.upper(), color='c')
    if collector is 'zgc':
        ax.plot(x[30:], new_data[30:], label=collector.upper(), color='gray')

    ax.ticklabel_format(style='plain')

    boxplot_data.append(data[30:])
    boxplot_errors.append(mean_confidence_interval(data[30:], 0.95))


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

    collectorsUpper = []

    for x in collectors:
        collectorsUpper.append(x.upper())

    plt.yticks((1, 2, 3, 4), collectorsUpper)
    bp.yaxis.set_label_position('right')

    workload_split = workload.split('-')
    title = 'Heap Size ' + workload_split[1][:len(workload_split[1]) - 1] + 'GB' \
            + ' | ' + 'Data Size ' + workload_split[3][:len(workload_split[3]) - 1] + 'GB' \
            + ' | ' + 'Read Percentage ' + workload_split[4] + '%' \
            + ' | ' + 'Operations ' + workload_split[5]

    ax.set_title(title, loc='right')

    ax.legend(loc=1, ncol=1, borderaxespad=0., edgecolor='black', fancybox=True,)
    ax1.legend(loc=1, ncol=1, borderaxespad=0., edgecolor='black', fancybox=True,)
    ax2.legend(loc=1, ncol=1, borderaxespad=0., edgecolor='black', fancybox=True,)
    ax3.legend(loc=1, ncol=1, borderaxespad=0., edgecolor='black', fancybox=True,)
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

    tmp = None

    for sub_dir in main_dir:
        if sub_dir.split('-')[1] == heap_size:
            if sub_dir.split('-')[4] != '100':
                result_dir.append('results/' + sub_dir)
            else:
                tmp = 'results/' + sub_dir
    if tmp is not None:
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

    ax.bar(width_pos[0], cms_array, width, yerr=cms_array_std, label='CMS', color='b')
    ax.bar(width_pos[1], g1_array, width, yerr=g1_array_std, label='G1', color='lightcoral')
    ax.bar(width_pos[2], shenandoah_array, width, yerr=shenandoah_array_std, label='SHENANDOAH', color='c')
    ax.bar(width_pos[3], zgc_array, width, yerr=zgc_array_std, label='ZGC', color='gray')

    ax.set_ylabel('Operations')
    ax.set_xlabel('Heap Size')
    ax.set_xticks(ind)
    ax.set_xticklabels(ind_name)
    ax.set_title(percent + '% Reads on ' + array[0].split('-')[5] + ' Operations', loc='right')
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), edgecolor='black', fancybox=True, loc=1, ncol=4)
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

    ax.bar(width_pos[0], cms_array, width, yerr=cms_array_std, label='CMS', color='b')
    ax.bar(width_pos[1], g1_array, width, yerr=g1_array_std, label='G1', color='lightcoral')
    ax.bar(width_pos[2], shenandoah_array, width, yerr=shenandoah_array_std, label='SHENANDOAH', color='c')
    ax.bar(width_pos[3], zgc_array, width, yerr=zgc_array_std, label='ZGC', color='gray')

    ax.set_ylabel('Operations')
    ax.set_xlabel('Percentage of Read Operations')
    ax.set_xticks(ind)
    ax.set_xticklabels(ind_name)
    ax.set_title(array[0].split('-')[5] + ' Operations on a ' + heap_size + ' Max Heap Size', loc='right')
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), edgecolor='black', fancybox=True, loc=1, ncol=4)
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
    if not os.path.exists('graphs/' + workload):
        os.mkdir('graphs/' + workload)
    graph_memory(read_stdout, garbageCollectors, workload)
    graph_latency(read_stdout, garbageCollectors, workload)
    graph_throughput(read_stdout, garbageCollectors, workload)

heap_sizes = ['4g', '6g', '8g']
percentages = ['0', '10', '30', '50', '70', '90', '100']

for heap_size in heap_sizes:
    throughput_per_heap_size(get_array_heap_size(heap_size), heap_size)
for percent in percentages:
    throughput_per_percent(get_array_percent(percent), percent)
