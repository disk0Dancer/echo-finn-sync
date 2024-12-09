install:
	brew install rabbitmq
	uv sync

up:
	brew services start rabbitmq
	@echo "Admin UI: http://localhost:15672"
	@wait


down:
	brew services stop rabbitmq
	rm app.log
	@echo "RabbitMQ is stopped"

echo: up
	@echo "RabbitMQ is running"
	uv run echo.py
	
finn: up
	@echo "RabbitMQ is running"
	uv run finn.py
	