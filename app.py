# app.py - Command-line application entry point
from models import Room, Tenant
from repositories import RoomRepository, TenantRepository, BillRepository
from services import BillingService


class ApartmentApp:
    """Apartment Management Application"""
    
    def __init__(self):
        # Initialize repositories
        self.room_repo = RoomRepository()
        self.tenant_repo = TenantRepository()
        self.bill_repo = BillRepository()
        
        # Initialize service
        self.billing_service = BillingService(
            self.room_repo, 
            self.tenant_repo, 
            self.bill_repo
        )
        
        # Create demo data
        self._create_demo_data()
    
    def _create_demo_data(self):
        """Create demo data"""
        print("\n📝 Creating demo data...")
        
        # Add rooms
        rooms = [
            Room(45.0, 2500, 5000),
            Room(60.0, 3200, 6000),
            Room(35.0, 1800, 3600),
            Room(80.0, 4500, 9000),
        ]
        for room in rooms:
            self.room_repo.add(room)
        
        # Add tenants
        tenants = [
            Tenant("AAA", "67340002", "AAA@email.com"),
            Tenant("BBB", "67340002", "BBB@email.com"),
            Tenant("CCC", "67340002", "CCC@email.com"),
        ]
        for tenant in tenants:
            self.tenant_repo.add(tenant)
        
        # Rent out rooms
        self.room_repo.get(101).rent_out(1000)
        self.room_repo.get(102).rent_out(1001)
        
        # Generate historical bills
        demo_bills = [
            Bill(101, 1000, 2500, "2026-01-15"),
            Bill(101, 1000, 2500, "2026-02-15"),
            Bill(102, 1001, 3200, "2026-01-10"),
            Bill(102, 1001, 3200, "2026-02-10"),
            Bill(103, 1002, 1800, "2026-01-20"),
            Bill(101, 1000, 2500, "2026-03-15"),
            Bill(102, 1001, 3200, "2026-03-10"),
        ]
        
        for bill in demo_bills:
            if bill.due_date < "2024-02-01":
                bill.mark_as_paid()
            self.bill_repo.add(bill)
        
        print(f"✅ Demo data created: {len(self.room_repo.get_all())} rooms, "
              f"{len(self.tenant_repo.get_all())} tenants, "
              f"{len(self.bill_repo.get_all())} bills")
    
    def _show_menu(self):
        """Display menu"""
        print("\n" + "=" * 55)
        print("🏢 Apartment Management System")
        print("=" * 55)
        print("\n📋 Room & Tenant Management:")
        print("  1. Add Room")
        print("  2. List All Rooms")
        print("  3. Add Tenant")
        print("  4. List All Tenants")
        print("  5. Rent Room")
        print("  6. Vacate Room")
        print("\n💰 Bill Management:")
        print("  7. Generate Monthly Bills")
        print("  8. List All Bills")
        print("  9. Pay Bill")
        print(" 10. View Unpaid Bills")
        print("\n🤖 Algorithm Demo (Task 2):")
        print(" 11. 🎯 Greedy Collection Algorithm")
        print(" 12. 🏗️  Min-Heap Data Structure Demo")
        print(" 13. 📖 Greedy Algorithm Explanation")
        print("\n📊 Statistics & Exit:")
        print(" 14. View Bill Statistics")
        print(" 15. Save & Exit")
        print("=" * 55)
    
    def _add_room(self):
        """Add a room"""
        try:
            area = float(input("Area (sqm): "))
            rent = float(input("Monthly rent: "))
            deposit = float(input("Deposit: "))
            self.room_repo.add(Room(area, rent, deposit))
            print("✅ Room added")
        except ValueError:
            print("❌ Invalid input")
    
    def _list_rooms(self):
        """List all rooms"""
        rooms = self.room_repo.get_all()
        if not rooms:
            print("No rooms found")
            return
        
        print("\n" + "=" * 50)
        print("Room List")
        print("=" * 50)
        for room in rooms:
            print(f"  {room}")
        print("=" * 50)
    
    def _add_tenant(self):
        """Add a tenant"""
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        self.tenant_repo.add(Tenant(name, phone, email))
        print("✅ Tenant added")
    
    def _list_tenants(self):
        """List all tenants"""
        tenants = self.tenant_repo.get_all()
        if not tenants:
            print("No tenants found")
            return
        
        print("\n" + "=" * 50)
        print("Tenant List")
        print("=" * 50)
        for tenant in tenants:
            print(f"  {tenant}")
        print("=" * 50)
    
    def _rent_room(self):
        """Rent a room to a tenant"""
        try:
            room_num = int(input("Room number: "))
            tenant_id = int(input("Tenant ID: "))
            
            room = self.room_repo.get(room_num)
            tenant = self.tenant_repo.get(tenant_id)
            
            if not room:
                print(f"❌ Room {room_num} not found")
                return
            if not tenant:
                print(f"❌ Tenant {tenant_id} not found")
                return
            
            if room.rent_out(tenant_id):
                print(f"✅ Room {room_num} rented to {tenant.name}")
            else:
                print(f"❌ Room {room_num} is not available")
        except ValueError:
            print("❌ Invalid input")
    
    def _vacate_room(self):
        """Vacate a room"""
        try:
            room_num = int(input("Room number: "))
            room = self.room_repo.get(room_num)
            
            if not room:
                print(f"❌ Room {room_num} not found")
                return
            
            # Check for unpaid bills
            unpaid = self.bill_repo.get_unpaid_bills()
            room_unpaid = [b for b in unpaid if b.room_number == room_num]
            
            if room_unpaid:
                print(f"⚠️ Room {room_num} has {len(room_unpaid)} unpaid bills")
                return
            
            if room.vacate():
                print(f"✅ Room {room_num} vacated")
            else:
                print(f"❌ Room {room_num} is not occupied")
        except ValueError:
            print("❌ Invalid input")
    
    def _generate_bills(self):
        """Generate monthly bills"""
        try:
            year = int(input("Year: "))
            month = int(input("Month (1-12): "))
            self.billing_service.generate_monthly_bills(year, month)
        except ValueError:
            print("❌ Invalid input")
    
    def _list_bills(self):
        """List all bills"""
        bills = self.bill_repo.get_all()
        if not bills:
            print("No bills found")
            return
        
        print("\n" + "=" * 60)
        print("All Bills")
        print("=" * 60)
        for bill in bills:
            print(f"  {bill}")
        print("=" * 60)
    
    def _pay_bill(self):
        """Pay a bill"""
        try:
            bill_id = int(input("Bill ID: "))
            self.billing_service.pay_bill(bill_id)
        except ValueError:
            print("❌ Invalid input")
    
    def _view_unpaid(self):
        """View unpaid bills"""
        unpaid = self.billing_service.get_unpaid_bills()
        overdue = self.billing_service.get_overdue_bills()
        
        if not unpaid:
            print("✅ No unpaid bills")
            return
        
        print("\n" + "=" * 50)
        print("Unpaid Bills")
        print("=" * 50)
        for bill in unpaid:
            print(f"  {bill}")
        print("=" * 50)
        
        if overdue:
            print(f"\n⚠️ Overdue: {len(overdue)} bills")
    
    def _greedy_collection(self):
        """Run greedy collection algorithm"""
        try:
            limit = int(input("Collection limit: "))
            self.billing_service.greedy_collection(limit)
        except ValueError:
            print("❌ Invalid input")
    
    def _heap_demo(self):
        """Run heap demo"""
        from heap import MinHeap
        from models import Bill
        
        print("\n" + "=" * 50)
        print("Min-Heap Demo")
        print("=" * 50)
        
        heap = MinHeap()
        bills = [
            Bill(101, 1000, 2500, "2026-03-15"),
            Bill(102, 1001, 3200, "2026-02-10"),
            Bill(103, 1002, 1800, "2026-04-01"),
            Bill(101, 1000, 2500, "2026-01-20"),
        ]
        
        print("\nInserting bills:")
        for bill in bills:
            heap.insert(bill)
            print(f"  Inserted: Due {bill.due_date}")
        
        print(f"\nPeek (earliest due): {heap.peek().due_date}")
        
        print("\nExtracting in order:")
        while not heap.is_empty():
            bill = heap.extract_min()
            print(f"  Extracted: Due {bill.due_date}")
    
    def _greedy_demo(self):
        """Run greedy algorithm explanation demo"""
        self.billing_service.greedy_collection_demo()
    
    def _show_statistics(self):
        """Show statistics"""
        self.billing_service.print_bill_summary()
        
        # Show room stats
        rooms = self.room_repo.get_all()
        occupied = len(self.room_repo.get_occupied_rooms())
        print(f"\n🏠 Room Statistics:")
        print(f"   Total: {len(rooms)}")
        print(f"   Occupied: {occupied}")
        print(f"   Available: {len(rooms) - occupied}")
        print(f"   Occupancy Rate: {(occupied/len(rooms)*100):.1f}%" if rooms else "0%")
    
    def _save_and_exit(self):
        """Save and exit"""
        print("👋 Goodbye!")
    
    def run(self):
        """Main application loop"""
        while True:
            self._show_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self._add_room()
            elif choice == '2':
                self._list_rooms()
            elif choice == '3':
                self._add_tenant()
            elif choice == '4':
                self._list_tenants()
            elif choice == '5':
                self._rent_room()
            elif choice == '6':
                self._vacate_room()
            elif choice == '7':
                self._generate_bills()
            elif choice == '8':
                self._list_bills()
            elif choice == '9':
                self._pay_bill()
            elif choice == '10':
                self._view_unpaid()
            elif choice == '11':
                self._greedy_collection()
            elif choice == '12':
                self._heap_demo()
            elif choice == '13':
                self._greedy_demo()
            elif choice == '14':
                self._show_statistics()
            elif choice == '15':
                self._save_and_exit()
                break
            else:
                print("❌ Invalid option")


if __name__ == "__main__":
    app = ApartmentApp()
    app.run()
