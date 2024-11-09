#!/bin/bash

declare -a libraries=(
    "vanilla:latest:['vue']"
    "oku-ui:latest:['@oku-ui/primitives']"
    "vuetify:latest:['vuetify']"
    "ant-design-vue:latest:['ant-design-vue']"
    "radix-ui:latest:['@radix-ui/vue']"
    "element-plus:latest:['element-plus']"
    "reka-ui:1.0.0-alpha.5:['reka-ui']"
    "naive-ui:latest:['naive-ui']"
    "quasar:latest:['quasar']"
    "vant:latest:['vant']"
    "radix-ui:latest:['radix-ui']"
    "bootstrap-vue-next:latest:['bootstrap-vue-next']"
    "anu-vue:latest:['anu-vue']"
)

RESULT_FILE="temp/performance_results.tsv"

rm -rf temp
mkdir -p temp

cleanup() {
    pkill -f "start.ts"
    pkill -f "tsx"
    sync
    echo 3 > /proc/sys/vm/drop_caches
}

trap cleanup EXIT

> "$RESULT_FILE"

for library_info in "${libraries[@]}"; do
    cleanup
    
    sleep 10

    IFS=':' read -r library_name library_version library_deps <<< "$library_info"
    
    start_time=$(date +%s.%N)
    
    tsx start.ts "$library_name" "$library_version" "$library_deps"
    
    end_time=$(date +%s.%N)
    
    duration=$(echo "$end_time - $start_time" | bc)
    
    echo -e "$library_name\t$duration" >> "$RESULT_FILE"
    
    sleep 10

    echo "---------------------------------"
done

cat "$RESULT_FILE"