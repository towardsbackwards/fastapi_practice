steps:
pip install -r requirements.txt
alembic init migrations
alembic revision --autogenerate -m "Initial"
alembic upgrade head
redis-server

start app:
uvicorn main:app --reload

check redis storage:
redis-cli --scan --pattern '*'
