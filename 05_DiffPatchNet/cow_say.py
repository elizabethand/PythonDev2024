import asyncio
import cowsay

clients = {}
available_cows = cowsay.list_cows() + ["cow"]

async def handle_login(writer, name):
    if name == "?":
        writer.write(f"{available_cows}\n".encode())
        await writer.drain()
        return None
    elif name not in available_cows:   
        writer.write("This name is not on the list of available cow names.\n".encode())
        writer.write("To get a list of cows, enter '?'.\n\n".encode())
        await writer.drain()
        return None
    elif name not in clients.keys():
        clients[name] = asyncio.Queue()  
        writer.write(f"Welcome, {name}!\n\n".encode())
        available_cows.remove(name)
        await writer.drain()
        print(f"User <{name.upper()}> has joined the chat.")
        return name
    else:
        writer.write("This cow's name is already taken. Please choose another one.\n".encode())
        await writer.drain()
        return None
    
async def handle_receive(writer, me):
    while True:
        message = await clients[me].get()
        writer.write(message.encode())
        await writer.drain()

async def create_cow_cay(me, text):
    if me == "cow":
        cow = "default"
    else:
        cow = me
    return cowsay.cowsay(message=text, cow=cow)

async def handle_commands(writer, me, message):
    global available_cows

    if message.startswith("who"):
        print(f"{me}: {message}")
        writer.write("\nRegistered cows:\n".encode())
        for cow in clients:
            writer.write(f"- {cow}\n".encode())
        writer.write(f"\n".encode())
        await writer.drain()
    elif message.startswith("cows"):
        print(f"{me}: {message}")
        writer.write("Available cow names:\n".encode())
        writer.write(f"{available_cows}\n".encode())
        await writer.drain()
    elif message.startswith("say"):
        print(f"{me}: {message}")
        _, recipient, text = message.split(" ", 2)
        await clients[recipient].put(await create_cow_cay(me, text))

    elif message.startswith("yield"):
        print(f"{me}: {message}")
        _, text = message.split(" ", 1)
        for client_queue in clients.values():
            await client_queue.put(await create_cow_cay(me, text))

    elif message.startswith("quit"):
        writer.write("Goodbye!\n".encode())
        await writer.drain()
        writer.close()
        available_cows = available_cows + [me]
        del clients[me]
        print(f"<{me.upper()}> has left the chat.")

async def handle_chat(reader, writer):
    me = None
    while me is None:
        message = (await reader.readline()).decode().strip()
        if message.startswith("login"):
            _, cow_name = message.split(" ", 1)
            me = await handle_login(writer, cow_name)
        elif message.startswith("quit"):
            writer.write("Goodbye!\n".encode())
            me = 1
            await writer.drain()
            writer.close()
        else:
            writer.write("\nError!\n".encode())
            writer.write("To use the chat, enter the command:\n".encode())
            writer.write("\tlogin cow_name\n".encode())
            writer.write("instead of cow_name, enter your login from available cow names.\n\n".encode())

    receive_task = asyncio.create_task(handle_receive(writer, me))
    try:
        while not reader.at_eof():
            message = (await reader.readline()).decode().strip()
            await handle_commands(writer, me, message)
    finally:
        receive_task.cancel()
        writer.close()
        await writer.wait_closed()


async def handle_receive(writer, name):
    while True:
        message = await clients[name].get()
        writer.write(f"{message}\n".encode())
        await writer.drain()

async def main():
    server = await asyncio.start_server(handle_chat, '0.0.0.0', 1337)
    async with server:
        print("Server started. Listening for incoming connections...")
        await server.serve_forever()

asyncio.run(main())
