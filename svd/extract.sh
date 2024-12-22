#!/usr/bin/env bash
for f in vendor/*.zip; do
    unzip -juLL $f '**.svd'
done

# Copy and rename H7 files to remove trailing 'x'
# and provide a second copy of the SVDs to modify
# for the revision-V hardware.
mv stm32h7a3x.svd stm32h7a3.svd
mv stm32h7b0x.svd stm32h7b0.svd
mv stm32h7b3x.svd stm32h7b3.svd
mv stm32h73x.svd stm32h735.svd
mv stm32h742x.svd stm32h742.svd
mv stm32h750x.svd stm32h750.svd
mv stm32h757_cm4.svd stm32h747cm4.svd
mv stm32h757_cm7.svd stm32h747cm7.svd
cp stm32h743.svd stm32h743v.svd
cp stm32h753.svd stm32h753v.svd

# Rename MP1 svd files to remove trailing 'x'
mv stm32mp157x.svd stm32mp157.svd
mv stm32mp153x.svd stm32mp153.svd

# Rename WLE5 file to remove _cm4, since it only has one core.
mv stm32wle5_cm4.svd stm32wle5.svd

# Copy L4X2 svd into L412; a 412 one doesn't exist.
# We handle its modified RTC register block in `devices/stm32l412.yaml`.
cp stm32l4x2.svd stm32l412.svd
