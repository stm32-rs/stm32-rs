#!/usr/bin/env bash
for f in vendor/*.zip; do
    unzip -juLL $f '**.svd'
done

cp stm32h743x.svd stm32h743.svd
cp stm32h743x.svd stm32h743v.svd
cp stm32h753x.svd stm32h753.svd
cp stm32h753x.svd stm32h753v.svd
cp stm32h7x5_cm4.svd stm32h747cm4.svd
cp stm32h7x5_cm7.svd stm32h747cm7.svd
cp stm32h7b3x.svd stm32h7b3.svd
cp stm32mp157x.svd stm32mp157.svd
cp stm32g4a1xx.svd stm32g4a1.svd
cp stm32g431xx.svd stm32g431.svd
cp stm32g441xx.svd stm32g441.svd
cp stm32g471xx.svd stm32g471.svd
cp stm32g473xx.svd stm32g473.svd
cp stm32g474xx.svd stm32g474.svd
cp stm32g483xx.svd stm32g483.svd
cp stm32g484xx.svd stm32g484.svd
cp stm32g491xx.svd stm32g491.svd
