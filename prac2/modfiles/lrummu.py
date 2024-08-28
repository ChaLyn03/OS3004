from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.page_table = OrderedDict()  # Keeps pages in the order of usage
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
            # Page is already in memory, move it to the end to mark as recently used
            self.page_table.move_to_end(page_number)
            if self.debug_mode:
                print(f"Page {page_number} read from memory.")
        else:
            # Page fault occurs
            self.page_faults += 1
            self._handle_page_fault(page_number, mode='R')

    def write_memory(self, page_number):
        if page_number in self.page_table:
            # Page is already in memory, mark as modified and recently used
            self.page_table.move_to_end(page_number)
            if self.debug_mode:
                print(f"Page {page_number} written to memory.")
            self.page_table[page_number] = 'W'
        else:
            # Page fault occurs
            self.page_faults += 1
            self._handle_page_fault(page_number, mode='W')

    def _handle_page_fault(self, page_number, mode):
        if len(self.memory) < self.frames:
            # There is still space in memory
            self.memory.append(page_number)
            self.page_table[page_number] = mode
        else:
            # No space, we need to replace the least recently used page
            lru_page, lru_mode = self.page_table.popitem(last=False)  # Removes and returns the LRU page
            self.memory.remove(lru_page)

            # If the replaced page was written to, we need to increment disk writes
            if lru_mode == 'W':
                self.disk_writes += 1

            # Replace the page in memory
            self.memory.append(page_number)
            self.page_table[page_number] = mode

            if self.debug_mode:
                print(f"Page fault: loaded page {page_number} into memory, replaced LRU page {lru_page}")

        # Increment disk reads as we load the new page into memory
        self.disk_reads += 1

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
