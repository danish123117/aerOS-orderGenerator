import sys
import time
import random
import uuid
from datetime import datetime , timezone
import os
from ngsiOperations.ngsildOperations.ngsildCrudOperations import ngsi_patch

def patch_order(timestamp,orderQuantity,orderId,orion,orion_port,context, context_port):
    entity = "urn:ngsi-ld:extOrder:order001"
    data = {
        "timestamp": timestamp,
        "orderId": orderId,
        "orderQuantity": orderQuantity
    }
    status = ngsi_patch(data,entity,orion,orion_port,context, context_port)
    return status

 
m = 60
FREQ_MAP = {
    "Unconstrained": 10*m,
    "At Capacity": 7*m,
    "Over Loaded": 6*m
}

frequency = sys.argv[1] if len(sys.argv) > 1 else "At Capacity"
mean = FREQ_MAP.get(frequency, 7*m) 
# add normal distribution to the interval
std_dev = 2 * m  # Standard deviation of 2 minutes
interval = max(1, int(random.gauss(mean, std_dev)))  # Ensure interval is at least 1 second gaussian distribution of the interval

with open("orders.log", "w") as f:
    f.write("")  # Clear log on start

quantity = 1
orion = os.getenv("ORION_LD_HOST", 'localhost')
orion_port = int(os.getenv("ORION_LD_PORT", 1026))
context = os.getenv("CONTEXT_HOST", 'localhost')
context_port = int(os.getenv("CONTEXT_PORT", 5051))

while True:
    order_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-2]
    
    patch_status =patch_order(orderId=order_id,timestamp=timestamp,orderQuantity=1,orionUrl=f"{orion}:{orion_port}")
    status = "Success" if patch_status.status_code == 204 else "Failed"
    order = f"Order ID: {order_id},  Quantity: {quantity}, Timestamp: {timestamp}, Status: {status}"
    with open("orders.log", "a") as f:
        f.write(order + "\n")
    print(order)
    time.sleep(interval)
