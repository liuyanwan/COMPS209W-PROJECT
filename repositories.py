# repositories.py 
from typing import List, Optional, Dict
from models import Room, Tenant, Bill, BillStatus

class RoomRepository:
    """Room data repository"""
    
    def __init__(self):
        self._rooms: Dict[int, Room] = {}
    
    def add(self, room: Room) -> Room:
        self._rooms[room.room_number] = room
        return room
    
    def get(self, room_number: int) -> Optional[Room]:
        return self._rooms.get(room_number)
    
    def get_all(self) -> List[Room]:
        return list(self._rooms.values())
    
    def get_occupied_rooms(self) -> List[Room]:
        return [r for r in self._rooms.values() if r.status.value == "occupied"]
    
    def get_available_rooms(self) -> List[Room]:
        return [r for r in self._rooms.values() if r.status.value == "available"]
    
    def update(self, room: Room) -> bool:
        if room.room_number in self._rooms:
            self._rooms[room.room_number] = room
            return True
        return False
    
    def delete(self, room_number: int) -> bool:
        if room_number in self._rooms:
            del self._rooms[room_number]
            return True
        return False
    
    def clear(self):
        self._rooms.clear()

class TenantRepository:
    """Tenant data repository"""
    
    def __init__(self):
        self._tenants: Dict[int, Tenant] = {}
    
    def add(self, tenant: Tenant) -> Tenant:
        self._tenants[tenant.tenant_id] = tenant
        return tenant
    
    def get(self, tenant_id: int) -> Optional[Tenant]:
        return self._tenants.get(tenant_id)
    
    def get_all(self) -> List[Tenant]:
        return list(self._tenants.values())
    
    def find_by_name(self, name: str) -> List[Tenant]:
        return [t for t in self._tenants.values() if name.lower() in t.name.lower()]
    
    def update(self, tenant: Tenant) -> bool:
        if tenant.tenant_id in self._tenants:
            self._tenants[tenant.tenant_id] = tenant
            return True
        return False
    
    def delete(self, tenant_id: int) -> bool:
        if tenant_id in self._tenants:
            del self._tenants[tenant_id]
            return True
        return False
    
    def clear(self):
        self._tenants.clear()

class BillRepository:
    """Bill data repository"""
    
    def __init__(self):
        self._bills: Dict[int, Bill] = {}
    
    def add(self, bill: Bill) -> Bill:
        self._bills[bill.bill_id] = bill
        return bill
    
    def add_batch(self, bills: List[Bill]) -> List[Bill]:
        for bill in bills:
            self._bills[bill.bill_id] = bill
        return bills
    
    def get(self, bill_id: int) -> Optional[Bill]:
        return self._bills.get(bill_id)
    
    def get_all(self) -> List[Bill]:
        return list(self._bills.values())
    
    def get_by_room(self, room_number: int) -> List[Bill]:
        return [b for b in self._bills.values() if b.room_number == room_number]
    
    def get_by_tenant(self, tenant_id: int) -> List[Bill]:
        return [b for b in self._bills.values() if b.tenant_id == tenant_id]
    
    def get_unpaid_bills(self) -> List[Bill]:
        """Get all unpaid bills (including overdue)"""
        return [b for b in self._bills.values() 
                if b.status in [BillStatus.UNPAID, BillStatus.OVERDUE]]
    
    def get_overdue_bills(self, current_date: str = None) -> List[Bill]:
        """Get overdue bills"""
        from datetime import datetime
        if current_date is None:
            current_date = datetime.now().strftime("%Y-%m-%d")
        
        overdue = []
        for bill in self._bills.values():
            if bill.status in [BillStatus.UNPAID, BillStatus.OVERDUE]:
                if bill.due_date < current_date:
                    bill.status = BillStatus.OVERDUE
                    overdue.append(bill)
        return overdue
    
    def update(self, bill: Bill) -> bool:
        if bill.bill_id in self._bills:
            self._bills[bill.bill_id] = bill
            return True
        return False
    
    def delete(self, bill_id: int) -> bool:
        if bill_id in self._bills:
            del self._bills[bill_id]
            return True
        return False
    
    def clear(self):
        self._bills.clear()
