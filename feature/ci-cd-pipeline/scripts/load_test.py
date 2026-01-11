#!/usr/bin/env python3
"""
Load testing script for Recommendation API
Branch: feature/ci-cd-pipeline
"""

import requests
import time
import concurrent.futures
import statistics
from typing import List, Dict
import argparse
import sys


class LoadTester:
    """Simple load tester for API endpoints"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []

    def make_request(self, endpoint: str, method: str = "GET", data: dict = None) -> Dict:
        """Make a single request and measure time"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()

        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            end_time = time.time()
            response_time = end_time - start_time

            return {
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code == 200,
                "error": None,
            }
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            return {"status_code": None, "response_time": response_time, "success": False, "error": str(e)}

    def run_load_test(
        self, endpoint: str, num_requests: int = 100, concurrency: int = 10, method: str = "GET", data: dict = None
    ) -> Dict:
        """Run load test with specified parameters"""
        print(f"Running load test: {num_requests} requests, {concurrency} concurrent workers")
        print(f"Endpoint: {endpoint}, Method: {method}")

        results = []
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(self.make_request, endpoint, method, data) for _ in range(num_requests)]

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        end_time = time.time()
        total_time = end_time - start_time

        return self.analyze_results(results, total_time)

    def analyze_results(self, results: List[Dict], total_time: float) -> Dict:
        """Analyze load test results"""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        response_times = [r["response_time"] for r in successful]

        stats = {
            "total_requests": len(results),
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "success_rate": len(successful) / len(results) * 100 if results else 0,
            "total_time": total_time,
            "requests_per_second": len(results) / total_time if total_time > 0 else 0,
            "avg_response_time": statistics.mean(response_times) if response_times else 0,
            "median_response_time": statistics.median(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "errors": [r["error"] for r in failed if r["error"]],
        }

        return stats

    def print_results(self, stats: Dict):
        """Print load test results"""
        print("\n" + "=" * 60)
        print("LOAD TEST RESULTS")
        print("=" * 60)
        print(f"Total Requests:      {stats['total_requests']}")
        print(f"Successful:          {stats['successful_requests']}")
        print(f"Failed:              {stats['failed_requests']}")
        print(f"Success Rate:        {stats['success_rate']:.2f}%")
        print(f"Total Time:          {stats['total_time']:.2f}s")
        print(f"Requests/Second:     {stats['requests_per_second']:.2f}")
        print(f"\nResponse Times:")
        print(f"  Average:           {stats['avg_response_time']:.3f}s")
        print(f"  Median:            {stats['median_response_time']:.3f}s")
        print(f"  Min:               {stats['min_response_time']:.3f}s")
        print(f"  Max:               {stats['max_response_time']:.3f}s")

        if stats["errors"]:
            print(f"\nErrors ({len(stats['errors'])}):")
            unique_errors = list(set(stats["errors"]))
            for error in unique_errors[:5]:  # Show first 5 unique errors
                print(f"  - {error}")

        print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Load test for Recommendation API")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--requests", type=int, default=100, help="Number of requests")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent workers")
    parser.add_argument("--endpoint", default="/predict", help="Endpoint to test")

    args = parser.parse_args()

    tester = LoadTester(base_url=args.url)

    # Test health endpoint
    print("Testing /health endpoint...")
    health_stats = tester.run_load_test(
        endpoint="/health", num_requests=args.requests, concurrency=args.concurrency, method="GET"
    )
    tester.print_results(health_stats)

    # Test predict endpoint
    print("Testing /predict endpoint...")
    predict_data = {"user_id": 1, "viewed_products": [1, 2, 3]}
    predict_stats = tester.run_load_test(
        endpoint=args.endpoint, num_requests=args.requests, concurrency=args.concurrency, method="POST", data=predict_data
    )
    tester.print_results(predict_stats)

    # Check if tests passed
    if health_stats["success_rate"] < 95 or predict_stats["success_rate"] < 95:
        print("❌ Load test failed: Success rate below 95%")
        sys.exit(1)

    if predict_stats["avg_response_time"] > 1.0:
        print("⚠️  Warning: Average response time exceeds 1 second")

    print("✅ Load test passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
