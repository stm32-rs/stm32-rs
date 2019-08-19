#!/usr/bin/env bash
for f in vendor/*.zip; do
    unzip -juLL $f '**.svd'
done

ln -s stm32h743x.svd stm32h743.svd || true
ln -s stm32h743x.svd stm32h743v.svd || true
ln -s stm32h753x.svd stm32h753.svd || true
ln -s stm32h753x.svd stm32h753v.svd || true
ln -s stm32h7x7_cm7.svd stm32h747cm7.svd || true
