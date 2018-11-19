#!/usr/bin/env bash
curl -kv -H "Content-Type: application/json" -H "sensor_token: token_mq135" -XPOST https://127.0.0.1/write --data '{"data_type":"temperature","value": 3.1}'