# custom Queue class and sort

class PathQueue:
    """
    Queue used to follow previously taken path
    """
    def __init__(self):
        self._queue = []
        
    def enqueue(self, value) -> None:
        self._queue.append(value)
        
    def dequeue(self):
        """
        returns first item in the queue
        and reinserts to the back of the queue
        """
        if len(self._queue) > 0:
            item = self._queue.pop(0)
            self.enqueue(item)
        else:
            raise IndexError("Path is Empty")
        return item
        
    def is_empty(self) -> bool:
        if len(self._queue) == 0:
            return True
        else:
            return False
        
    def clear_queue(self) -> None:
        self._queue.clear()

class MergeSort:  
    """
    handles sorting a list with merge sort 
    """
    
    def __init__(self, arr):
        self.arr = arr
      
    def _merge(self, l, m, r):

        # Copy data to temp array
        left = self.arr[l:m+1]
        right = self.arr[m+1: r+1]
    
        i = 0     # index of first subarray
        j = 0     # index of second subarray
        k = l     # index of merged subarray in arr
    
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                self.arr[k] = left[i]
                i += 1
            else:
                self.arr[k] = right[j]
                j += 1
            k += 1
    
        # remaining elements of left
        while i < len(left):
            self.arr[k] = left[i]
            i += 1
            k += 1
    
        # remaining elements of right
        while j < len(right):
            self.arr[k] = right[j]
            j += 1
            k += 1
   
    # since list instance variable is mutated during the sort returning is not required    
    def sort(self, l,r):
        """
        merge sort array starting from l ending on r
        """
        if not l<r:
            return

        m = l+(r-l)//2

        # Sort first and second halves of the l -> r slice then merge
        self.sort(l, m)
        self.sort(m+1, r)
        self._merge(l, m, r)

