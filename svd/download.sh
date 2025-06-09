#!/usr/bin/env bash
declare -a arr=(
    "stm32c0-svd"
    "stm32f0_svd"
    "stm32f1_svd"
    "stm32f2_svd"
    "stm32f3-svd"
    "stm32f4-svd"
    "stm32f7-svd"
    "stm32g0-svd"
    "stm32g4_svd"
    "stm32h5-svd"
    "stm32h7-svd"
    "stm32h7rs-svd"
    "stm32l0-svd"
    "stm32l1_svd"
    "stm32l4_svd"
    "stm32l4plus-svd"
    "stm32l5-svd"
    "stm32mp1-svd"
    "stm32u0-svd"
    "stm32u5_svd"
    "stm32wb_svd"
    "stm32wb0-svd"
    "stm32wba5-svd"
    "stm32wl-svd"
    "stm32wl3-svd"
)

for f in "${arr[@]}"
do
    wget -U "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)" https://www.st.com/resource/en/svd/$f.zip -O vendor/en.$f.zip
done
