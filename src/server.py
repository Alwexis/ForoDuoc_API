import uvicorn
from fastapi import FastAPI, Request
import json
from db import DB
from models import Tarea, AutoIncremento

app = FastAPI()
db = DB()

@app.get("/")
async def root():
    productos = await db.get("productos")
    return json.loads(json.dumps(productos))

@app.get("/tareas")
async def get_tareas(request: Request):
    params = {}
    for k, v in request.query_params.items():
        params[k] = v
    tareas = await db.get("Tareas", params)
    return json.loads(json.dumps(tareas))

@app.post("/tareas")
async def post_tareas(tarea: Tarea):
    auto_incremento = AutoIncremento("tareas")
    tarea.id = await auto_incremento.next()
    await db.insert("Tareas", tarea.model_dump())
    return json.loads(json.dumps(tarea.model_dump()))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)