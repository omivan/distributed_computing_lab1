import matplotlib.pyplot as plt
import numpy as np

def plot_thread_execution_times(fifo_file, rr_file):
    fifo_priorities, fifo_execution_times = [], []
    rr_priorities, rr_execution_times = [], []
    fifo_default_exec_time = None
    rr_default_exec_time = None

    with open(fifo_file, 'r') as file:
        for line in file:
            parts = line.split()
            exec_time = float(parts[-1])
            if parts[0] == "Default":
                priority = 31
                fifo_default_exec_time = exec_time
            else:
                priority = int(parts[0])
                priority = min(priority, 63)
                fifo_priorities.append(priority)
                fifo_execution_times.append(exec_time)

    if fifo_default_exec_time is not None:
        fifo_priorities.insert(0, 31)
        fifo_execution_times.insert(0, fifo_default_exec_time)

    with open(rr_file, 'r') as file:
        for line in file:
            parts = line.split()
            exec_time = float(parts[-1])
            if parts[0] == "Default":
                priority = 31
                rr_default_exec_time = exec_time
            else:
                priority = int(parts[0])
                priority = min(priority, 63)
                rr_priorities.append(priority)
                rr_execution_times.append(exec_time)

    if rr_default_exec_time is not None:
        rr_priorities.insert(0, 31)
        rr_execution_times.insert(0, rr_default_exec_time)

    bar_width = 0.35
    index = np.arange(len(fifo_priorities))

    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(index - bar_width/2, fifo_execution_times, bar_width, label='SCHED_FIFO', color='royalblue')
    bars2 = ax.bar(index + bar_width/2, rr_execution_times, bar_width, label='SCHED_RR', color='coral')

    ax.set_xlabel('Thread Priority')
    ax.set_ylabel('Execution Time (ms)')
    ax.set_title('Comparison of Thread Execution Times by Scheduling Policy')
    ax.set_xticks(index)
    ax.set_xticklabels([f'Default(31)' if p == 31 else p for p in fifo_priorities])
    ax.legend()

    for bars in (bars1, bars2):
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{int(yval)}', ha='center', va='bottom', fontweight='bold')

    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', which='both', axis='y')
    plt.tight_layout()
    plt.show()

plot_thread_execution_times('threadDataFIFO.txt', 'threadDataRR.txt')
