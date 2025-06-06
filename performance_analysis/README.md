# Performance Analysis

This directory contains scripts and configurations for load testing the RadarLivre system. The test suite includes simulators for collectors, aircraft, and web clients.

## Prerequisites

* Python 3.x
* Pandas, Scipy, Numpy and Requests (installed via pip)

## Installation

```bash
pip install requests pandas scipy numpy
```

## Components

### Aircraft Simulator
Simulates aircraft movement and generates ADS-B data:
- Calculates realistic flight paths
- Generates position, velocity, and altitude data
- Simulates vertical and horizontal movement

### Collector Simulator
Simulates ADS-B collectors:
- Sends periodic HELLO messages
- Generates and sends ADS-B data
- Can simulate both regular collectors and airport collectors
- Logs all actions and response times

### Web Client Simulator
Simulates web clients accessing the system:
- Polls collector status
- Requests flight information
- Monitors specific flights
- Simulates user interactions with the map

## Running Tests

### 1. Create Test Collectors
First, create the test collectors in the system:
```bash
./create_tests_collectors.sh
```

### 2. Run Collector Tests
Start the collector simulators. The argument is the number of collectors to simulate:
```bash
./run_test_collectors.sh <number_of_collectors>
```

Example:
```bash
./run_test_collectors.sh 10  # Simulates 10 collectors
```

### 3. Run Web Client Tests
Start the web client simulators. The argument is the number of web clients to simulate:
```bash
./run_test_web_clients.sh <number_of_clients>
```

Example:
```bash
./run_test_web_clients.sh 50  # Simulates 50 web clients
```

Note: The scripts will create PID files (`collector_pids.txt` and `web_clients_pids.txt`) to track the running processes.

## Managing Tests

### Server Configuration
The simulators are configured to connect to:
- Base URL: `http://localhost:8000/api`
- Default credentials: username="admin", password="123456"

If you need to change these settings, modify:
- `simulator_manager.py` for collector credentials and base URL
- `web_client_simulator.py` for the base URL

### Cleaning Logs
Before running new tests, clean the log files:
```bash
rm -f collectors_action.log web_clients_action.log
```

### Stopping Tests
To stop all running simulators, use the PID files:

1. Stop collector simulators:
```bash
kill $(cat collector_pids.txt)
rm collector_pids.txt
```

2. Stop web client simulators:
```bash
kill $(cat web_clients_pids.txt)
rm web_clients_pids.txt
```

### Restarting Tests
To run new tests:
1. Stop any running tests
2. Clean the log files
3. Run the tests again

## Logging

The tests generate two log files:
- `collectors_action.log`: Contains collector simulator actions and response times
- `web_clients_action.log`: Contains web client simulator actions and response times

## Analysis

Use the `analyze_log.py` script to analyze the test results:
```bash
python analyze_log.py
```

This will generate statistics about:
- Response times
- Success rates
- Error patterns
- System performance under load

## Customization

You can customize the test parameters in:
- `test_collectors_infos.csv`: Collector configurations
- `aircraft_simulator.py`: Aircraft behavior parameters
- `collector_simulator.py`: Collector behavior parameters
- `web_client_simulator.py`: Web client behavior parameters