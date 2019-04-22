#!/usr/bin/env bash

which svd2rust >/dev/null
if [ $? -ne 0 ]
then
    cargo install --version $1 svd2rust
else
    ver=$(svd2rust -V | cut -d' ' -f2)
    if [ "$ver" != "$1" ]
    then
        cargo install --force --version $1 svd2rust
    fi
fi


