steps:
pip install -r requirements.txt
alembic init migrations
alembic revision --autogenerate -m "Initial"
alembic upgrade head
redis-server

### from src/:
celery -A tasks.tasks:celery worker --loglevel=INFO
celery -A tasks.tasks:celery flower


start app:
uvicorn main:app --reload

check redis storage:
redis-cli --scan --pattern '*'


steps[docker]:
docker compose build
docker compose up