import requests
import time

FETCH_URL = "http://localhost:8000/process_order?user_id=123&product_id=456&zip_code=12345"

def send_request():
    return requests.get(FETCH_URL)


def main():
    start_time = time.time()
    send_request()
    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f} seconds")

if __name__ ==  "__main__":
    main()
    
# $ python measure_single_task.py 
# Total time: 3.52 seconds