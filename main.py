import matplotlib.pyplot as plt

def plot_thread_execution_times(filename):
    priorities = []
    execution_times = []
    colors = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:
                priority_str, exec_time = parts[0], float(parts[1])

                if priority_str == "Default":
                    priority = 0 
                    colors.append('orange')
                else:
                    priority = int(priority_str)
                    colors.append('skyblue') 
                
                priorities.append(priority)
                execution_times.append(exec_time)

    labels = [f"{p}" if p != 0 else "Default(31)" for p in priorities]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(priorities, execution_times, color=colors, edgecolor='black')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom', fontweight='bold')

    plt.xlabel('Thread Priority Number', fontsize=12, fontweight='bold')
    plt.ylabel('Execution Time (ms)', fontsize=12, fontweight='bold')
    plt.title('Thread Execution Time vs Priority', fontsize=14, fontweight='bold')
    plt.xticks(priorities, labels, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    plt.show()

plot_thread_execution_times('threadData.txt')
