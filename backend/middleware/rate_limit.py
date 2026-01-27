from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from collections import defaultdict

# Simple in-memory rate limiter (use Redis in production)
request_counts = defaultdict(list)

def rate_limit(max_requests: int = 10, window_seconds: int = 60):
    """Rate limiting middleware"""
    async def limiter(request: Request):
        client_ip = request.client.host
        now = datetime.now()
        
        # Clean old requests
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if now - req_time < timedelta(seconds=window_seconds)
        ]
        
        # Check rate limit
        if len(request_counts[client_ip]) >= max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds"
            )
        
        # Add current request
        request_counts[client_ip].append(now)
        
    return limiter
