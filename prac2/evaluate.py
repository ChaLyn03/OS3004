from mmu import MMU
from clockmmu import ClockMMU
from lrummu import LruMMU
from randmmu import RandMMU

import sys
import os
import psutil  # To track memory usage
from enum import Enum
from dataclasses import dataclass
from functools import cache

mmu_labels = [
    (ClockMMU, "clock"),
    (LruMMU, "lru"),
    (RandMMU, "rand"),
    (MMU, "undefined")
]

@cache
def name_of_mmu(mmu):
    for (mmu_type, label) in mmu_labels:
        if isinstance(mmu, mmu_type):
            return label
    return None

class TraceFile(str, Enum):
    BZIP = "bzip"
    GCC = "gcc"
    SAMPLE = "sample"
    SIXPACK = "sixpack"
    SWIM = "swim"

class ReplacementMMU(MMU, Enum):
    rand = RandMMU
    lru = LruMMU
    clock = ClockMMU

class DebugMode(int, Enum):
    DEBUG = True
    QUIET = False

PAGE_OFFSET = 12  # page is 2^12 = 4KB

@dataclass
class SimulationParameters:
    trace_file: TraceFile
    frames: int
    replacement_mode: ReplacementMMU
    debug_mode: DebugMode

@dataclass
class SimulationFactory:
    trace_files: list[TraceFile]
    frames_range: list[int]
    replacement_modes: list[ReplacementMMU]
    debug_modes: list[DebugMode]

    def enumerate(self):
        for file in self.trace_files:
            for mmu in self.replacement_modes:
                for frames in self.frames_range:
                    for debug in self.debug_modes:
                        yield SimulationParameters(
                            file,
                            frames,
                            mmu,
                            debug
                        )

def get_memory_usage():
    """Get current memory usage of the process in KB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss // 1024  # in KB

def simulate(sim: SimulationParameters):
    filename = f"{sim.trace_file.value}.trace"
    try:
        with open(filename, 'r') as file:
            # Read the trace file contents
            trace_contents = file.readlines()
    except FileNotFoundError:
        print(f"Input '{filename}' could not be found")
        return
    
    frames = sim.frames
    mmu = sim.replacement_mode.value(frames)
    no_events = 0
    peak_memory = get_memory_usage()  # Initialize peak memory tracking

    for trace_line in trace_contents:
        trace_cmd = trace_line.strip().split(" ")
        logical_address = int(trace_cmd[0], 16)
        page_number = logical_address >> PAGE_OFFSET

        # Process read or write
        if trace_cmd[1] == "R":
            mmu.read_memory(page_number)
        elif trace_cmd[1] == "W":
            mmu.write_memory(page_number)
        else:
            print(f"Badly formatted file. Error on line {no_events + 1}")
            return

        # Track peak memory usage after each memory operation
        current_memory = get_memory_usage()
        if current_memory > peak_memory:
            peak_memory = current_memory

        no_events += 1

    fault_rate = mmu.get_total_page_faults() / no_events
    print(f"{filename:<14}|{name_of_mmu(mmu):<8}|{frames: 8d}|{no_events: 8d}|{mmu.get_total_disk_reads(): 7d} reads|{mmu.get_total_disk_writes(): 7d}|{fault_rate: .3%}|{peak_memory: 6d} KB used (peak)")
    
    return f"{filename},{name_of_mmu(mmu)},{frames},{no_events},{mmu.get_total_disk_reads()},{mmu.get_total_disk_writes()},{fault_rate},{peak_memory}\r\n"

def main():
    frame_list = [2,4,8,16,32]  # Add 16 and 32 frames to the simulation

    factory = SimulationFactory(
        [x for x in TraceFile],
        frame_list,
        [x for x in ReplacementMMU],
        [DebugMode.QUIET]
    )

    with open("output.csv", "w") as outfile:
        outfile.write("trace,mmu,frames,no_events,reads,writes,fault_rate,peak_memory_kb\r\n")
        for sim_params in factory.enumerate():
            outfile.write(simulate(sim_params))

if __name__ == "__main__":
    main()
