"""
Integration tests for Recommendation API
Branch: feature/api-development
"""

import pytest
import time
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)


class TestAPIIntegration:
    """Integration tests for API endpoints"""
    
    def test_health_check_available(self):
        """Test that health check endpoint is available"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_recommendation_flow(self):
        """Test complete recommendation flow"""
        # Test multiple users
        test_cases = [
            {"user_id": 1, "viewed_products": [1, 2, 3]},
            {"user_id": 2, "viewed_products": [10, 20]},
            {"user_id": 3, "viewed_products": [5, 15, 25]},
        ]
        
        for test_case in test_cases:
            response = client.post("/predict", json=test_case)
            assert response.status_code == 200
            data = response.json()
            assert "user_id" in data
            assert "recommendations" in data
            assert data["user_id"] == test_case["user_id"]
            assert isinstance(data["recommendations"], list)
    
    def test_concurrent_requests(self):
        """Test API handles concurrent requests"""
        import concurrent.futures
        
        def make_request():
            response = client.post("/predict", json={
                "user_id": 1,
                "viewed_products": [1, 2, 3]
            })
            return response.status_code == 200
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        assert all(results), "Some concurrent requests failed"
    
    def test_error_handling_invalid_payload(self):
        """Test API handles invalid payloads gracefully"""
        invalid_payloads = [
            {"invalid": "data"},
            {"user_id": "not_a_number"},
            {"user_id": 1},  # Missing viewed_products
            {"viewed_products": [1, 2, 3]},  # Missing user_id
        ]
        
        for payload in invalid_payloads:
            response = client.post("/predict", json=payload)
            # Should return error status (422 for validation error or 400 for bad request)
            assert response.status_code in [400, 422], \
                f"Expected error status for invalid payload: {payload}"
    
    def test_response_time(self):
        """Test API response time is acceptable"""
        start_time = time.time()
        response = client.post("/predict", json={
            "user_id": 1,
            "viewed_products": [1, 2, 3]
        })
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < 1.0, f"Response time too slow: {response_time}s"
    
    def test_docs_available(self):
        """Test API documentation is available"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()


class TestAPIDataValidation:
    """Test data validation in API"""
    
    def test_user_id_validation(self):
        """Test user_id validation"""
        # Valid user_id
        response = client.post("/predict", json={
            "user_id": 1,
            "viewed_products": [1, 2, 3]
        })
        assert response.status_code == 200
    
    def test_viewed_products_validation(self):
        """Test viewed_products validation"""
        # Valid viewed_products
        response = client.post("/predict", json={
            "user_id": 1,
            "viewed_products": [1, 2, 3, 4, 5]
        })
        assert response.status_code == 200
    
    def test_empty_viewed_products(self):
        """Test empty viewed_products list"""
        response = client.post("/predict", json={
            "user_id": 1,
            "viewed_products": []
        })
        # Should handle empty list gracefully
        assert response.status_code in [200, 400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
