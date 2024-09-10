from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        self.frames = frames
        self.memory = []  # Represents frames in memory
        self.use_bits = []  # Represents use bits for each page in memory
        self.dirty_bits = []  # Tracks whether each page in memory is dirty
        self.clock_hand = 0  # Points to the current position of the clock hand
        self.page_table = {}  # Maps page number to frame index in memory
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
            # Page is already in memory, set use bit to 1
            frame_index = self.page_table[page_number]
            self.use_bits[frame_index] = 1
            if self.debug_mode:
                print(f"Page {page_number} read from memory.")
        else:
            # Page fault occurs
            self.page_faults += 1
            self._handle_page_fault(page_number, dirty=False)

    def write_memory(self, page_number):
        if page_number in self.page_table:
            # Page is already in memory, set use bit to 1 and mark as dirty
            frame_index = self.page_table[page_number]
            self.use_bits[frame_index] = 1
            self.dirty_bits[frame_index] = True  # Mark page as dirty
            if self.debug_mode:
                print(f"Page {page_number} written to memory.")
        else:
            # Page fault occurs
            self.page_faults += 1
            self._handle_page_fault(page_number, dirty=True)

    def _handle_page_fault(self, page_number, dirty):
        if len(self.memory) < self.frames:
            # There is still space in memory
            self.memory.append(page_number)
            self.use_bits.append(1)  # Set use bit to 1 for new page
            self.dirty_bits.append(dirty)  # Mark as dirty if it was a write
            self.page_table[page_number] = len(self.memory) - 1
        else:
            # No space, we need to find a page to replace using the Clock algorithm
            while True:
                if self.use_bits[self.clock_hand] == 0:
                    # Found a page to replace
                    replaced_page = self.memory[self.clock_hand]

                    # Check if the replaced page is dirty, if so increment disk writes
                    if self.dirty_bits[self.clock_hand]:
                        self.disk_writes += 1
                        if self.debug_mode:
                            print(f"Writing dirty page {replaced_page} to disk.")

                    # Replace the page in memory
                    self.memory[self.clock_hand] = page_number
                    self.page_table[page_number] = self.clock_hand
                    del self.page_table[replaced_page]
                    self.use_bits[self.clock_hand] = 1  # Set use bit to 1 for new page
                    self.dirty_bits[self.clock_hand] = dirty  # Mark as dirty if it's a write

                    if self.debug_mode:
                        print(f"Page fault: loaded page {page_number} into frame {self.clock_hand}, replaced page {replaced_page}")
                    
                    # Move clock hand forward
                    self.clock_hand = (self.clock_hand + 1) % self.frames
                    break
                else:
                    # Clear the use bit and move the clock hand
                    self.use_bits[self.clock_hand] = 0
                    self.clock_hand = (self.clock_hand + 1) % self.frames

        # Increment disk reads as we load the new page into memory
        self.disk_reads += 1
        if self.debug_mode:
            print(f"Reading page {page_number} from disk.")

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
