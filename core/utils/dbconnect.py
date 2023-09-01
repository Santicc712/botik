import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_user(self, user_id: int, first_name: str, last_name: str, username: str) -> None:
        query = "INSERT INTO user_pro (user_id, first_name, last_name, username) " \
                "VALUES ($1, $2, $3, $4) " \
                "ON CONFLICT (user_id) DO NOTHING"
        return await self.connector.fetchval(query, user_id, first_name, last_name, username)