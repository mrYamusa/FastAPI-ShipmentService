# # from fastapi import FastAPI
# # from contextlib import asynccontextmanager
# # from rich import panel, print
# from passlib.context import CryptContext

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

# password = "verystrong"
# context = CryptContext(schemes="sha256_crypt")
# context = CryptContext(schemes="bcrypt_sha256")
# context = CryptContext(schemes="bcrypt", deprecated="auto")
# hash = context.hash(password)
# print(context.hash(password), password)
# print(context.hash(password), password)
# print(context.verify("verystrong", context.hash(password)))
# print(context.verify("verystrong", hash))

import requests
import json

# Configuration
URL_DATA = "https://simplora.org/data"
URL_VERIFY = "https://simplora.org/verify-message"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpY3NpZGF2aWRAZ21haWwuY29tIiwiZXhwIjoxNzY2NzcyNTYyfQ.A1FUNVUutDe6D5prPSeOj2w2ZZfyolG_QTXCPLZ37e8"
EMAIL = "icsidavid@gmail.com"

MORSE_CODE_DICT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "/": " ",
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "text/event-stream",
    "Cache-Control": "no-cache",
}

print("🚀 Starting the decoding process...")

morse_signals = []

# 1. Capture the stream
with requests.get(URL_DATA, headers=headers, stream=True) as response:
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                # We only care about lines starting with 'data: '
                if decoded_line.startswith("data:"):
                    signal = decoded_line.replace("data:", "").strip()

                    if signal == "END":
                        break

                    # Store signal (including spaces and / separators)
                    if signal == "":  # Handle the empty space signals
                        continue
                    morse_signals.append(signal)
    else:
        print(f"❌ Failed to connect: {response.status_code}")
        exit()

# 2. Join signals and decode
# The signals coming in are individual letters/separators.
# We join them into a string, then split by '/' for words.
full_morse = " ".join(morse_signals)
print(f"📡 Raw Morse: {full_morse}")


def decode_morse(signals):
    decoded_message = ""
    for symbol in signals:
        if symbol in MORSE_CODE_DICT:
            decoded_message += MORSE_CODE_DICT[symbol]
    return decoded_message


final_message = decode_morse(morse_signals)
print(f"✅ Decoded Message: {final_message}")

# 3. Send verification POST request
verify_headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

payload = {"message": final_message, "email": EMAIL}

print("📤 Sending verification...")
verify_response = requests.post(URL_VERIFY, headers=verify_headers, json=payload)

if verify_response.status_code == 200:
    print("🎊 Success!")
    print(json.dumps(verify_response.json(), indent=4))
else:
    print(f"⚠️ Verification Failed: {verify_response.status_code}")
    print(verify_response.text)
