import pandas as pd
import matplotlib.pyplot as plt
import math

# Load the CSV file
df = pd.read_csv('output.csv')
df['disk_accesses'] = df['reads'] + df['writes']
df['disk_accesses_log'] = df['disk_accesses'].apply(lambda x: math.log(x, 10))
df['fault_rate_log'] = df['fault_rate'].apply(lambda x: math.log(x, 2))
df['frames_log'] = df['frames'].apply(lambda x: math.log(x, 2))

# Display the first few rows of the dataframe
print(df.head())

# Assuming the CSV file has columns like 'mmu', 'trace', 'frames', 'fault_rate', 'reads', and 'writes'

# Plot 1: Page Fault Rate vs. Number of Frames for each algorithm

def plot_fault_rate(subset: pd.DataFrame, label: str, show: bool = False):
    traces = sorted(subset['trace'].unique())
    mmus = sorted(set(subset['mmu']))

    traces_dep = None

    if len(traces) == 1:
        traces_dep = True
    if len(mmus) == 1:
        traces_dep = False

    plt.figure(figsize=(10, 6))
    if traces_dep:
        for mmu in mmus:
            subset2 = subset[subset['mmu'] == mmu]
            print(subset2.to_string())
            plt.plot(subset2['frames_log'], subset2['fault_rate_log'], marker='o', label=mmu)
    else:
        for trace in traces:
            subset2 = subset[subset['trace'] == trace]
            print(subset2.to_string())
            plt.plot(subset2['frames_log'], subset2['fault_rate_log'], marker='o', label=trace)
    
    second_level = "mmu" if traces_dep else "trace"
    drop_it = "trace" if traces_dep else "mmu"
    subset3 = subset.copy().set_index(keys=['frames', second_level], drop=True).sort_index().drop(columns=[drop_it])
    mean = subset3.groupby(level=['frames']).mean()
    mean['fault_rate_log'] = mean['fault_rate'].apply(lambda x: math.log(x, 2))
    print(mean.to_string())
    plt.plot(mean['frames_log'], mean['fault_rate_log'], marker='o', label='average')

    plt.title(f'Page Fault Rate vs. Number of Frames for {label}')
    plt.xlabel('Number of Frames (log2)')
    plt.ylabel('Page Fault Rate (log2)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'plots/fault_rate_vs_frames/fault_rate_vs_frames_{"traces" if traces_dep else "mmu"}_{label}.png')
    if show:
        plt.show()

def plot_thread_time(subset: pd.DataFrame, label: str, show: bool = False):
    traces = sorted(subset['trace'].unique())
    mmus = sorted(set(subset['mmu']))

    traces_dep = None

    if len(traces) == 1:
        traces_dep = True
    if len(mmus) == 1:
        traces_dep = False
    print(traces_dep, label)

    plt.figure(figsize=(10, 6))
    if traces_dep:
        for mmu in mmus:
            subset2: pd.DataFrame = subset[subset['mmu'] == mmu]
            print(subset2.to_string())
            plt.plot(subset2['frames_log'], subset2['time_sec'], marker='o', label=mmu)
    else:
        for trace in traces:
            subset2 = subset[subset['trace'] == trace]
            print(subset2.to_string())
            plt.plot(subset2['frames_log'], subset2['time_sec'], marker='o', label=trace)
    
    second_level = "mmu" if traces_dep else "trace"
    drop_it = "trace" if traces_dep else "mmu"
    subset3 = subset.copy().set_index(keys=['frames', second_level], drop=True).sort_index().drop(columns=[drop_it])
    mean = subset3.groupby(level=['frames']).mean()
    print(mean.to_string())
    plt.plot(mean['frames_log'], mean['time_sec'], marker='o', label='average')

    plt.title(f'System Cost vs. Number of Frames for {label}')
    plt.xlabel('Number of Frames (log2)')
    plt.ylabel('Time (sec)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'plots/time_vs_frames/time_vs_frames_{"traces" if traces_dep else "mmu"}_{label}.png')
    if show:
        plt.show()

for algo in df['mmu'].unique():
    subset = df[df['mmu'] == algo]
    plot_fault_rate(subset, label=algo)
    plot_thread_time(subset, label=algo)

for trace in sorted(df['trace'].unique()):
    subset = df[df['trace'] == trace]
    plot_fault_rate(subset, label=trace)
    plot_thread_time(subset, label=trace)