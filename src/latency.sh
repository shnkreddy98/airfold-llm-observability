#!/bin/bash

AUTH_TOKEN="aft_tTGkRNOPvjC7Oa9BflQlPaV3fy9.c37l3loJPDNAeUIQhi9zrI3ZrLx8TnHDz6IgbIdhwoz"

granularity=("minute" "hour" "day" "month")
apis=("latency_timeline" "requests_timeline" "tokens_pm" "total_values" "latency_timeline_mv" "requests_timeline_mv" "tokens_pm_mv" "total_values_mv")

for api in "${apis[@]}"; do
    for granular in "${granularity[@]}"; do
        url="https://api.us.airfold.co/v1/pipes/${api}.json?interval=default&granularity=${granular}"
        
        curl_output=$(curl -s -H "Authorization: Bearer $AUTH_TOKEN" "$url")
        
        curl_time_seconds=$(echo "$curl_output" | jq -r ".statistics.elapsed")
        rows=$(echo "$curl_output" | jq -r ".rows")
        rowsread=$(echo "$curl_output" | jq -r ".statistics.rows_read")
        bytesread=$(echo "$curl_output" | jq -r ".statistics.bytes_read")
        
        printf "%s | %s | %s | %s | %s | %s | %s \n" "$api" "$filter" "$granular" "$curl_time_seconds" "$rows" "$rowsread" "$bytesread"
    done
done