#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to cleanup on exit
cleanup() {
    echo -e "\n${GREEN}Shutting down services...${NC}"
    
    # Kill the backend server
    if [ ! -z "$BACKEND_PID" ]; then
        echo "Stopping backend server..."
        kill $BACKEND_PID 2>/dev/null
        wait $BACKEND_PID 2>/dev/null
    fi
    
    # Stop Docker containers
    echo "Stopping Docker containers..."
    docker-compose down
    
    echo -e "${GREEN}All services stopped.${NC}"
    exit 0
}

# Trap signals to ensure cleanup
trap cleanup EXIT INT TERM

# Start Docker containers
echo -e "${GREEN}Starting Docker containers...${NC}"
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 5

# Test database connection
echo "Testing database connection..."
pixi run test-db
if [ $? -ne 0 ]; then
    echo -e "${RED}Database connection failed!${NC}"
    exit 1
fi

# Start backend server
echo -e "${GREEN}Starting backend server...${NC}"
pixi run backend-dev &
BACKEND_PID=$!

# Give the server time to start
sleep 2

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}Backend server failed to start!${NC}"
    exit 1
fi

echo -e "${GREEN}Services are running!${NC}"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo -e "\nPress ${GREEN}Enter${NC} to stop all services..."

# Wait for user input
read -r

# Cleanup will be called automatically due to trap