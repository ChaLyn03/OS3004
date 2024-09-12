import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('output.csv')

# Display the first few rows of the dataframe
print(df.head())

# Assuming the CSV file has columns like 'mmu', 'trace', 'frames', 'fault_rate', 'reads', and 'writes'

# Plot 1: Page Fault Rate vs. Number of Frames for each algorithm
plt.figure(figsize=(10, 6))
for algo in df['mmu'].unique():
    subset = df[df['mmu'] == algo]
    plt.plot(subset['frames'], subset['fault_rate'], marker='o', label=algo)

plt.title('Page Fault Rate vs. Number of Frames for Different Algorithms')
plt.xlabel('Number of Frames')
plt.ylabel('Page Fault Rate')
plt.legend()
plt.grid(True)
plt.savefig('fault_rate_vs_frames.png')
plt.show()

# Plot 2: Disk Accesses (Reads and Writes) vs. Number of Frames for each algorithm
plt.figure(figsize=(10, 6))
for algo in df['mmu'].unique():
    subset = df[df['mmu'] == algo]
    plt.plot(subset['frames'], subset['reads'] + subset['writes'], marker='o', label=algo)

plt.title('Disk Accesses (Reads + Writes) vs. Number of Frames for Different Algorithms')
plt.xlabel('Number of Frames')
plt.ylabel('Disk Accesses (Reads + Writes)')
plt.legend()
plt.grid(True)
plt.savefig('disk_accesses_vs_frames.png')
plt.show()

# Plot 3: Comparison of Page Fault Rate for each trace
plt.figure(figsize=(10, 6))
for trace in df['trace'].unique():
    subset = df[df['trace'] == trace]
    plt.plot(subset['frames'], subset['fault_rate'], marker='o', label=trace)

plt.title('Page Fault Rate vs. Number of Frames for Different Traces')
plt.xlabel('Number of Frames')
plt.ylabel('Page Fault Rate')
plt.legend()
plt.grid(True)
plt.savefig('fault_rate_vs_traces.png')
plt.show()

# Plot 4: Comparison of Disk Accesses (Reads + Writes) for each trace
plt.figure(figsize=(10, 6))
for trace in df['trace'].unique():
    subset = df[df['trace'] == trace]
    plt.plot(subset['frames'], subset['reads'] + subset['writes'], marker='o', label=trace)

plt.title('Disk Accesses (Reads + Writes) vs. Number of Frames for Different Traces')
plt.xlabel('Number of Frames')
plt.ylabel('Disk Accesses (Reads + Writes)')
plt.legend()
plt.grid(True)
plt.savefig('disk_accesses_vs_traces.png')
plt.show()
