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


