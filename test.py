# # from fastapi import FastAPI
# # from contextlib import asynccontextmanager
# # from rich import panel, print
from passlib.context import CryptContext

# # @asynccontextmanager
# # async def lifespan_handler(app: FastAPI):
# #     print(panel.Panel("Starting up Yamusa's server...", border_style="green"))
# #     yield
# #     print(panel.Panel("Shutting down Yamusa's server...", border_style="red"))


# # app = FastAPI(title="Mr Yamusa's FastAPI Shipment Service", lifespan=lifespan_handler)


# # @app.get("/{word}")
# # def read_root(word: str):
# #     return {"Hello": word}

# import time
# import asyncio
# from rich import print


# # async def endpoint(route: str) -> str:
# #     print(f"Handling {route}")
# #     await asyncio.sleep(0)
# #     print(f"Response {route}")
# #     return route


# # async def server():
# #     tests = ("GET /shipment?id=1", "PATCH /shipment?id=4", "GET /shipment?id=3")
# #     start = time.perf_counter()
# #     # requests = [asyncio.create_task(endpoint(route)) for route in tests]
# #     async with asyncio.TaskGroup() as task_group:  #
# #         requests = [task_group.create_task(endpoint(route)) for route in tests]
# #         print(await requests[0])
# #     # done, pending = await asyncio.wait(requests)
# #     end = time.perf_counter()

# #     print(f"Time taken {end - start:.2f}s")


# # asyncio.run(server())


# async def task(route: str, delay: int) -> str:
#     print(f"Handling {route}")
#     await asyncio.sleep(delay)
#     print(f"Response {route}")
#     return route


# async def server():
#     routes = ("GET /shipment?id=1", "PATCH /shipment?id=4", "GET /shipment?id=3")
#     start = time.perf_counter()
#     # responses = [endpoint(route) for route in routes]
#     async with asyncio.TaskGroup() as task_group:
#         task_group.create_task(task(routes[0], 2))
#         task_group.create_task(task(routes[1], 4))
#         task_group.create_task(task(routes[2], 3))
#     end = time.perf_counter()

#     print(f"Time taken {end - start:.2f}s")


# asyncio.run(server())

password = "verystrong"
# context = CryptContext(schemes="sha256_crypt")
context = CryptContext(schemes="bcrypt_sha256")
# context = CryptContext(schemes="bcrypt", deprecated="auto")
hash = context.hash(password)
# print(context.hash(password), password)
# print(context.hash(password), password)
# print(context.verify("verystrong", context.hash(password)))
print(context.verify("verystrong", hash))
