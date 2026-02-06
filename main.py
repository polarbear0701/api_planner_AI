from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal, init_db
from sqlalchemy import text


app = FastAPI(
	title="AI Planner API",
	description="AI-powered planning and task management API",
	version="0.1.0"
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
	init_db()
	print("Database initialized")

@app.get("/health")
async def health_check():
	return {"status": "ok"}
	
@app.get("/db_test")
async def test_db():
	db = SessionLocal()
	try:
		db.execute(text("SELECT 1"))
		db.close
		return {"status": "Database connecttion successful"}
	except Exception as e:
		return {"status": f"Database connection failed: {str(e)}"}
		

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)