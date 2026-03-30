from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.services.neo4j_service import init_graph
from app.services.kafka_consumer import start_consumer
import threading

app = FastAPI(title="Bitcoin AML Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_graph()
    threading.Thread(target=start_consumer, daemon=True).start()

app.include_router(router, prefix="/api")
