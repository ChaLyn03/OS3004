from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}  # Maps page number to its status ('R' for read, 'W' for written)
        self.memory = []  # Represents frames in memory
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False

    def read_memory(self, page_number):
        if page_number in self.page_table:
            # Page is already in memory, no action needed
            if self.debug_mode:
                print(f"Page {page_number} read from memory.")
        else:
            # Page fault occurs
            self.page_faults += 1
            self._handle_page_fault(page_number, mode='R')

    def write_memory(self, page_number):
        if page_number in self.page_table:
            # Page is already in memory, mark as modified
            if self.debug_mode:
                print(f"Page {page_number} written to memory.")
            self.page_table[page_number] = 'W'  # Update page status to 'W'
        else:
            # Page fault occurs
            self.page_faults += 1
            self._handle_page_fault(page_number, mode='W')

    def _handle_page_fault(self, page_number, mode):
        if len(self.memory) < self.frames:
            # There is still space in memory
            self.memory.append(page_number)
            self.page_table[page_number] = mode  # Set page mode ('R' or 'W')
            replace_index = len(self.memory) - 1
        else:
            # No space, we need to replace a random page
            replace_index = random.randint(0, self.frames - 1)
            replaced_page = self.memory[replace_index]

            # If the replaced page was written to, we need to increment disk writes
            if self.page_table[replaced_page] == 'W':
                self.disk_writes += 1

            # Replace the page in memory
            self.memory[replace_index] = page_number
            del self.page_table[replaced_page]
            self.page_table[page_number] = mode  # Set page mode ('R' or 'W')

        # Increment disk reads as we load the new page into memory
        self.disk_reads += 1

        if self.debug_mode:
            print(f"Page fault: loaded page {page_number} into frame {replace_index}")

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
