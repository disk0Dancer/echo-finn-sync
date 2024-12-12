# Отчёт по лабораторной работе
# Автор работы: Чураков Григорий

## Название работы
Реализация и тестирование алгоритмов «Эхо» и «Финн» для распределённых вычислений

## Цель работы
1. Реализация алгоритмов «Эхо» и «Финн» для синхронизации процессов в распределённой системе.
2. Изучение работы алгоритмов в различных топологиях сети.
3. Использование RabbitMQ для коммуникации между процессами.

---

## Постановка задачи
1. Разработать алгоритм «Эхо» для синхронизации процессов в сети с древовидной топологией.
2. Реализовать алгоритм «Финн» для произвольной ориентированной сети.
3. Организовать взаимодействие между процессами с использованием RabbitMQ.
4. Провести тестирование и анализ производительности.

---

## Теоретическое обоснование

### Алгоритм «Эхо»
Алгоритм «Эхо» используется для широковещательной передачи данных в древовидной сети:
- Инициатор отправляет сообщение всем соседям.
- Каждый узел пересылает сообщение дальше, кроме отправителя.
- Листовые узлы возвращают сообщение «эхо» инициатору.
- Алгоритм завершается, когда инициатор получает ответы от всех соседей.

**Применение:** подходит для задач глобальной синхронизации.

---

### Алгоритм Финна
Алгоритм Финна предназначен для работы с произвольными направленными графами. 
Каждый процесс ведёт два множества:
1. \( Inc(s) \): процессы, которые предшествовали текущему.
2. \( NInc(s) \): процессы, предшествовавшие соседним узлам.

Процесс завершает свою работу, когда множества становятся равны.

**Применение:** обеспечивает согласованность состояния процессов в сложных сетях.

---

## Реализация

### Используемые технологии
1. **Язык программирования:** Python.
2. **Среда обмена:** RabbitMQ.
3. **Библиотека для работы с RabbitMQ:** `pika`.

---

### Устройство клиента RabbitMQ
#### 1. Создание соединения
Клиент устанавливает соединение с RabbitMQ:
```python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
```

#### 2. Объявление очередей
Очереди используются для отправки и получения сообщений:
```python
queue_name = 'node_queue'
channel.queue_declare(queue=queue_name)
```

#### 3. Публикация сообщений
Сообщения отправляются с использованием basic_publish:
```python
message = {'type': 'token', 'sender': 'node1'}
channel.basic_publish(exchange='', routing_key='node_queue', body=json.dumps(message))
```

#### 4. Подписка на события
Подписка реализуется с помощью basic_consume:

```python
def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
```

---

### Реализация алгоритмов

#### Алгоритм «Эхо»

- Сообщения отправляются через очереди.
- Узлы обрабатывают сообщения и пересылают их дальше.
- Листовые узлы возвращают маркеры обратно к инициатору.

#### Алгоритм «Финн»

- Каждый узел обновляет множества ( Inc ) и ( NInc ) на основе полученных сообщений.
- Сообщения передаются в соседние узлы до выполнения условия завершения.

### Тестирование

#### Алгоритм «Эхо»

1.	Тестирование проводилось на древовидной сети из 7 узлов.
2.	Алгоритм завершил работу корректно, инициатор получил ответы от всех соседей.
3.	Время выполнения увеличивалось линейно с глубиной дерева.

#### Алгоритм «Финна»

1.	Тестировался на графе из 5 узлов.
2. Алгоритм показал стабильность при различных последовательностях событий.
3.	Затраты на память увеличиваются с ростом размера множества ( Inc ).