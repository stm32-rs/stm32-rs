#!/usr/bin/env bash

set -euo pipefail

CARGO_HOME="${CARGO_HOME:-$HOME/.cargo/}"

FORM_VERSION="${FORM_VERSION:-v0.10.0}"
SVDTOOLS_VERSION="${SVDTOOLS_VERSION:-v0.3.10}"
SVD2RUST_VERSION="${SVD2RUST_VERSION:-v0.32.0}"
SVDCONV_VERSION="${SVDCONV_VERSION:-3.3.46}"

case "${1:-}" in
    form)
        form="${2:-$FORM_VERSION}"
        ;;
    svdtools)
        svdtools="${2:-$SVDTOOLS_VERSION}"
        ;;
    svd2rust)
        svd2rust="${2:-$SVD2RUST_VERSION}"
        ;;
    svdconv)
        svdconv="${2:-$SVDCONV_VERSION}"
        ;;
    *)
        form=$FORM_VERSION
        svdtools=$SVDTOOLS_VERSION
        svd2rust=$SVD2RUST_VERSION
        svdconv=$SVDCONV_VERSION
        echo "Install default versions"
        ;;
esac

if [ "${form:-}" ]; then
    echo "form = ${form}"
    curl -sSfL https://github.com/djmcgill/form/releases/download/$form/form-x86_64-unknown-linux-gnu.gz | gzip -d - > $CARGO_HOME/bin/form
    chmod +x $CARGO_HOME/bin/form
fi

if [ "${svdtools:-}" ]; then
    echo "svdtools = ${svdtools}"
    curl -sSfL https://github.com/stm32-rs/svdtools/releases/download/$svdtools/svdtools-x86_64-unknown-linux-gnu.gz | gzip -d - > $CARGO_HOME/bin/svdtools
    chmod +x $CARGO_HOME/bin/svdtools
fi

if [ "${svd2rust:-}" ]; then
    echo "svd2rust = ${svd2rust}"
    curl -sSfL https://github.com/rust-embedded/svd2rust/releases/download/$svd2rust/svd2rust-x86_64-unknown-linux-gnu.gz | gzip -d - > $CARGO_HOME/bin/svd2rust
    chmod +x $CARGO_HOME/bin/svd2rust
fi

if [ "${svdconv:-}" ]; then
    echo "svdconv = ${svdconv}"
    curl -sSfL https://github.com/Open-CMSIS-Pack/devtools/releases/download/tools/svdconv/$svdconv/svdconv-$svdconv-linux-amd64.tbz2 | tar -xj -C $CARGO_HOME/bin/
    chmod +x $CARGO_HOME/bin/svdconv
fi
