set -euxo pipefail

NAME=$(svdtools info $1 device-name --input-format xml)
CRATE_PATH=$(echo $(basename $1) | sed -E 's|(\w*)\.svd\.patched|\1|g')
echo "html_url: https://stm32-rs.github.io/stm32-rs/${NAME}.html" > $2
echo "crate_path: crate::${CRATE_PATH}" >> $2
