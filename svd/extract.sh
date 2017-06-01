#!/bin/bash
for f in vendor/*.zip; do
    unzip -j $f '*.svd'
done
rename 'y/A-Z/a-z/' *.svd
