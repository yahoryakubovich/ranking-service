IMAGE_NAME ?= ranking-service:latest

compute-scores:
	@echo "Computing interest and popularity scores..."
	@python scripts/compute_scores.py

populate-redis:
	@echo "Populating Redis..."
	@python scripts/populate_redis.py

build:
	@echo "Exporting requirements and building image..."
	uv export > requirements.txt
	docker build -t $(IMAGE_NAME) .

up:
	@echo "Starting Redis and Ranking Service..."
	docker-compose up -d

down:
	@echo "Stopping containers..."
	docker-compose down

load-test:
	@echo "Running load test..."
	locust -f tests/locustfile.py --host=http://localhost:8000