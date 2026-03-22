from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as honeypot_router
from app.api.admin_routes import router as admin_router


app = FastAPI(
    title="AI Agentic HoneyPot API",
    description=(
        "Detects scam messages, engages scammers, extracts intelligence, "
        "stores conversations, and provides analytics."
    ),
    version="1.1.0"
)

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Safe for hackathon/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROUTES --------------------
# Core honeypot + demo routes
app.include_router(honeypot_router)

# Admin / analytics routes (MongoDB-backed)
app.include_router(admin_router)
