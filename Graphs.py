import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import sem, t


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

    plt.xlabel('Time (ms)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('microbench/memory_workload_' + workload + ' ' + collector, dpi=100)
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

    plt.xlabel('Time (ms)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('microbench/memory_workload_' + workload + ' ' + collector, dpi=100)
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

    plt.xlabel('Time (ms)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('microbench/memory_workload_' + workload + ' ' + collector, dpi=100)
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

    plt.xlabel('Time (ms)')
    plt.ylabel('Memory (MB)')

    plt.title('memory_workload_' + workload + ' ' + collector, loc='right')

    before_patch = mpatches.Patch(color='lightcoral', label=collector + ' Before')
    after_patch = mpatches.Patch(color='c', label=collector + ' After')

    ax.legend(handles=[before_patch, after_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=2, mode='expand',
              borderaxespad=0.)

    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    fig.set_size_inches((18, 9), forward=False)
    plt.savefig('microbench/memory_workload_' + workload + ' ' + collector, dpi=100)
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
    plt.savefig('microbench/latency_workload_' + workload + ' ' + collector, dpi=100)
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
                element = line.split(' ')[1]
                operations.append(element[:len(element) - 1])
    data = np.char.replace(operations, ',', '.')
    data = data.astype(np.float)

    new_data = []
    for i in range(1000, len(data), 1000):
        new_data.append(data[i-1000:i].sum())

    x = np.arange(0, len(new_data), 1)

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
    ax = fig.add_subplot(411)
    ax1 = fig.add_subplot(412)
    ax2 = fig.add_subplot(413)
    ax3 = fig.add_subplot(514)
    bp = fig.add_subplot(414)

    throughput(files[0] + '/microbench.log', ax, boxplot_data, boxplot_errors, collectors[0])
    throughput(files[1] + '/microbench.log', ax1, boxplot_data, boxplot_errors, collectors[1])
    throughput(files[2] + '/microbench.log', ax2, boxplot_data, boxplot_errors, collectors[2])
    throughput(files[3] + '/microbench.log', ax3, boxplot_data, boxplot_errors, collectors[3])

    boxplot_mean = [np.mean(boxplot_data[0]), np.mean(boxplot_data[1]), np.mean(boxplot_data[2])
                    ,np.mean(boxplot_data[3])]
    bp.errorbar(boxplot_mean, [1, 2, 3], xerr=boxplot_errors, fmt='o')

    plt.yticks((1, 2, 3, 4), collectors)
    bp.yaxis.set_label_position('right')
    plt.title('throughput_workload_' + workload, loc='right')
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    ax3.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    fig.set_size_inches((18, 9), forward=False)
    plt.subplots_adjust(hspace=0.5)
    plt.savefig('microbench/throughput_workload_' + workload, dpi=100)
    #plt.show()
    plt.close(fig)


garbageCollectors = ['cms', 'g1', 'shenandoah', 'zgc']

#####################################################
##### EDIT BELOW ####################################

# Colocar aqui os relative paths dos resultados
read_stdout4 = ['microbench/thesis-cms-2g-2g-1562678077',
                'microbench/thesis-g1-2g-2g-1562678242',
                'microbench/thesis-shenandoah-2g-2g-1562678365',
                'microbench/thesis-zgc-2g-2g-1562678484']

# graph_memory gera gráfico de memória (vai para ./microbench/ folder)
# graph_latency gera gráfico de latencia (vai para ./microbench/ folder)
# graph_throughput gera gráfico de throughput (Ainda não está a ser logged) (vai para ./microbench/ folder)

graph_memory(read_stdout4, garbageCollectors, '4gb')
graph_latency(read_stdout4, garbageCollectors, '4gb')

