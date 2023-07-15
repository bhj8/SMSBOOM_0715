import aiohttp
import asyncio
import os

sem = asyncio.Semaphore(50)

async def check_proxy(session, protocol, ip, port):
    url = f"{protocol}://{ip}:{port}"
    proxy = os.environ.get('http_proxy', None)

    async with sem:
        try:
            async with session.get('https://www.google.com', proxy=proxy, timeout=5) as response:
                print(f"Success with {ip}:{port}")
                return response.status == 200
        except Exception as e:
            print(f"Error with {ip}:{port}. Exception: {e}")
            return False


async def process_file(protocol, filename):
    async with aiohttp.ClientSession() as session:
        with open(filename, 'r') as f:
            lines = f.readlines()

        tasks = [check_proxy(session, protocol, *line.strip().split(':')) for line in lines]

        results = await asyncio.gather(*tasks)

        valid_proxies = [line for result, line in zip(results, lines) if result]

        with open(filename, 'w') as f:
            for proxy in valid_proxies:
                f.write(proxy + '\n')


# 设置全局代理
os.environ['http_proxy'] = "http://127.0.0.1:7890"
os.environ['https_proxy'] = "http://127.0.0.1:7890"

# 运行协程
asyncio.run(process_file('http', 'http_proxy.txt'))
asyncio.run(process_file('socks4', 'socks4_proxy.txt'))
asyncio.run(process_file('socks5', 'socks5_proxy.txt'))
