# heap.py 
from typing import List, Optional, Any

class MinHeap:
    """
    Min-Heap (Priority Queue) Implementation
    
    Heap Invariant:
    For any node parent and its child:
        due_date(parent) <= due_date(child)
    
    Complexity:
    - insert: O(log n)
    - peek: O(1)
    - extract_min: O(log n)
    - build_heap: O(n)
    """
    
    def __init__(self):
        """Initialize an empty heap"""
        self._heap: List[Any] = []
    
    def insert(self, item: Any) -> None:
        """Insert element into heap - O(log n)"""
        self._heap.append(item)
        self._heapify_up(len(self._heap) - 1)
    
    def peek(self) -> Optional[Any]:
        """View minimum element without removing - O(1)"""
        if self.is_empty():
            return None
        return self._heap[0]
    
    def extract_min(self) -> Optional[Any]:
        """Remove and return minimum element - O(log n)"""
        if self.is_empty():
            return None
        
        min_item = self._heap[0]
        last_item = self._heap.pop()
        
        if not self.is_empty():
            self._heap[0] = last_item
            self._heapify_down(0)
        
        return min_item
    
    def is_empty(self) -> bool:
        """Check if heap is empty"""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Return number of elements in heap"""
        return len(self._heap)
    
    def build_heap(self, items: List[Any]) -> None:
        """Build heap from list efficiently - O(n) (Floyd's algorithm)"""
        self._heap = items.copy()
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self._heapify_down(i)
    
    def _heapify_up(self, index: int) -> None:
        """Bubble up to maintain heap invariant"""
        if index <= 0:
            return
        
        parent_index = (index - 1) // 2
        
        if self._heap[index] < self._heap[parent_index]:
            self._heap[index], self._heap[parent_index] = self._heap[parent_index], self._heap[index]
            self._heapify_up(parent_index)
    
    def _heapify_down(self, index: int) -> None:
        """Bubble down to maintain heap invariant"""
        left_idx = 2 * index + 1
        right_idx = 2 * index + 2
        smallest = index
        
        if left_idx < len(self._heap) and self._heap[left_idx] < self._heap[smallest]:
            smallest = left_idx
        
        if right_idx < len(self._heap) and self._heap[right_idx] < self._heap[smallest]:
            smallest = right_idx
        
        if smallest != index:
            self._heap[index], self._heap[smallest] = self._heap[smallest], self._heap[index]
            self._heapify_down(smallest)
    
    def get_all(self) -> List[Any]:
        """Get all elements (order not guaranteed)"""
        return self._heap.copy()
    
    def __str__(self) -> str:
        if self.is_empty():
            return "MinHeap: empty"
        
        result = ["MinHeap contents:"]
        for i, item in enumerate(self._heap):
            if hasattr(item, 'due_date'):
                result.append(f"  [{i}] Bill #{item.bill_id} - due: {item.due_date}")
            else:
                result.append(f"  [{i}] {item}")
        return "\n".join(result)


# Unit test
if __name__ == "__main__":
    from models import Bill
    
    print("=" * 50)
    print("Min-Heap Unit Test")
    print("=" * 50)
    
    heap = MinHeap()
    
    bills = [
        Bill(101, 1000, 2500, "2026-03-15"),
        Bill(102, 1001, 3200, "2026-02-10"),
        Bill(103, 1002, 1800, "2026-04-01"),
        Bill(101, 1000, 2500, "2026-01-20"),
    ]
    
    print("\n1. Testing insert():")
    for bill in bills:
        heap.insert(bill)
        print(f"   Inserted: Room {bill.room_number} | Due {bill.due_date}")
    
    print(f"\n2. Testing peek(): {heap.peek().due_date}")
    
    print("\n3. Testing extract_min() (ordered by due date):")
    while not heap.is_empty():
        bill = heap.extract_min()
        print(f"   Extracted: Room {bill.room_number} | Due {bill.due_date}")
    
    print("\n4. Testing build_heap():")
    heap.build_heap(bills)
    print(f"   Heap size: {heap.size()}")
    print(f"   Peek (earliest due): {heap.peek().due_date}")
