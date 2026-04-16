# models.py 
from datetime import datetime
from enum import Enum
from typing import Optional, List

class RoomStatus(Enum):
    """Room status enumeration"""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"

class BillStatus(Enum):
    """Bill status enumeration"""
    UNPAID = "unpaid"
    PAID = "paid"
    OVERDUE = "overdue"
    COLLECTED = "collected"

class Room:
    """Room class - demonstrates encapsulation"""
    _room_counter = 101
    
    def __init__(self, area: float, monthly_rent: float, deposit: float = 0):
        self.room_number = Room._room_counter
        Room._room_counter += 1
        self.area = area
        self.monthly_rent = monthly_rent
        self.deposit = deposit
        self._status = RoomStatus.AVAILABLE
        self._current_tenant_id: Optional[int] = None
    
    @property
    def status(self) -> RoomStatus:
        return self._status
    
    @property
    def current_tenant_id(self) -> Optional[int]:
        return self._current_tenant_id
    
    def rent_out(self, tenant_id: int) -> bool:
        """Rent out room to a tenant"""
        if self._status != RoomStatus.AVAILABLE:
            return False
        self._status = RoomStatus.OCCUPIED
        self._current_tenant_id = tenant_id
        return True
    
    def vacate(self) -> bool:
        """Vacate the room"""
        if self._status != RoomStatus.OCCUPIED:
            return False
        self._status = RoomStatus.AVAILABLE
        self._current_tenant_id = None
        return True
    
    def __str__(self):
        status_icon = {
            RoomStatus.AVAILABLE: "✅",
            RoomStatus.OCCUPIED: "👤",
            RoomStatus.MAINTENANCE: "🔧"
        }
        tenant_info = f" | Tenant: {self._current_tenant_id}" if self._current_tenant_id else ""
        return f"{status_icon[self._status]} Room {self.room_number} | {self.area}㎡ | ¥{self.monthly_rent}/month{tenant_info}"

class Tenant:
    """Tenant class"""
    _id_counter = 1000
    
    def __init__(self, name: str, phone: str, email: str):
        self.tenant_id = Tenant._id_counter
        Tenant._id_counter += 1
        self.name = name
        self.phone = phone
        self.email = email
    
    def __str__(self):
        return f"Tenant #{self.tenant_id}: {self.name} | {self.phone}"

class Bill:
    """Bill class - priority element for heap sorting"""
    _bill_counter = 5000
    
    def __init__(self, room_number: int, tenant_id: int, amount: float, due_date: str):
        """
        Initialize a bill
        :param room_number: Room number
        :param tenant_id: Tenant ID
        :param amount: Bill amount
        :param due_date: Due date in "YYYY-MM-DD" format (priority key for heap)
        """
        self.bill_id = Bill._bill_counter
        Bill._bill_counter += 1
        self.room_number = room_number
        self.tenant_id = tenant_id
        self.amount = amount
        self.due_date = due_date
        self.status = BillStatus.UNPAID
        self.collected_date: Optional[str] = None
    
    def mark_as_paid(self) -> bool:
        """Mark bill as paid"""
        if self.status == BillStatus.UNPAID or self.status == BillStatus.OVERDUE:
            self.status = BillStatus.PAID
            return True
        return False
    
    def mark_as_collected(self, collected_date: str = None) -> bool:
        """Mark bill as collected (called by greedy algorithm)"""
        if self.status == BillStatus.UNPAID or self.status == BillStatus.OVERDUE:
            self.status = BillStatus.COLLECTED
            self.collected_date = collected_date or datetime.now().strftime("%Y-%m-%d")
            return True
        return False
    
    def is_overdue(self, current_date: str = None) -> bool:
        """Check if bill is overdue"""
        if current_date is None:
            current_date = datetime.now().strftime("%Y-%m-%d")
        if self.status == BillStatus.UNPAID and self.due_date < current_date:
            self.status = BillStatus.OVERDUE
            return True
        return False
    
    def __lt__(self, other):
        """
        Override less-than operator for heap comparison
        Earlier due_date = higher priority
        """
        return self.due_date < other.due_date
    
    def __str__(self):
        status_icon = {
            BillStatus.UNPAID: "⏳",
            BillStatus.PAID: "✅",
            BillStatus.OVERDUE: "⚠️",
            BillStatus.COLLECTED: "📞"
        }
        return f"{status_icon[self.status]} Bill #{self.bill_id} | Room {self.room_number} | ¥{self.amount} | Due: {self.due_date}"
