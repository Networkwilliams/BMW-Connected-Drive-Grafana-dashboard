# BMW Connected Drive Grafana Dashboard

A Python-based API server that fetches vehicle data from BMW ConnectedDrive and exposes it for visualization in Grafana.

## Features

- Real-time BMW vehicle data integration via `bimmer_connected` library
- RESTful API endpoint for Grafana JSON datasource
- Automatic data caching and periodic updates (every 5 minutes)
- Docker support for easy deployment
- Mock API servers for testing without BMW credentials
- Pre-configured Grafana dashboard

## Vehicle Data Exposed

- **Vehicle Information**: Name, VIN, Model
- **Mileage**: Current odometer reading
- **Fuel Status**: Fuel percentage and range
- **Battery Status**: Battery percentage and electric range (for hybrid/electric vehicles)
- **Location**: GPS coordinates
- **Door Lock State**: Locked/unlocked status
- **Climate**: Climate control status
- **Charging Status**: Current charging state (for electric/hybrid vehicles)

## Prerequisites

- Python 3.11+
- BMW ConnectedDrive account
- Grafana instance with JSON API plugin
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Direct Python Installation

```bash
# Install required Python package
pip install bimmer_connected

# Configure credentials in bmw_api.py
# Edit lines 11-12 to add your BMW username and password
BMW_USERNAME = "your-username"
BMW_PASSWORD = "your-password"

# Run the API server
python3 bmw_api.py
```

### Option 2: Docker Installation

```bash
# Build the Docker image
docker build -f Dockerfile.bmw -t bmw-api .

# Run the container
docker run -d -p 8898:8898 \
  -e BMW_USERNAME="your-username" \
  -e BMW_PASSWORD="your-password" \
  bmw-api
```

## Configuration

Edit `bmw_api.py` and configure your BMW credentials:

```python
BMW_USERNAME = "your-username"  # Your BMW ConnectedDrive username
BMW_PASSWORD = "your-password"  # Your BMW ConnectedDrive password
BMW_REGION = Regions.REST_OF_WORLD  # Change if needed (Regions.NORTH_AMERICA, etc.)
```

## Usage

### Running the Real API

```bash
python3 bmw_api.py
```

The API will:
1. Fetch initial BMW vehicle data
2. Start HTTP server on port 8898
3. Update data every 5 minutes automatically

Access the API at: `http://localhost:8898`

### Running Mock API (for Testing)

For testing without BMW credentials:

```bash
# Mock API with kilometers
python3 bmw_mock_api.py

# Mock API with miles
python3 bmw_mock_api_miles.py
```

Both mock servers run on port 8898 and return sample vehicle data.

## Grafana Setup

### 1. Install JSON API Plugin

```bash
grafana-cli plugins install simpod-json-datasource
```

### 2. Add Data Source

1. Navigate to Configuration → Data Sources
2. Add new "JSON API" datasource
3. Set URL to: `http://localhost:8898` (or your server address)
4. Save & Test

### 3. Import Dashboard

1. Navigate to Dashboards → Import
2. Upload `bmw-dashboard.json`
3. Select your JSON API datasource
4. Import

## BMW ConnectedDrive Authentication

BMW ConnectedDrive uses hCaptcha for authentication. If you encounter authentication issues, use the `bmw_captcha_helper.py` script for guidance on obtaining the hCaptcha token.

```bash
python3 bmw_captcha_helper.py
```

Follow the displayed instructions to extract the hCaptcha token from your browser's developer tools.

## API Response Format

```json
{
  "status": "success",
  "vehicles": [
    {
      "name": "My BMW",
      "vin": "WBA1234567890",
      "model": "COMBUSTION",
      "mileage": 45678,
      "mileage_unit": "km",
      "fuel_percent": 67,
      "fuel_range": 420,
      "fuel_range_unit": "km",
      "battery_percent": 85,
      "electric_range": 45,
      "electric_range_unit": "km",
      "latitude": 51.5074,
      "longitude": -0.1278,
      "door_lock_state": "LOCKED",
      "climate_on": false,
      "charging_status": "NOT_CHARGING",
      "last_updated": "2024-02-27T01:23:45"
    }
  ],
  "timestamp": 1709001825.123
}
```

## Troubleshooting

### Authentication Failed

- Verify your BMW ConnectedDrive credentials
- Check if your account has access to BMW ConnectedDrive services
- Try the captcha helper script for token generation

### No Data Returned

- Ensure your BMW vehicle is connected to ConnectedDrive
- Check that your vehicle's data is visible in the official BMW app
- Review API server logs for errors

### Connection Timeout

- Increase the cache update interval in `bmw_api.py` (line 100)
- Check your network connection
- Verify BMW ConnectedDrive service status

## File Structure

- `bmw_api.py` - Main API server with BMW ConnectedDrive integration
- `bmw_mock_api.py` - Mock API server (kilometers)
- `bmw_mock_api_miles.py` - Mock API server (miles)
- `bmw_captcha_helper.py` - Helper script for authentication
- `bmw-dashboard.json` - Grafana dashboard configuration
- `Dockerfile.bmw` - Docker container configuration

## License

This project is provided as-is for personal use with BMW ConnectedDrive services.

## Credits

Built using the excellent [bimmer_connected](https://github.com/bimmerconnected/bimmer_connected) library.
