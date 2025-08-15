# Hotel Management System

Simple hotel management API built with Flask and SQLite. It allows managing rooms and reservations and can serve as a foundation for a full-featured system.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## API Overview

- `GET /rooms` – list all rooms
- `POST /rooms` – add a new room (`{"number": "101", "type": "single", "price": 100}`)
- `GET /reservations` – list reservations
- `POST /reservations` – create a reservation (`{"room_id": 1, "guest_name": "Alice", "check_in": "2024-01-01", "check_out": "2024-01-02"}`)
- `GET /rooms/<id>/availability?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD` – check room availability

## Testing

```bash
python -m unittest
```
