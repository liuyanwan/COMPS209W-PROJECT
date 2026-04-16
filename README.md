# COMP S209W individual project
# 🏢 Apartment Management System

A Python-based apartment management system implementing Object-Oriented Programming (OOP) concepts with **Min-Heap** data structure and **Greedy Algorithm** for bill collection scheduling.

##  Features

### Core Features
- 🏠 Room Management (add, view, rent, vacate)
- 👤 Tenant Management (add, view, search)
- 💰 Bill Management (generate monthly bills, pay, view status)

### Algorithm Implementation 
- **Min-Heap (Priority Queue)**: Bill priority queue based on due date
  - `insert()`: O(log n)
  - `peek()`: O(1)
  - `extract_min()`: O(log n)
  - `build_heap()`: O(n)
  
- **Greedy Collection Algorithm**: Always selects the earliest due bill for collection
  - Time Complexity: O(n + k log n)
  - Heap finds optimal choice, Greedy makes local optimal decision each step

## Project Structure

| File | Description |
|------|-------------|
| `models.py` | Data models: Tenant, Room, Bill classes |
| `heap.py` | Min-Heap ADT implementation (insert, extract_min, peek) |
| `repositories.py` | CRUD operations for in-memory data storage |
| `services.py` | Business logic + Greedy Collection Algorithm |
| `app.py` | CLI menu and application entry point |
| `README.md` | Project documentation |

## OOP Concepts

| Concept | Location | Description |
|---------|----------|-------------|
| Encapsulation | `models.py` | Private `_status`, `_current_tenant_id` |
| Polymorphism | `heap.py` | `__lt__` method for heap comparison |
| Composition | `services.py` | Service contains multiple repositories |

## Example Workflow
1. Add a room
>Area: 50
Monthly Rent: 3000
Deposit: 6000

2. Add a tenant
>Name: AAA
Phone: 12345678
Email: AAA@example.com

3. Rent room to tenant
>Room Number: 101
Tenant ID: 1000

4. Generate monthly bills
>Year: 2026
Month: 3

5. Run greedy collection
>Limit: 5

🏢 Apartment Management System
========================================
1. Add Room        8. List Bills
2. List Rooms      9. Pay Bill
3. Add Tenant     10. View Unpaid
4. List Tenants   11. Greedy Collection
5. Rent Room      12. Heap Demo
6. Vacate Room    13. Statistics
7. Generate Bills 14. Exit

## How to Run
python app.py

## Technologies Used
Language: Python 3.7+

Data Structures: Custom Min-Heap implementation

Algorithms: Greedy Collection Algorithm

## References
- [Heap Data Structure - Wikipedia](https://en.wikipedia.org/wiki/Heap_(data_structure))
- [Greedy Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Greedy_algorithm)
- [GeeksforGeeks: Heap Data Structure](https://www.geeksforgeeks.org/heap-data-structure/)
- [GeeksforGeeks: Greedy Algorithms](https://www.geeksforgeeks.org/greedy-algorithms/)

