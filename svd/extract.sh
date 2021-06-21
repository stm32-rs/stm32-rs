#!/usr/bin/env bash
for f in vendor/*.zip; do
    unzip -juLL $f '**.svd'
done

# Copy and rename H7 files to remove trailing 'x'
# and provide a second copy of the SVDs to modify
# for the revision-V hardware.
cp stm32h743x.svd stm32h743.svd
mv stm32h743x.svd stm32h743v.svd
cp stm32h753x.svd stm32h753.svd
mv stm32h753x.svd stm32h753v.svd
mv stm32h7x5_cm4.svd stm32h747cm4.svd
mv stm32h7x5_cm7.svd stm32h747cm7.svd
mv stm32h7b3x.svd stm32h7b3.svd

# Rename MP1 svd files to remove trailing 'x'
mv stm32mp157x.svd stm32mp157.svd

# Rename G4 svd files to remove trailing 'xx'
mv stm32g4a1xx.svd stm32g4a1.svd
mv stm32g431xx.svd stm32g431.svd
mv stm32g441xx.svd stm32g441.svd
mv stm32g471xx.svd stm32g471.svd
mv stm32g473xx.svd stm32g473.svd
mv stm32g474xx.svd stm32g474.svd
mv stm32g483xx.svd stm32g483.svd
mv stm32g484xx.svd stm32g484.svd
mv stm32g491xx.svd stm32g491.svd

# Rename WLE5 file to remove _cm4, since it only has one core.
mv stm32wle5_cm4.svd stm32wle5.svd

# Copy L4X2 svd into L412; a 412 one doesn't exist.
# We handle its modified RTC register block in `devices/stm32l412.yaml`.
cp stm32l4x2.svd stm32l412.svd