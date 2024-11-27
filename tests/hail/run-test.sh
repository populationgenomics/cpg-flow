#!/bin/bash

analysis-runner \
    --dataset "fewgenomes" \
    --description "cpg-flow_test" \
    --access-level "test" \
    --output-dir "cpg-flow_test" \
    --config "tests/hail/config.toml" \
    tests/hail/workflow.py
