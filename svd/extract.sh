#!/bin/bash
for f in vendor/*.zip; do
    unzip -juLL $f '*.svd'
done
