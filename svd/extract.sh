#!/usr/bin/env bash
for f in vendor/*.zip; do
    unzip -juLL $f '**.svd'
done

# Copy and rename H7 files to remove trailing 'x'
# and provide a second copy of the SVDs to modify
# for the revision-V hardware.
mv stm32h745_cm4.svd stm32h745cm4.svd
mv stm32h745_cm7.svd stm32h745cm7.svd
mv stm32h747_cm4.svd stm32h747cm4.svd
mv stm32h747_cm7.svd stm32h747cm7.svd
mv stm32h755_cm4.svd stm32h755cm4.svd
mv stm32h755_cm7.svd stm32h755cm7.svd
mv stm32h757_cm4.svd stm32h757cm4.svd
mv stm32h757_cm7.svd stm32h757cm7.svd
cp stm32h743.svd stm32h743v.svd
cp stm32h753.svd stm32h753v.svd

# Rename MP1 svd files to remove trailing 'x'
mv stm32mp157x.svd stm32mp157.svd
mv stm32mp153x.svd stm32mp153.svd

# Rename WLE5 file to remove _cm4, since it only has one core.
mv stm32wle5_cm4.svd stm32wle5.svd

mv stm32wb55_cm4.svd stm32wb55.svd
