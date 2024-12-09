install:
	brew install rabbitmq
	uv sync

up:
	brew services start rabbitmq
	@wait

echo: up
	@echo "RabbitMQ is running"
	uv run echo.py
	
finn: up
	@echo "RabbitMQ is running"
	uv run finn.py
	