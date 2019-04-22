#!/usr/bin/env bash
set -euxo pipefail

mkdir html

mkdir html/stm32f
python3 scripts/htmlcomparesvd.py svd/stm32f{0x8,103,107,217,303,3x8,469,7x2,7x9}.svd.patched
sed -i 's#<table>#<p>Only a representative member of each family included; click to view entire family</p><table>#' html/index.html
sed -i 's#stm32f0x8#<a href="stm32f0/index.html">STM32F0x8</a>#' html/index.html
sed -i 's#stm32f103#<a href="stm32f1/index.html">STM32F103</a>#' html/index.html
sed -i 's#stm32f107#<a href="stm32f1/index.html">STM32F107</a>#' html/index.html
sed -i 's#stm32f217#<a href="stm32f2/index.html">STM32F217</a>#' html/index.html
sed -i 's#stm32f303#<a href="stm32f3/index.html">STM32F303</a>#' html/index.html
sed -i 's#stm32f3x8#<a href="stm32f3/index.html">STM32F3x8</a>#' html/index.html
sed -i 's#stm32f469#<a href="stm32f4/index.html">STM32F469</a>#' html/index.html
sed -i 's#stm32f7x2#<a href="stm32f7/index.html">STM32F7x2</a>#' html/index.html
sed -i 's#stm32f7x9#<a href="stm32f7/index.html">STM32F7x9</a>#' html/index.html
mv html/*.html html/stm32f

mkdir html/stm32f/stm32f0
python3 scripts/htmlcomparesvd.py svd/stm32f0*.svd.patched
mv html/*.html html/stm32f/stm32f0

mkdir html/stm32f/stm32f1
python3 scripts/htmlcomparesvd.py svd/stm32f1*.svd.patched
mv html/*.html html/stm32f/stm32f1

mkdir html/stm32f/stm32f2
python3 scripts/htmlcomparesvd.py svd/stm32f2*.svd.patched
mv html/*.html html/stm32f/stm32f2

mkdir html/stm32f/stm32f3
python3 scripts/htmlcomparesvd.py svd/stm32f3*.svd.patched
mv html/*.html html/stm32f/stm32f3

mkdir html/stm32f/stm32f4
python3 scripts/htmlcomparesvd.py svd/stm32f4*.svd.patched
mv html/*.html html/stm32f/stm32f4

mkdir html/stm32f/stm32f7
python3 scripts/htmlcomparesvd.py svd/stm32f7*.svd.patched
mv html/*.html html/stm32f/stm32f7

mkdir html/stm32l
python3 scripts/htmlcomparesvd.py svd/stm32l{0x3,162,4x6}.svd.patched
sed -i 's#<table>#<p>Only a representative member of each family included; click to view entire family<\/p><table>#' html/index.html
sed -i 's#stm32l0x3#<a href="stm32l0/index.html">STM32L0x3</a>#' html/index.html
sed -i 's#stm32l162#<a href="stm32l1/index.html">STM32L162</a>#' html/index.html
sed -i 's#stm32l4x6#<a href="stm32l4/index.html">STM32L4x6</a>#' html/index.html
mv html/*.html html/stm32l

mkdir html/stm32l/stm32l0
python3 scripts/htmlcomparesvd.py svd/stm32l0*.svd.patched
mv html/*.html html/stm32l/stm32l0

mkdir html/stm32l/stm32l1
python3 scripts/htmlcomparesvd.py svd/stm32l1*.svd.patched
mv html/*.html html/stm32l/stm32l1

mkdir html/stm32l/stm32l4
python3 scripts/htmlcomparesvd.py svd/stm32l4*.svd.patched
mv html/*.html html/stm32l/stm32l4

mkdir html/stm32h
python3 scripts/htmlcomparesvd.py svd/stm32h7x3.svd.patched
sed -i 's#<table>#<p>Only a representative member of each family included; click to view entire family</p><table>#' html/index.html
sed -i 's#stm32h7x3#<a href="stm32h7/index.html">STM32H7x3</a>#' html/index.html
mv html/*.html html/stm32h

mkdir html/stm32h/stm32h7
python3 scripts/htmlcomparesvd.py svd/stm32h7x3.svd.patched
mv html/*.html html/stm32h/stm32h7

cat > html/index.html <<EOF
<!DOCTYPE html>
<a href="stm32f/index.html">STM32F</a><br>
<a href="stm32l/index.html">STM32L</a><br>
<a href="stm32h/index.html">STM32H</a><br>
EOF
