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

    plt.title(f'Page Fault Rate vs. Number of Frames for {label}')
    plt.xlabel('Number of Frames (log2)')
    plt.ylabel('Page Fault Rate (log2)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'plots/fault_rate_vs_frames/fault_rate_vs_frames_{"traces" if traces_dep else "mmu"}_{label}.png')
    if show:
        plt.show()

def plot_disk_accesses(subset: pd.DataFrame, label: str, show: bool = False):
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
            plt.plot(subset2['frames_log'], subset2['disk_accesses_log'], marker='o', label=mmu)
    else:
        for trace in traces:
            subset2 = subset[subset['trace'] == trace]
            print(subset2.to_string())
            plt.plot(subset2['frames_log'], subset2['disk_accesses_log'], marker='o', label=trace)

    plt.title(f'Disk Accesses (Reads + Writes) vs. Number of Frames for {label}')
    plt.xlabel('Number of Frames (log2)')
    plt.ylabel('Disk Accesses (Reads + Writes) (log10)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'plots/disk_accesses_vs_frames/disk_accesses_vs_frames_{"traces" if traces_dep else "mmu"}_{label}.png')
    if show:
        plt.show()

for algo in df['mmu'].unique():
    subset = df[df['mmu'] == algo]
    plot_fault_rate(subset, label=algo)
    plot_disk_accesses(subset, label=algo)

for trace in sorted(df['trace'].unique()):
    subset = df[df['trace'] == trace]
    plot_fault_rate(subset, label=trace)
    plot_disk_accesses(subset, label=trace)