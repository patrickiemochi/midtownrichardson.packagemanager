from flask import Flask, request, jsonify
import sqlite3
from contextlib import closing

app = Flask(__name__)
DB_NAME = 'hotel.db'


def init_db():
    with closing(sqlite3.connect(DB_NAME)) as db:
        c = db.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS rooms (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   number TEXT UNIQUE NOT NULL,
                   type TEXT NOT NULL,
                   price REAL NOT NULL
               )'''
        )
        c.execute(
            '''CREATE TABLE IF NOT EXISTS reservations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   room_id INTEGER NOT NULL,
                   guest_name TEXT NOT NULL,
                   check_in TEXT NOT NULL,
                   check_out TEXT NOT NULL,
                   FOREIGN KEY(room_id) REFERENCES rooms(id)
               )'''
        )
        db.commit()


@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'POST':
        data = request.get_json()
        with closing(sqlite3.connect(DB_NAME)) as db:
            c = db.cursor()
            c.execute(
                'INSERT INTO rooms (number, type, price) VALUES (?, ?, ?)',
                (data['number'], data['type'], data['price'])
            )
            db.commit()
            room_id = c.lastrowid
        return jsonify({'id': room_id, 'status': 'created'}), 201
    else:
        with closing(sqlite3.connect(DB_NAME)) as db:
            c = db.cursor()
            c.execute('SELECT id, number, type, price FROM rooms')
            rows = c.fetchall()
            rooms = [dict(zip(['id', 'number', 'type', 'price'], row)) for row in rows]
        return jsonify(rooms)


@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if request.method == 'POST':
        data = request.get_json()
        with closing(sqlite3.connect(DB_NAME)) as db:
            c = db.cursor()
            c.execute(
                '''SELECT COUNT(*) FROM reservations
                   WHERE room_id=? AND NOT (check_out<=? OR check_in>=?)''',
                (data['room_id'], data['check_in'], data['check_out'])
            )
            if c.fetchone()[0] > 0:
                return jsonify({'error': 'Room not available'}), 400
            c.execute(
                'INSERT INTO reservations (room_id, guest_name, check_in, check_out) VALUES (?,?,?,?)',
                (data['room_id'], data['guest_name'], data['check_in'], data['check_out'])
            )
            db.commit()
            res_id = c.lastrowid
        return jsonify({'id': res_id, 'status': 'booked'}), 201
    else:
        with closing(sqlite3.connect(DB_NAME)) as db:
            c = db.cursor()
            c.execute('SELECT id, room_id, guest_name, check_in, check_out FROM reservations')
            rows = c.fetchall()
            reservations = [
                dict(zip(['id', 'room_id', 'guest_name', 'check_in', 'check_out'], row))
                for row in rows
            ]
        return jsonify(reservations)


@app.route('/rooms/<int:room_id>/availability')
def check_availability(room_id):
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    with closing(sqlite3.connect(DB_NAME)) as db:
        c = db.cursor()
        c.execute(
            '''SELECT COUNT(*) FROM reservations
               WHERE room_id=? AND NOT (check_out<=? OR check_in>=?)''',
            (room_id, check_in, check_out)
        )
        available = c.fetchone()[0] == 0
    return jsonify({'room_id': room_id, 'available': available})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
