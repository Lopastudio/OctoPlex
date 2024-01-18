#!/bin/bash

# Insert a new study group
curl -X POST -H "Content-Type: application/json" -d '{"table_name": "study_groups", "values": {"name": "Group A"}}' http://localhost:5000/api/insert

# Insert a new teacher
curl -X POST -H "Content-Type: application/json" -d '{"table_name": "teachers", "values": {"name": "John Doe"}}' http://localhost:5000/api/insert



