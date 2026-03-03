#!/usr/bin/env python3
import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from bimmer_connected.account import MyBMWAccount
from bimmer_connected.api.regions import Regions
import threading
import time

# BMW credentials
BMW_USERNAME = ""
BMW_PASSWORD = ""
BMW_REGION = Regions.REST_OF_WORLD

# Cache for BMW data
bmw_data_cache = {}
cache_lock = threading.Lock()

async def fetch_bmw_data():
    """Fetch BMW vehicle data"""
    try:
        account = MyBMWAccount(BMW_USERNAME, BMW_PASSWORD, BMW_REGION)
        await account.get_vehicles()

        vehicles_data = []
        for vehicle in account.vehicles:
            vehicle_info = {
                "name": vehicle.name,
                "vin": vehicle.vin,
                "model": vehicle.drive_train.name if hasattr(vehicle, 'drive_train') else "Unknown",
                "mileage": vehicle.mileage.value if hasattr(vehicle, 'mileage') and vehicle.mileage else 0,
                "mileage_unit": vehicle.mileage.unit if hasattr(vehicle, 'mileage') and vehicle.mileage else "km",
            }

            # Fuel data
            if hasattr(vehicle, 'fuel_and_battery'):
                if hasattr(vehicle.fuel_and_battery, 'remaining_fuel_percent'):
                    vehicle_info['fuel_percent'] = vehicle.fuel_and_battery.remaining_fuel_percent
                if hasattr(vehicle.fuel_and_battery, 'remaining_range_fuel'):
                    vehicle_info['fuel_range'] = vehicle.fuel_and_battery.remaining_range_fuel.value if vehicle.fuel_and_battery.remaining_range_fuel else 0
                    vehicle_info['fuel_range_unit'] = vehicle.fuel_and_battery.remaining_range_fuel.unit if vehicle.fuel_and_battery.remaining_range_fuel else "km"
                if hasattr(vehicle.fuel_and_battery, 'remaining_battery_percent'):
                    vehicle_info['battery_percent'] = vehicle.fuel_and_battery.remaining_battery_percent
                if hasattr(vehicle.fuel_and_battery, 'remaining_range_electric'):
                    vehicle_info['electric_range'] = vehicle.fuel_and_battery.remaining_range_electric.value if vehicle.fuel_and_battery.remaining_range_electric else 0
                    vehicle_info['electric_range_unit'] = vehicle.fuel_and_battery.remaining_range_electric.unit if vehicle.fuel_and_battery.remaining_range_electric else "km"

            # Location
            if hasattr(vehicle, 'vehicle_location') and vehicle.vehicle_location:
                if hasattr(vehicle.vehicle_location, 'location'):
                    vehicle_info['latitude'] = vehicle.vehicle_location.location.latitude
                    vehicle_info['longitude'] = vehicle.vehicle_location.location.longitude

            # Door lock state
            if hasattr(vehicle, 'doors_and_windows'):
                if hasattr(vehicle.doors_and_windows, 'door_lock_state'):
                    vehicle_info['door_lock_state'] = str(vehicle.doors_and_windows.door_lock_state)

            # Climate
            if hasattr(vehicle, 'climate'):
                if hasattr(vehicle.climate, 'is_climate_on'):
                    vehicle_info['climate_on'] = vehicle.climate.is_climate_on

            # Charging status (for electric/hybrid)
            if hasattr(vehicle, 'fuel_and_battery'):
                if hasattr(vehicle.fuel_and_battery, 'charging_status'):
                    vehicle_info['charging_status'] = str(vehicle.fuel_and_battery.charging_status)

            # Last updated
            if hasattr(vehicle, 'data') and hasattr(vehicle.data, 'attributes'):
                if hasattr(vehicle.data.attributes, 'updateTime_converted_timestamp'):
                    vehicle_info['last_updated'] = str(vehicle.data.attributes.updateTime_converted_timestamp)

            vehicles_data.append(vehicle_info)

        return {"status": "success", "vehicles": vehicles_data, "timestamp": time.time()}
    except Exception as e:
        return {"status": "error", "error": str(e), "timestamp": time.time()}

def update_cache_periodically():
    """Update BMW data cache every 5 minutes"""
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data = loop.run_until_complete(fetch_bmw_data())
            loop.close()

            with cache_lock:
                global bmw_data_cache
                bmw_data_cache = data

            print(f"BMW data updated: {data.get('status')}")
        except Exception as e:
            print(f"Error updating BMW data: {e}")
            with cache_lock:
                bmw_data_cache = {"status": "error", "error": str(e), "timestamp": time.time()}

        # Wait 5 minutes before next update
        time.sleep(300)

class BMWAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with cache_lock:
            data = bmw_data_cache.copy()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    # Start cache updater thread
    cache_thread = threading.Thread(target=update_cache_periodically, daemon=True)
    cache_thread.start()

    # Initial fetch
    print("Fetching initial BMW data...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bmw_data_cache = loop.run_until_complete(fetch_bmw_data())
    loop.close()
    print(f"Initial fetch complete: {bmw_data_cache.get('status')}")

    # Start HTTP server
    server = HTTPServer(('0.0.0.0', 8898), BMWAPIHandler)
    print("BMW API running on port 8898")
    server.serve_forever()
