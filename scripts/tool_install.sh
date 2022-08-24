#!/usr/bin/env bash

FORM_VERSION="${FORM_VERSION:-v0.10.0}"
SVDTOOLS_VERSION="${SVDTOOLS_VERSION:-v0.2.6}"
SVD2RUST_VERSION="${SVD2RUST_VERSION:-v0.25.1}"

case $1 in
    form)
        if [ $2 ]; then
            form=$2
        else
            form=$FORM_VERSION
        fi
        ;;
    svdtools)
        if [ $2 ]; then
            svdtools=$2
        else
            svdtools=$SVDTOOLS_VERSION
        fi
        ;;
    svd2rust)
        if [ $2 ]; then
            svd2rust=$2
        else
            svd2rust=$SVD2RUST_VERSION
        fi
        ;;
    *)
        form=$FORM_VERSION
        svdtools=$SVDTOOLS_VERSION
        svd2rust=$SVD2RUST_VERSION
        echo "Install default versions"
        ;;
esac

if [ $form ]; then
    echo "form = ${form}"
    curl -L https://github.com/djmcgill/form/releases/download/$form/form-x86_64-unknown-linux-gnu.gz | gzip -d - > ~/.cargo/bin/form
    chmod +x ~/.cargo/bin/form
fi
if [ $svdtools ]; then
    echo "svdtools = ${svdtools}"
    curl -L https://github.com/stm32-rs/svdtools/releases/download/$svdtools/svdtools-x86_64-unknown-linux-gnu.gz | gzip -d - > ~/.cargo/bin/svdtools
    chmod +x ~/.cargo/bin/svdtools
fi
if [ $svd2rust ]; then
    echo "svd2rust = ${svd2rust}"
    curl -L https://github.com/rust-embedded/svd2rust/releases/download/$svd2rust/svd2rust-x86_64-unknown-linux-gnu.gz | gzip -d - > ~/.cargo/bin/svd2rust
    chmod +x ~/.cargo/bin/svd2rust
fi
