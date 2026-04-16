# services.py 
from datetime import datetime
from typing import List, Optional, Tuple
from models import Bill, BillStatus
from repositories import RoomRepository, TenantRepository, BillRepository
from heap import MinHeap


class BillingService:
    """
    Billing Service - Contains bill generation and Greedy Collection Algorithm
    
    Greedy Collection Algorithm:
    - Problem: Select earliest due bills for collection
    - Strategy: Always take heap top (earliest due)
    - Complexity: O(n + k log n)
    """
    
    def __init__(self, room_repo: RoomRepository, tenant_repo: TenantRepository, bill_repo: BillRepository):
        self.room_repo = room_repo
        self.tenant_repo = tenant_repo
        self.bill_repo = bill_repo
    
    def generate_monthly_bills(self, year: int, month: int) -> int:
        """Generate monthly bills for all occupied rooms"""
        generated_count = 0
        occupied_rooms = self.room_repo.get_occupied_rooms()
        
        # Due date: 15th of next month
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        due_date = f"{next_year}-{next_month:02d}-15"
        
        for room in occupied_rooms:
            tenant_id = room.current_tenant_id
            if tenant_id:
                # Check if bill already exists
                existing = self.bill_repo.get_by_room(room.room_number)
                already_exists = any(b.due_date == due_date for b in existing)
                
                if not already_exists:
                    bill = Bill(room.room_number, tenant_id, room.monthly_rent, due_date)
                    self.bill_repo.add(bill)
                    generated_count += 1
                    print(f"📋 Generated: Room {room.room_number} | ¥{room.monthly_rent} | Due {due_date}")
        
        print(f"✅ Generated {generated_count} bills")
        return generated_count
    
    def pay_bill(self, bill_id: int) -> bool:
        """Pay a bill"""
        bill = self.bill_repo.get(bill_id)
        if not bill:
            print(f"❌ Bill {bill_id} not found")
            return False
        
        if bill.mark_as_paid():
            print(f"💰 Bill #{bill_id} paid ¥{bill.amount}")
            return True
        else:
            print(f"⚠️ Bill #{bill_id} status: {bill.status.value}")
            return False
    
    def get_unpaid_bills(self) -> List[Bill]:
        """Get all unpaid bills"""
        return self.bill_repo.get_unpaid_bills()
    
    def get_overdue_bills(self) -> List[Bill]:
        """Get overdue bills"""
        return self.bill_repo.get_overdue_bills()
    
    # ========== Greedy Collection Algorithm ==========
    
    def greedy_collection(self, limit: int = 10, current_date: str = None) -> Tuple[List[Bill], int]:
        """
        Greedy Collection Algorithm
        
        Steps:
        1. Get all unpaid bills
        2. Build min-heap (O(n))
        3. Extract min k times (O(k log n))
        4. Mark each as collected
        
        Complexity: O(n + k log n)
        """
        if current_date is None:
            current_date = datetime.now().strftime("%Y-%m-%d")
        
        pending_bills = self.bill_repo.get_unpaid_bills()
        
        if not pending_bills:
            print("📭 No unpaid bills to collect")
            return [], 0
        
        print(f"\n📋 Greedy Collection Started")
        print(f"   Pending: {len(pending_bills)} | Limit: {limit}")
        
        # Build heap - O(n)
        heap = MinHeap()
        heap.build_heap(pending_bills)
        
        print(f"   Earliest due: {heap.peek().due_date}")
        
        # Greedy extraction - O(k log n)
        collected_bills = []
        k = min(limit, heap.size())
        
        for i in range(k):
            bill = heap.extract_min()
            if bill:
                bill.mark_as_collected(current_date)
                self.bill_repo.update(bill)
                collected_bills.append(bill)
                print(f"   [{i+1}] 📞 Collected: Room {bill.room_number} | ¥{bill.amount} | Due {bill.due_date}")
        
        print(f"✅ Collected {len(collected_bills)} bills")
        return collected_bills, len(collected_bills)
    
    def greedy_collection_demo(self, limit: int = 5) -> None:
        """Demonstrate greedy collection algorithm"""
        print("\n" + "=" * 60)
        print("Greedy Collection Algorithm - Demonstration")
        print("=" * 60)
        print("\nProblem: Select earliest due bills for collection")
        print("Strategy: Always pick heap top (earliest due)")
        print("Heap role: Find global earliest due (O(log n))")
        print("=" * 60)
        
        # Demo data
        demo_bills = [
            Bill(101, 1000, 2500, "2026-01-15"),
            Bill(102, 1001, 3200, "2026-02-10"),
            Bill(103, 1002, 1800, "2026-03-01"),
            Bill(101, 1000, 2500, "2026-01-20"),
            Bill(102, 1001, 3200, "2026-02-25"),
            Bill(104, 1003, 4500, "2026-01-05"),
        ]
        
        print("\nDemo Bills:")
        for bill in demo_bills:
            print(f"  Bill #{bill.bill_id}: Room {bill.room_number} | ¥{bill.amount} | Due {bill.due_date}")
        
        heap = MinHeap()
        heap.build_heap(demo_bills)
        
        print(f"\nHeap Peek (Earliest Due): {heap.peek().due_date}")
        print("\nGreedy Process:")
        
        for i in range(min(limit, len(demo_bills))):
            bill = heap.extract_min()
            print(f"  Step {i+1}: Select Bill #{bill.bill_id} (Due {bill.due_date})")
            if not heap.is_empty():
                print(f"          Next candidate: Due {heap.peek().due_date}")
        
        print("\n" + "=" * 60)
    
    def get_bill_summary(self) -> dict:
        """Get bill summary statistics"""
        all_bills = self.bill_repo.get_all()
        unpaid = self.bill_repo.get_unpaid_bills()
        overdue = self.get_overdue_bills()
        collected = [b for b in all_bills if b.status == BillStatus.COLLECTED]
        paid = [b for b in all_bills if b.status == BillStatus.PAID]
        
        return {
            "total_bills": len(all_bills),
            "paid": len(paid),
            "unpaid": len(unpaid),
            "overdue": len(overdue),
            "collected": len(collected),
            "total_unpaid_amount": sum(b.amount for b in unpaid),
            "total_overdue_amount": sum(b.amount for b in overdue),
            "paid_amount": sum(b.amount for b in paid)
        }
    
    def print_bill_summary(self):
        """Print bill summary"""
        s = self.get_bill_summary()
        print("\n" + "=" * 50)
        print("📊 Bill Summary")
        print("=" * 50)
        print(f"Total Bills: {s['total_bills']}")
        print(f"Paid: {s['paid']}")
        print(f"Unpaid: {s['unpaid']}")
        print(f"Overdue: {s['overdue']}")
        print(f"Collected: {s['collected']}")
        print(f"Unpaid Amount: ¥{s['total_unpaid_amount']}")
        print(f"Overdue Amount: ¥{s['total_overdue_amount']}")
        print(f"Collected Amount: ¥{s['paid_amount']}")
        print("=" * 50)
