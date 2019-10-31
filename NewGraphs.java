import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import scipy
from os import walk
from os import path

garbage_collectors = ['cms', 'g1', 'shenandoah', 'zgc']
heap_sizes = ['4g', '6g', '8g']
percentages_reduced = ['0', '50', '100']
percentages_augmented = ['0', '10', '30', '50', '70', '90', '100']
latencies = ['latencyPercentile', 'latencyMax', 'latencySum']
primitive_directory = 'resultsPrimitive/'
non_primitive_directory = 'shenandoahResults/'


def mean_confidence_interval(data, confidence):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
    return h


def get_array_by_percentage(percent, results):
    result_dir = []
    main_dir = []
    for (dir_path, dir_names, file_names) in walk(results):
        main_dir.extend(dir_names)
        break
    for sub_dir in main_dir:
        if sub_dir.split('-')[4] == percent:
            result_dir.append(path.join(results, sub_dir + '/'))
    return result_dir


def get_array_by_heap_size(heap_size, results, percentages):
    result_dir = []
    main_dir = []
    tmp = None
    for (dir_path, dir_names, file_names) in walk(results):
        main_dir.extend(dir_names)
        break
    for sub_dir in main_dir:
        if sub_dir.split('-')[1] == heap_size and sub_dir.split('-')[4] in percentages:
            if sub_dir.split('-')[4] == '100':
                tmp = path.join(results, sub_dir + '/')
            else:
                result_dir.append(path.join(results, sub_dir + '/'))
    if tmp != None:
        result_dir.append(tmp)

    return result_dir


def graph_by_percentage(array, percent, metric):
    if metric.lower() in ['memory', 'throughput'] or metric in latencies:
        ind = np.arange(len(array))
        ind_name = []
        cms_array = []
        cms_std = []
        g1_array = []
        g1_std = []
        shenandoah_array = []
        shenandoah_std = []
        zgc_array = []
        zgc_std = []
        width = 0.10
        width_pos = [ind - width * 1.5, ind - width / 2, ind + width / 2, ind + width * 1.5]
        fig, ax = plt.subplots()
        for sub_dir in array:
            size = sub_dir.split('-')[1][:len(sub_dir.split('-')[1]) - 1]
            ind_name.append(size)
            for gc in garbage_collectors:
                if metric.lower() == 'memory':
                    result = memory_extra(sub_dir + '/' + gc, gc, size)
                elif metric.lower() == 'throughput':
                    result = throughput_extra(sub_dir + '/' + gc)
                elif metric in latencies:
                    result = latency_extra(sub_dir + '/' + gc, metric)
                if gc is 'cms':
                    cms_array.append(result[0])
                    if metric not in latencies:
                        cms_std.append(result[1])
                if gc is 'g1':
                    g1_array.append(result[0])
                    if metric not in latencies:
                        g1_std.append(result[1])
                if gc is 'shenandoah':
                    shenandoah_array.append(result[0])
                    if metric not in latencies:
                        shenandoah_std.append(result[1])
                if gc is 'zgc':
                    zgc_array.append(result[0])
                    if metric not in latencies:
                        zgc_std.append(result[1])

        if metric in latencies:
            ax.bar(width_pos[0], cms_array, width, label='CMS', color=(1,0.39,0.38))
            ax.bar(width_pos[1], g1_array, width, label='G1', color=(0.22,0.24,0.27))
            ax.bar(width_pos[2], shenandoah_array, width, label='SHENANDOAH', color=(0.0,0.68,0.71))
            ax.bar(width_pos[3], zgc_array, width, label='ZGC', color=(0.26,0.72,0.51))
            plt.yscale('symlog')
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        else:
            ax.bar(width_pos[0], cms_array, width, yerr=cms_std,
                   capsize=5, label='CMS', color=(1, 0.39, 0.38))
            ax.bar(width_pos[1], g1_array, width, yerr=g1_std,
                   capsize=5, label='G1', color=(0.22, 0.24, 0.27))
            ax.bar(width_pos[2], shenandoah_array, width, yerr=shenandoah_std,
                   capsize=5, label='SHENANDOAH', color=(0.0, 0.68, 0.71))
            ax.bar(width_pos[3], zgc_array, width, yerr=zgc_std,
                   capsize=5, label='ZGC', color=(0.26, 0.72, 0.51))

        if metric.lower() == 'memory':
            ax.set_ylabel('Average Memory (MB)', labelpad=20)
            ax.set_ylim(top=8192)
        elif metric.lower() == 'throughput':
            ax.set_ylabel('Operations', labelpad=20)
            # ax.set_ylim(top=300000)
        elif metric == 'latencyPercentile':
            ax.set_ylabel('95th Percentile (ms)', labelpad=20)
        elif metric == 'latencyMax':
            ax.set_ylabel('Max Pause Time (ms)', labelpad=20)
        elif metric == 'latencySum':
            ax.set_ylabel('Total Pause Time (ms)', labelpad=20)

        ax.set_xlabel('Heap Size (GB)', labelpad=20)
        ax.set_xticks(ind)
        ax.set_xticklabels(ind_name)
        ax.yaxis.grid(True)
        ax.set_title(percent + '% Reads on ' + array[0].split('-')[5] + ' Operations with a '
                     + array[0].split('-')[3][:len(array[0].split('-')[3]) - 1] + 'GB Workload', loc='right')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), edgecolor='black', fancybox=True, loc=1, ncol=4)
        fig.set_size_inches((18, 9), forward=False)

        if metric.lower() == 'memory':
            plt.savefig('graphs/memory_percent_' + percent, dpi=100)
        elif metric.lower() == 'throughput':
            plt.savefig('graphs/throughput_percent_' + percent, dpi=100)
        elif metric == 'latencyPercentile':
            plt.savefig('graphs/latency_percentile_percent_' + percent, dpi=100)
        elif metric == 'latencyMax':
            plt.savefig('graphs/latency_max_percent_' + percent, dpi=100)
        elif metric == 'latencySum':
            plt.savefig('graphs/latency_sum_percent_' + percent, dpi=100)

        plt.close(fig)


def graph_by_heap_size(array, heap_size, metric):
    if metric.lower() in ['memory', 'throughput'] or metric in latencies:
        ind = np.arange(len(array))
        ind_name = []
        cms_array = []
        g1_array = []
        shenandoah_array = []
        zgc_array = []
        cms_std = []
        g1_std = []
        shenandoah_std = []
        zgc_std = []
        width = 0.10
        width_pos = [ind - width * 1.5, ind - width / 2, ind + width / 2, ind + width * 1.5]
        fig, ax = plt.subplots()
        for sub_dir in array:
            size = sub_dir.split('-')[1][:len(sub_dir.split('-')[1]) - 1]
            ind_name.append(sub_dir.split('-')[4] + '%')
            for gc in garbage_collectors:
                if metric.lower() == 'memory':
                    result = memory_extra(sub_dir + '/' + gc, gc, size)
                elif metric.lower() == 'throughput':
                    result = throughput_extra(sub_dir + '/' + gc)
                elif metric in latencies:
                    result = latency_extra(sub_dir + '/' + gc, metric)

                if gc is 'cms':
                    cms_array.append(result[0])
                    if metric not in latencies:
                        cms_std.append(result[1])
                if gc is 'g1':
                    g1_array.append(result[0])
                    if metric not in latencies:
                        g1_std.append(result[1])
                if gc is 'shenandoah':
                    shenandoah_array.append(result[0])
                    if metric not in latencies:
                        shenandoah_std.append(result[1])
                if gc is 'zgc':
                    zgc_array.append(result[0])
                    if metric not in latencies:
                        zgc_std.append(result[1])

        if metric in latencies:
            ax.bar(width_pos[0], cms_array, width, label='CMS', color=(1,0.39,0.38))
            ax.bar(width_pos[1], g1_array, width, label='G1', color=(0.22,0.24,0.27))
            ax.bar(width_pos[2], shenandoah_array, width, label='SHENANDOAH', color=(0.0,0.68,0.71))
            ax.bar(width_pos[3], zgc_array, width, label='ZGC', color=(0.26,0.72,0.51))
            plt.yscale('symlog')
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        else:
            ax.bar(width_pos[0], cms_array, width, yerr=cms_std,
                   capsize=5, label='CMS', color=(1, 0.39, 0.38))
            ax.bar(width_pos[1], g1_array, width, yerr=g1_std,
                   capsize=5, label='G1', color=(0.22, 0.24, 0.27))
            ax.bar(width_pos[2], shenandoah_array, width, yerr=shenandoah_std,
                   capsize=5, label='SHENANDOAH', color=(0.0, 0.68, 0.71))
            ax.bar(width_pos[3], zgc_array, width, yerr=zgc_std,
                   capsize=5, label='ZGC', color=(0.26, 0.72, 0.51))

        if metric.lower() == 'memory':
            ax.set_ylabel('Average Memory (MB)', labelpad=20)
            ax.set_ylim(top=8192)
        elif metric.lower() == 'throughput':
            ax.set_ylabel('Operations', labelpad=20)
            # ax.set_ylim(top=300000)
        elif metric == 'latencyPercentile':
            ax.set_ylabel('95th Percentile (ms)', labelpad=20)
        elif metric == 'latencyMax':
            ax.set_ylabel('Max Pause Time (ms)', labelpad=20)
        elif metric == 'latencySum':
            ax.set_ylabel('Total Pause Time (ms)', labelpad=20)

        ax.set_xlabel('Percentage of Read Operations', labelpad=20)
        ax.set_xticks(ind)
        ax.set_xticklabels(ind_name)
        ax.yaxis.grid(True)
        ax.set_title(array[0].split('-')[5] + ' Operations on a ' + heap_size + ' Max Heap Size with a '
                     + array[0].split('-')[3][:len(array[0].split('-')[3]) - 1] + 'GB Workload', loc='right')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), edgecolor='black', fancybox=True, loc=1, ncol=4)
        fig.set_size_inches((18, 9), forward=False)

        if metric.lower() == 'memory':
            plt.savefig('graphs/memory_heap_size_' + heap_size, dpi=100)
        elif metric.lower() == 'throughput':
            plt.savefig('graphs/throughput_heap_size_' + heap_size, dpi=100)
        elif metric == 'latencyPercentile':
            plt.savefig('graphs/latency_percentile_heap_size_' + heap_size, dpi=100)
        elif metric == 'latencyMax':
            plt.savefig('graphs/latency_max_heap_size_' + heap_size, dpi=100)
        elif metric == 'latencySum':
            plt.savefig('graphs/latency_sum_heap_size_' + heap_size, dpi=100)

        plt.close(fig)


def memory_extra(file_path, collector, size):
    result = []
    operations = []
    with open(file_path + '/jvm.log', 'r') as f:
        if collector is not 'zgc':
            for line in f:
                if 'M->' in line and float(line[1:5]) > 30:
                    for segment in line.split(' '):
                        if 'M->' in segment:
                            operations.append(segment.split('M')[0])
                            operations.append(segment.split('M')[1][2:])
        if collector is 'zgc':
            for line in f:
                if ')->' in line and float(line[1:5]) > 30:
                    for segment in line.split(' '):
                        if ')->' in segment:
                            operations.append(segment.split('M')[0])
                            operations.append(segment.split('M')[1].split('>')[1])
    operations = [float(x) for x in operations]
    operations = [int(x) for x in operations]

    result.append(int(np.mean(operations)))
    result.append(int(np.std(operations)))
    return result


def throughput_extra(path):
    result = []
    operations = []
    with open(path + '/microbench.log', 'r') as f:
        for line in f:
            if 'Throughput:' in line:
                element = line.split(' ')[2]
                operations.append(element[:len(element) - 1])
    operations = [float(x) for x in operations]
    operations = [int(x) for x in operations]
    data = operations[3:len(operations)]

    result.append(np.mean(data))
    result.append(np.std(data))
    return result


def latency_extra(path, mode):
    result = []
    operations = []
    with open(path + '/jvm.log', 'r') as f:
        for line in f:
            if 'Total time for which application threads were stopped:' in line and float(line[1:5]) > 30:
                element = line.split(' ')
                count = 0
                for i in element:
                    if 'seconds' in i:
                        pause = element[count-1]
                        operations.append(pause)
                        break
                    count += 1
    operations = [float(x) for x in operations]
    operations = np.multiply(operations, 1000)
    operations = np.sort(operations)

    if mode == 'latencyPercentile':
        result.append(np.percentile(operations, 95))
    elif mode == 'latencyMax':
        result.append(np.max(operations))
    elif mode == 'latencySum':
        result.append(np.sum(operations))

    return result


def throughput_per_percent_compare(array1, array2, percent):
    for gc in garbage_collectors:

        ind = np.arange(len(array1))
        ind_name = []

        non_primitive_array = []
        primitive_array = []
        non_primitive_array_std = []
        primitive_array_std = []

        width = 0.10
        width_pos = [ind - width / 2, ind + width / 2]
        fig, ax = plt.subplots()

        for sub_dir in array1:
            ind_name.append(sub_dir.split('-')[1])
            result = throughput_extra(sub_dir + '/' + gc)
            non_primitive_array.append(result[0])
            non_primitive_array_std.append(result[1])

        for sub_dir in array2:
            result = throughput_extra(sub_dir + '/' + gc)
            primitive_array.append(result[0])
            primitive_array_std.append(result[1])

        ax.bar(width_pos[0], non_primitive_array, width, yerr=non_primitive_array_std,
               capsize=5, label='Non-primitive Workload', color=(1,0.39,0.38))
        ax.bar(width_pos[1], primitive_array, width, yerr=primitive_array_std,
               capsize=5, label='Primitive Workload', color=(0.0,0.68,0.71))

        ax.set_ylabel('Operations', labelpad=20)
        ax.set_xlabel('Heap Size', labelpad=20)
        ax.set_xticks(ind)
        ax.set_xticklabels(ind_name)
        ax.set_title(percent + '% Reads on ' + array1[0].split('-')[5] + ' Operations with ' + gc.upper() + ' with a '
                     + array1[0].split('-')[3][:len(array1[0].split('-')[3]) - 1] + 'GB Workload', loc='right')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), edgecolor='black', fancybox=True, loc=1, ncol=4)
        fig.set_size_inches((18, 9), forward=False)
        plt.savefig('graphs/throughput_percent_' + gc + '_' + percent, dpi=100)
        plt.close(fig)


def throughput_per_heap_size_compare(array1, array2, heap_size):
    for gc in garbage_collectors:

        ind = np.arange(len(array1))  # 7
        ind_name = []

        non_primitive_array = []
        primitive_array = []
        non_primitive_array_std = []
        primitive_array_std = []

        width = 0.10
        width_pos = [ind - width / 2, ind + width / 2]
        fig, ax = plt.subplots()

        for sub_dir in array1:
            ind_name.append(sub_dir.split('-')[4] + '%')
            result = throughput_extra(sub_dir + '/' + gc)
            non_primitive_array.append(result[0])
            non_primitive_array_std.append(result[1])

        for sub_dir in array2:
            ind_name.append(sub_dir.split('-')[4] + '%')
            result = throughput_extra(sub_dir + '/' + gc)
            primitive_array.append(result[0])
            primitive_array_std.append(result[1])

        ax.bar(width_pos[0], non_primitive_array, width, yerr=non_primitive_array_std,
               capsize=5, label='Non-primitive Workload', color=(1,0.39,0.38))
        ax.bar(width_pos[1], primitive_array, width, yerr=primitive_array_std,
               capsize=5, label='Primitive Workload', color=(0.0,0.68,0.71))

        ax.set_ylabel('Operations', labelpad=20)
        ax.set_xlabel('Percentage of Read Operations', labelpad=20)
        ax.set_xticks(ind)
        ax.set_xticklabels(ind_name)
        ax.set_title(array1[0].split('-')[5] + ' Operations on a ' + heap_size + ' Max Heap Size with ' + gc.upper()
                     + ' with a ' + array1[0].split('-')[3][:len(array1[0].split('-')[3]) - 1] + 'GB Workload',
                     loc='right')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), edgecolor='black', fancybox=True, loc=1, ncol=4)
        fig.set_size_inches((18, 9), forward=False)
        plt.savefig('graphs/throughput_heap_size_' + gc + '_' + heap_size, dpi=100)
        plt.close(fig)


def graphs_primitive():
    for percent in percentages_reduced:
        graph_by_percentage(get_array_by_percentage(percent, primitive_directory), percent, 'memory')
        graph_by_percentage(get_array_by_percentage(percent, primitive_directory), percent, 'throughput')
    for latency in latencies:
        for percent in percentages_reduced:
            graph_by_percentage(get_array_by_percentage(percent, primitive_directory), percent, latency)

    for heap_size in heap_sizes:
        graph_by_heap_size(get_array_by_heap_size(heap_size, primitive_directory, percentages_augmented),
                           heap_size, 'throughput')


def graphs_non_primitive():
    for percent in percentages_reduced:
        graph_by_percentage(get_array_by_percentage(percent, non_primitive_directory), percent, 'memory')
        graph_by_percentage(get_array_by_percentage(percent, non_primitive_directory), percent, 'throughput')
    for latency in latencies:
        for percent in percentages_reduced:
            graph_by_percentage(get_array_by_percentage(percent, non_primitive_directory), percent, latency)

    for heap_size in heap_sizes:
        graph_by_heap_size(get_array_by_heap_size(heap_size, non_primitive_directory, percentages_augmented),
                           heap_size, 'throughput')


def graphs_duo_compare():
    for percent in percentages_reduced:
        throughput_per_percent_compare(get_array_by_percentage(percent, non_primitive_directory),
                                       get_array_by_percentage(percent, primitive_directory),
                                       percent)

    for heap_size in heap_sizes:
        throughput_per_heap_size_compare(get_array_by_heap_size(heap_size, non_primitive_directory, percentages_augmented),
                                         get_array_by_heap_size(heap_size, primitive_directory, percentages_augmented),
                                         heap_size)


graphs_non_primitive()