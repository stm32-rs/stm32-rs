#!/usr/bin/env bash
set -euxo pipefail

mkdir -p html/stm32f
python3 scripts/htmlcomparesvd.py html/stm32f svd/stm32f{0x8,103,107,217,303,3x4,469,7x9}.svd.patched
sed -i 's#<table>#<p>Only a representative member of each family included; click to view entire family</p><table>#' html/stm32f/index.html
sed -i 's#stm32f0x8#<a href="stm32f0/index.html">STM32F0x8</a>#' html/stm32f/index.html
sed -i 's#stm32f103#<a href="stm32f1/index.html">STM32F103</a>#' html/stm32f/index.html
sed -i 's#stm32f107#<a href="stm32f1/index.html">STM32F107</a>#' html/stm32f/index.html
sed -i 's#stm32f217#<a href="stm32f2/index.html">STM32F217</a>#' html/stm32f/index.html
sed -i 's#stm32f303#<a href="stm32f3/index.html">STM32F303</a>#' html/stm32f/index.html
sed -i 's#stm32f3x4#<a href="stm32f3/index.html">STM32F3x4</a>#' html/stm32f/index.html
sed -i 's#stm32f469#<a href="stm32f4/index.html">STM32F469</a>#' html/stm32f/index.html
sed -i 's#stm32f7x9#<a href="stm32f7/index.html">STM32F7x9</a>#' html/stm32f/index.html

mkdir -p html/stm32f/stm32f0
python3 scripts/htmlcomparesvd.py html/stm32f/stm32f0 svd/stm32f0*.svd.patched

mkdir -p html/stm32f/stm32f1
python3 scripts/htmlcomparesvd.py html/stm32f/stm32f1 svd/stm32f1*.svd.patched

mkdir -p html/stm32f/stm32f2
python3 scripts/htmlcomparesvd.py html/stm32f/stm32f2 svd/stm32f2*.svd.patched

mkdir -p html/stm32f/stm32f3
python3 scripts/htmlcomparesvd.py html/stm32f/stm32f3 svd/stm32f3*.svd.patched

mkdir -p html/stm32f/stm32f4
python3 scripts/htmlcomparesvd.py html/stm32f/stm32f4 svd/stm32f4*.svd.patched

mkdir -p html/stm32f/stm32f7
python3 scripts/htmlcomparesvd.py html/stm32f/stm32f7 svd/stm32f7{x2,x3,30,45,50,x6,65,x7,x9}.svd.patched

mkdir -p html/stm32l
python3 scripts/htmlcomparesvd.py html/stm32l svd/stm32l{0x3,162,4x6}.svd.patched
sed -i 's#<table>#<p>Only a representative member of each family included; click to view entire family<\/p><table>#' html/stm32l/index.html
sed -i 's#stm32l0x3#<a href="stm32l0/index.html">STM32L0x3</a>#' html/stm32l/index.html
sed -i 's#stm32l162#<a href="stm32l1/index.html">STM32L162</a>#' html/stm32l/index.html
sed -i 's#stm32l4x6#<a href="stm32l4/index.html">STM32L4x6</a>#' html/stm32l/index.html

mkdir -p html/stm32l/stm32l0
python3 scripts/htmlcomparesvd.py html/stm32l/stm32l0 svd/stm32l0*.svd.patched

mkdir -p html/stm32l/stm32l1
python3 scripts/htmlcomparesvd.py html/stm32l/stm32l1 svd/stm32l1*.svd.patched

mkdir -p html/stm32l/stm32l4
python3 scripts/htmlcomparesvd.py html/stm32l/stm32l4 svd/stm32l4*.svd.patched

mkdir -p html/stm32h
python3 scripts/htmlcomparesvd.py html/stm32h svd/stm32h753.svd.patched
sed -i 's#<table>#<p>Only a representative member of each family included; click to view entire family</p><table>#' html/stm32h/index.html
sed -i 's#stm32h753#<a href="stm32h7/index.html">STM32H753</a>#' html/stm32h/index.html

mkdir -p html/stm32h/stm32h7
python3 scripts/htmlcomparesvd.py html/stm32h/stm32h7 svd/stm32h7*.svd.patched

cat > html/comparisons.html <<EOF
<!DOCTYPE html>
<head>
<meta charset="utf-8">
<meta name=viewport content="width=device-width, initial-scale=1">
<title>stm32-rs Peripheral Comparisons</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
</head>

<body>
<nav class="navbar navbar-inverse">
  <div class="container">
    <div class="navbar-header">
      <a class="navbar-brand" href="index.html">stm32-rs Device Coverage</a>
    </div>
    <div class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">Peripheral Comparisons</a></li>
      </ul>
    </div>
  </div>
</nav>

<h1>Device families</h1>
<ul>
  <li><a href="stm32f/index.html">STM32F</a></li>
  <li><a href="stm32l/index.html">STM32L</a></li>
  <li><a href="stm32h/index.html">STM32H</a></li>
</ul>
</body>
</html>
EOF
