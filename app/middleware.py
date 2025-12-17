from fastapi.middleware import Middleware
from fastapi import Request
import time

async def calculate_process_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    print("\n" + "-" * 50)
    print(f"Método: {request.method}")
    print(f"Ruta: {request.url.path}")
    print(f"Status: {response.status_code}")
    print(f"Tiempo: {process_time:.3f}s")
    print("-" * 50)    
    return response


    
    