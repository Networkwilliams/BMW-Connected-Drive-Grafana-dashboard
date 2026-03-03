#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class BMWMockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Mock BMW vehicle data
        mock_data = {
            "status": "success",
            "vehicles": [
                {
                    "name": "My BMW",
                    "vin": "WBA1234567890DEMO",
                    "model": "COMBUSTION",
                    "mileage": 45678,
                    "mileage_unit": "km",
                    "fuel_percent": 67,
                    "fuel_range": 420,
                    "fuel_range_unit": "km",
                    "door_lock_state": "LOCKED",
                    "climate_on": False,
                    "last_updated": str(time.time())
                }
            ],
            "timestamp": time.time()
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(mock_data).encode())

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8898), BMWMockHandler)
    print("Mock BMW API running on port 8898")
    server.serve_forever()
