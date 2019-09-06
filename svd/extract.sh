#!/usr/bin/env bash
for f in vendor/*.zip; do
    unzip -juLL $f '**.svd'
done

cp stm32h743x.svd stm32h743.svd
cp stm32h743x.svd stm32h743v.svd
cp stm32h753x.svd stm32h753.svd
cp stm32h753x.svd stm32h753v.svd
cp stm32h7x5_cm7.svd stm32h747cm7.svd
cp stm32h7x5_cm7.svd stm32h757cm7.svd
