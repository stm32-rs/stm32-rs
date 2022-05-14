#!/usr/bin/env bash

if [ $FORM_VERSION ]; then
    curl -L https://github.com/djmcgill/form/releases/download/$FORM_VERSION/form-x86_64-unknown-linux-gnu.gz | gzip -d - > ~/.cargo/bin/form
    chmod +x ~/.cargo/bin/form
fi
if [ $SVDTOOLS_VERSION ]; then
    curl -L https://github.com/stm32-rs/svdtools/releases/download/$SVDTOOLS_VERSION/svdtools-x86_64-unknown-linux-gnu.gz | gzip -d - > ~/.cargo/bin/svdtools
    chmod +x ~/.cargo/bin/svdtools
fi
if [ $SVD2RUST_VERSION ]; then
    curl -L https://github.com/rust-embedded/svd2rust/releases/download/$SVD2RUST_VERSION/svd2rust-x86_64-unknown-linux-gnu.gz | gzip -d - > ~/.cargo/bin/svd2rust
    chmod +x ~/.cargo/bin/svd2rust
fi
