#!/bin/bash
URL="http://100.76.206.82:9005/data.json"
count=10
fail=0
success=0
for i in $(seq 1 $count); do
    code=$(curl -s -o /dev/null -w "%{http_code}" $URL)
    if [ "$code" = "200" ]; then
        success=$((success+1))
    else
        fail=$((fail+1))
        echo "Request $i failed with HTTP $code"
    fi
    sleep 0.5
done
echo "Total requests: $count, Success: $success, Failures: $fail"