from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime
import asyncio
import os

app = FastAPI()

# Configuración de CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Configuración para guardar imágenes
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Almacenamiento en memoria para notificaciones
notifications = []
active_connections = []

class ConnectionManager:
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/realtime", response_class=HTMLResponse)
async def realtime_view(request: Request):
    return templates.TemplateResponse("realtime.html", {"request": request, "notifications": notifications})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantener conexión abierta
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/webhook")
async def receive_notification(
    echa: str = Form(...),
    hora: str = Form(...),
    direccion: str = Form(...),
    idCamara: str = Form(...),
    imagen: UploadFile = File(...)
):
    # Guardar la imagen
    file_extension = os.path.splitext(imagen.filename)[1]
    unique_filename = f"{datetime.now().timestamp()}{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_location, "wb+") as file_object:
        file_object.write(await imagen.read())

    # Crear objeto de notificación
    notification = {
        "echa": echa,
        "hora": hora,
        "direccion": direccion,
        "idCamara": idCamara,
        "imagen": unique_filename,  # Guardamos el nombre único del archivo
        "timestamp": datetime.now().isoformat(),
        "image_url": f"/uploads/{unique_filename}"  # Ruta para acceder a la imagen
    }

    # Guardar notificación
    notifications.append(notification)
    
    # Enviar a clientes WebSocket
    await manager.broadcast(notification)
    
    return {
        "status": "received",
        "data": {
            **notification,
            "imagen": "Archivo recibido correctamente"  # No devolvemos el nombre completo por seguridad
        }
    }

@app.get("/notifications")
async def get_notifications():
    return notifications

# Servir archivos estáticos (imágenes subidas)
from fastapi.staticfiles import StaticFiles
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)