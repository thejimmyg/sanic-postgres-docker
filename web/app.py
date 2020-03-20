import os


from asyncpg import create_pool
from sanic import Sanic
from sanic.response import json


app = Sanic(__name__)


# https://stackoverflow.com/questions/49978507/using-asyncpg-connection-pool-with-sanic
@app.listener('before_server_start')
async def init_pg(app, loop):
    class Pg:
        def __init__(self, pg_pool):
            self.pg_pool = pg_pool
    
        async def fetch(self, sql, *args, **kwargs):
            async with self.pg_pool.acquire() as connection:
                return await connection.fetch(sql, *args, **kwargs)
    
        async def execute(self, sql, *args, **kwargs):
            async with self.pg_pool.acquire() as connection:
                return await connection.execute(sql, *args, **kwargs)

    app.pg_pool = await create_pool(
        os.environ['DATABASE_URL'],
        loop=loop,
    )
    app.pg = Pg(app.pg_pool)
    print('-------- setup connection pool --------')


@app.listener('after_server_stop')
async def cleanup_pg(app, loop):
    await app.pg_pool.close()
    print('-------- shutdown connection pool --------')


@app.route("/")
async def root(req):
    result = await req.app.pg.fetch('SELECT 1 as a, 2 as b')
    print(result)
    return json([dict(r) for r in result])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', '8000')))
