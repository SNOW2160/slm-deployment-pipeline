import requests
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def call(url, prompt, api_key):
    payload = {"prompt": prompt, "max_tokens": 32}
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    t0 = time.time()
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    t1 = time.time()
    return (t1 - t0), r.status_code, r.text

def run(url, prompt, total, concurrency, api_key):
    results = []
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(call, url, prompt, api_key) for _ in range(total)]
        for f in as_completed(futures):
            try:
                results.append(f.result())
            except Exception as e:
                results.append((None, "error", str(e)))
    latencies = [r[0] for r in results if isinstance(r[0], float)]
    latencies.sort()
    if not latencies:
        print("No successful results")
        return
    def pct(p):
        idx = int(p/100.0 * (len(latencies)-1))
        return latencies[idx]
    print(f"requests: {total}, success: {len(latencies)}")
    print(f"p50: {pct(50):.3f}s, p95: {pct(95):.3f}s, p99: {pct(99):.3f}s")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost:8000/generate')
    parser.add_argument('--prompt', default='Hello world')
    parser.add_argument('--requests', type=int, default=20)
    parser.add_argument('--concurrency', type=int, default=4)
    parser.add_argument('--api_key', default='devkey')
    args = parser.parse_args()
    run(args.url, args.prompt, args.requests, args.concurrency, args.api_key)
