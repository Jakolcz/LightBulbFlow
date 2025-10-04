import asyncio


async def main():
    print("Hello, async World!")
    pass


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by keyboard interrupt")
