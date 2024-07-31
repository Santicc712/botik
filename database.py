import aiosqlite

DATABASE_NAME = 'garage.db'


async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                model TEXT NOT NULL
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS repairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (car_id) REFERENCES cars(id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wishlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (car_id) REFERENCES cars(id)
            )
        ''')
        await db.commit()


async def add_car(user_id: int, name: str, model: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            INSERT INTO cars (user_id, name, model) VALUES (?, ?, ?)
        ''', (user_id, name, model))
        await db.commit()


async def list_cars(user_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute('SELECT id, name, model FROM cars WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchall()


async def update_car(car_id: int, new_name: str, new_model: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            UPDATE cars SET name = ?, model = ? WHERE id = ?
        ''', (new_name, new_model, car_id))
        await db.commit()


async def delete_car(car_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('DELETE FROM cars WHERE id = ?', (car_id,))
        await db.execute('DELETE FROM repairs WHERE car_id = ?', (car_id,))
        await db.execute('DELETE FROM wishlist WHERE car_id = ?', (car_id,))
        await db.commit()


async def add_repair(car_id: int, description: str, date: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            INSERT INTO repairs (car_id, description, date) VALUES (?, ?, ?)
        ''', (car_id, description, date))
        await db.commit()


async def list_repairs(car_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute('SELECT id, description, date FROM repairs WHERE car_id = ?', (car_id,)) as cursor:
            return await cursor.fetchall()


async def update_repair(repair_id: int, new_description: str, new_date: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            UPDATE repairs SET description = ?, date = ? WHERE id = ?
        ''', (new_description, new_date, repair_id))
        await db.commit()


async def delete_repair(repair_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('DELETE FROM repairs WHERE id = ?', (repair_id,))
        await db.commit()


async def add_wishlist(car_id: int, description: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            INSERT INTO wishlist (car_id, description) VALUES (?, ?)
        ''', (car_id, description))
        await db.commit()


async def list_wishlist(car_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute('SELECT id, description FROM wishlist WHERE car_id = ?', (car_id,)) as cursor:
            return await cursor.fetchall()


async def update_wishlist(wishlist_id: int, new_description: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            UPDATE wishlist SET description = ? WHERE id = ?
        ''', (new_description, wishlist_id))
        await db.commit()


async def delete_wishlist(wishlist_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('DELETE FROM wishlist WHERE id = ?', (wishlist_id,))
        await db.commit()