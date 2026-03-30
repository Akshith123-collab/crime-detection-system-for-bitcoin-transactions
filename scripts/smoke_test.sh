#!/usr/bin/env bash
set -e

echo "===== Docker containers ====="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo
echo "===== Kafka topics ====="
docker exec aml-kafka kafka-topics --list --bootstrap-server localhost:9092 || true

echo
echo "===== Neo4j Browser ====="
echo "Open: http://localhost:7474"
echo "User: neo4j"
echo "Password: amlproject123"
