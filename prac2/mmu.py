'''
* Interface for Memory Management Unit.
* The memory management unit should maintain the concept of a page table.
* As pages are read and written to, this changes the pages loaded into the
* the limited number of frames. The MMU keeps records, which will be used
* to analyse the performance of different replacement strategies implemented
* for the MMU.
*
'''
class MMU:
    def read_memory(self, page_number):
        pass

    def write_memory(self, page_number):
        pass

    def set_debug(self):
        pass

    def reset_debug(self):
        pass

    def get_total_disk_reads(self):
        return -1

    def get_total_disk_writes(self):
        return -1

    def get_total_page_faults(self):
        return -1
