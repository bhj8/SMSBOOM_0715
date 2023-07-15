import requests
import os

def check_proxy(protocol, ip, port):
    url = f"{protocol}://{ip}:{port}"
    proxies = {protocol: url}

    if protocol in ['socks4', 'socks5']:
        proxies = {
            'http': url,
            'https': url,
        }

    try:
        response = requests.get('https://www.google.com', proxies=proxies, timeout=5)
        print(f"Success with {ip}:{port}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error with {ip}:{port}. Exception: {e}")
        return False

def process_file(protocol, filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    valid_proxies = [line.strip() for line in lines if check_proxy(protocol, *line.strip().split(':'))]

    with open(filename, 'w') as f:
        for proxy in valid_proxies:
            f.write(proxy + '\n')

# 设置全局代理
os.environ['http_proxy'] = "http://127.0.0.1:7890"
os.environ['https_proxy'] = "http://127.0.0.1:7890"

# 处理文件
process_file('http', 'http_proxy.txt')
process_file('socks4', 'socks4_proxy.txt')
process_file('socks5', 'socks5_proxy.txt')
