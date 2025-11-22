import os
import json
import mysql.connector
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "db"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "db"),
}

@app.post("/query")
async def run_query(request: Request):
    body = await request.json()
    sql = body.get("sql")
    if not sql:
        return {"error": "Missing 'sql' in request"}

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"success": True, "rows": rows}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=52765)
