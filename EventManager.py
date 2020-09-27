import asyncio
from collections import deque


# TODO - нужно добавить возможность удалять задачи по таймауту или же при
#  определенных обстоятельствах
class EventManager:
    def __init__(self):
        self.tasks = deque()

    # Начать обработку событийного цикла событий
    async def handle(self):
        await asyncio.gather(*self.tasks)

    # Добавить задачу в событийный цикл
    def add_task(self, func, *args, **params):
        task = asyncio.create_task(func(*args, **params))
        self.tasks.append(task)
