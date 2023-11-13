import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []
lock = threading.Lock()

with open('proxy2.txt', 'r') as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            r = requests.get('https://ipinfo.io/json', proxies={'https': proxy, 'http': proxy}, timeout=2)
        except:
            continue
        if r.status_code == 200:
                print(proxy)

threads = []
for _ in range(10):
    threading.Thread(target=check_proxies).start()

# Now print all valid proxies
print("Valid proxies:")
for proxy in valid_proxies:
    print(proxy)
