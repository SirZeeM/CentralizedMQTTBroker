#!/bin/bash

# Create main project directory
mkdir -p mqtt-project
cd mqtt-project

# Create package directories
for dir in mqtt-broker mqtt-network mqtt-protocol mqtt-storage mqtt-auth mqtt-common; do
    mkdir -p $dir/{src,tests}
    mkdir -p $dir/src/${dir//-/_}
    touch $dir/src/${dir//-/_}/__init__.py
    touch $dir/tests/__init__.py
done

# Create docker directory
mkdir -p docker

# Create initial files
touch docker/Dockerfile.broker
touch docker/docker-compose.yml

# Create pyproject.toml files
for dir in mqtt-broker mqtt-network mqtt-protocol mqtt-storage mqtt-auth mqtt-common; do
    touch $dir/pyproject.toml
done

# Create README.md
echo "# MQTT Project" > README.md

