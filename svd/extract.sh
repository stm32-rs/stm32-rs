#!/bin/bash
for f in vendor/*.zip; do
    unzip -jLL $f '*.svd'
done
