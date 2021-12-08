# STM32 Peripheral Access Crates

[![CI](https://github.com/stm32-rs/stm32-rs/workflows/CI/badge.svg?branch=master)](https://github.com/stm32-rs/stm32-rs)
[![crates.io](https://img.shields.io/crates/v/stm32f0.svg?label=stm32f0)](https://crates.io/crates/stm32f0)
[![crates.io](https://img.shields.io/crates/v/stm32f1.svg?label=stm32f1)](https://crates.io/crates/stm32f1)
[![crates.io](https://img.shields.io/crates/v/stm32f2.svg?label=stm32f2)](https://crates.io/crates/stm32f2)
[![crates.io](https://img.shields.io/crates/v/stm32f3.svg?label=stm32f3)](https://crates.io/crates/stm32f3)
[![crates.io](https://img.shields.io/crates/v/stm32f4.svg?label=stm32f4)](https://crates.io/crates/stm32f4)
[![crates.io](https://img.shields.io/crates/v/stm32f7.svg?label=stm32f7)](https://crates.io/crates/stm32f7)
[![crates.io](https://img.shields.io/crates/v/stm32g0.svg?label=stm32g0)](https://crates.io/crates/stm32g0)
[![crates.io](https://img.shields.io/crates/v/stm32g4.svg?label=stm32g4)](https://crates.io/crates/stm32g4)
[![crates.io](https://img.shields.io/crates/v/stm32h7.svg?label=stm32h7)](https://crates.io/crates/stm32h7)
[![crates.io](https://img.shields.io/crates/v/stm32l0.svg?label=stm32l0)](https://crates.io/crates/stm32l0)
[![crates.io](https://img.shields.io/crates/v/stm32l1.svg?label=stm32l1)](https://crates.io/crates/stm32l1)
[![crates.io](https://img.shields.io/crates/v/stm32l4.svg?label=stm32l4)](https://crates.io/crates/stm32l4)
[![crates.io](https://img.shields.io/crates/v/stm32l5.svg?label=stm32l5)](https://crates.io/crates/stm32l5)
[![crates.io](https://img.shields.io/crates/v/stm32mp1.svg?label=stm32mp1)](https://crates.io/crates/stm32mp1)
[![crates.io](https://img.shields.io/crates/v/stm32wl.svg?label=stm32wl)](https://crates.io/crates/stm32wl)
[![crates.io](https://img.shields.io/crates/v/stm32wb.svg?label=stm32wb)](https://crates.io/crates/stm32wb)
[![Matrix](https://img.shields.io/matrix/stm32-rs:matrix.org)](https://matrix.to/#/#stm32-rs:matrix.org)

This repository provides Rust device support crates for all STM32
microcontrollers, providing a safe API to that device's peripherals using
[svd2rust] and a community-built collection of patches to the basic SVD files.
There is one crate per device family, and each supported device is a
feature-gated module in that crate. These crates are commonly known as
peripheral access crates or "PACs".

[svd2rust]: https://github.com/rust-embedded/svd2rust

To view the generated code that makes up each crate, visit the
[stm32-rs-nightlies](https://github.com/stm32-rs/stm32-rs-nightlies)
repository, which is automatically rebuilt on every commit to stm32-rs master.
The stm32-rs repository contains the patches to the underlying SVD files and
the tooling to generate the crates.

While these crates are widely used, not every register of every device will
have been tested on hardware, and so errors or omissions may remain. We can't
make any guarantee of correctness. Please report any bugs you find!

You can see current coverage status for each chip
[here](https://stm32-rs.github.io/stm32-rs/). Coverage means that individual fields are
documented with possible values, but even devices with low coverage should
have every register and field available in the API. That page also allows you
to drill down into each field on each register on each peripheral.

## Using Device Crates In Your Own Project

In your own project's `Cargo.toml`:
```toml
[dependencies.stm32f4]
version = "0.14.0"
features = ["stm32f405", "rt"]
```

The `rt` feature is optional but helpful. See
[svd2rust](https://docs.rs/svd2rust/latest/svd2rust/#the-rt-feature) for
details.

Then, in your code:

```rust
use stm32f4::stm32f405;

let mut peripherals = stm32f405::Peripherals::take().unwrap();
```

Refer to `svd2rust` [documentation](https://docs.rs/svd2rust) for further usage.

Replace `stm32f4` and `stm32f405` with your own device; see the individual
crate READMEs for the complete list of supported devices. All current STM32
devices should be supported to some level.

## Using Latest "Nightly" Builds

Whenever the master branch of this repository is updated, all device crates are
built and deployed to the
[stm32-rs-nightlies](https://github.com/stm32-rs/stm32-rs-nightlies)
repository. You can use this in your `Cargo.toml`:

```toml
[dependencies.stm32f4]
git = "https://github.com/stm32-rs/stm32-rs-nightlies"
features = ["stm32f405", "rt"]
```

The nightlies should always build and be as stable as the latest release, but
contain the latest patches and updates.


## Generating Device Crates / Building Locally

* Install `svd2rust`: `cargo install --version 0.20.0 svd2rust`
* Install `form`: `cargo install form`
* Install rustfmt: `rustup component add rustfmt`
* Install svdtools: `pip install --user svdtools`
* Unzip bundled SVD zip files: `cd svd; ./extract.sh; cd ..`
* Generate patched SVD files: `make patch` (you probably want `-j` for all `make` invocations)
* Generate svd2rust device crates: `make svd2rust`
* Optional: Format device crates: `make form`

## Motivation and Objectives

This project serves two purposes:

* Create a source of high-quality STM32 SVD files, with manufacturer errors
  and inconsistencies fixed. These files could be used with svd2rust or other
  tools, or in other projects. They should hopefully be useful in their own
  right.
* Create and publish svd2rust-generated crates covering all STM32s, using
  the SVD files.

When this project began, many individual crates existed for specific STM32
devices, typically maintained separately with hand-edited updates to the SVD
files. This project hopes to reduce that duplication of effort and centralise
the community's STM32 device support in one place.

## Helping

This project is still young and there's a lot to do!

* More peripheral patches need to be written, most of all. See what we've got
  in `peripherals/` and grab a reference manual!
* Also everything needs testing, and you can't so easily automate finding bugs
  in the SVD files...

## Supported Device Families

[![crates.io](https://img.shields.io/crates/v/stm32f0.svg?label=stm32f0)](https://crates.io/crates/stm32f0)
[![crates.io](https://img.shields.io/crates/v/stm32f1.svg?label=stm32f1)](https://crates.io/crates/stm32f1)
[![crates.io](https://img.shields.io/crates/v/stm32f2.svg?label=stm32f2)](https://crates.io/crates/stm32f2)
[![crates.io](https://img.shields.io/crates/v/stm32f3.svg?label=stm32f3)](https://crates.io/crates/stm32f3)
[![crates.io](https://img.shields.io/crates/v/stm32f4.svg?label=stm32f4)](https://crates.io/crates/stm32f4)
[![crates.io](https://img.shields.io/crates/v/stm32f7.svg?label=stm32f7)](https://crates.io/crates/stm32f7)
[![crates.io](https://img.shields.io/crates/v/stm32g0.svg?label=stm32g0)](https://crates.io/crates/stm32g0)
[![crates.io](https://img.shields.io/crates/v/stm32g4.svg?label=stm32g4)](https://crates.io/crates/stm32g4)
[![crates.io](https://img.shields.io/crates/v/stm32h7.svg?label=stm32h7)](https://crates.io/crates/stm32h7)
[![crates.io](https://img.shields.io/crates/v/stm32l0.svg?label=stm32l0)](https://crates.io/crates/stm32l0)
[![crates.io](https://img.shields.io/crates/v/stm32l1.svg?label=stm32l1)](https://crates.io/crates/stm32l1)
[![crates.io](https://img.shields.io/crates/v/stm32l4.svg?label=stm32l4)](https://crates.io/crates/stm32l4)
[![crates.io](https://img.shields.io/crates/v/stm32l5.svg?label=stm32l5)](https://crates.io/crates/stm32l5)
[![crates.io](https://img.shields.io/crates/v/stm32mp1.svg?label=stm32mp1)](https://crates.io/crates/stm32mp1)
[![crates.io](https://img.shields.io/crates/v/stm32wl.svg?label=stm32wl)](https://crates.io/crates/stm32wl)
[![crates.io](https://img.shields.io/crates/v/stm32wb.svg?label=stm32wb)](https://crates.io/crates/stm32wb)

Please see the individual crate READMEs for the full list of devices each crate
supports. All SVDs released by ST for STM32 devices are covered, so probably
your device is supported to some extent!

**Devices that are nearly identical, like the STM32F405/F415, are supported by
ST under a single SVD file STM32F405, so if you can't find your exact device
check if its sibling is supported instead. The crate READMEs make this clear.**

Many peripherals are not yet patched to provide the type-safe friendly-name
interface (enumerated values); please consider helping out with this!

Check out the full list of supported devices [here](https://stm32-rs.github.io/stm32-rs/).

## Adding New Devices

* Update SVD zips in `svd/vendor` to include new SVD.
* Run `svd/extract.sh` to extract the zips into `svd` (ignored in git).
* Add new YAML file in `devices/` with the new SVD path and include any
  required SVD patches for this device, such as renaming or merging fields.
* You can run `scripts/matchperipherals.py` script to find out what existing
  peripherals could be cleanly applied to this new SVD. If they look sensible,
  you can include them in your device YAML.
* Re-run `scripts/makecrates.py devices/` to update the crates with the new devices.
* Run `make` to rebuild, which will make a patched SVD and then run `svd2rust`
  on it to generate the final library.

## Updating Existing Devices/Peripherals

* You'll need to run `svd/extract.sh` at least once to pull the SVDs out.
* Edit the device or peripheral YAML (see below for format).
* Run `make` to rebuild all the crates using `svd patch` and `svd2rust`.
* Test your new stuff compiles: `cd stm32f4; cargo build --features stm32f405`

If you've added a new peripheral, consider using the `matchperipherals.py`
script to see which devices it would cleanly apply to.

To generate a new peripheral file from scratch, consider using
`periphtemplate.py`, which creates an empty peripheral file based on a single
SVD file, with registers and fields ready to be populated. For single bit wide
fields with names ending in 'E' or 'D' it additionally generates sample
"Enabled"/"Disabled" entries to save time.

## Device and Peripheral YAML Format

Please see the [svdtools](https://github.com/stm32-rs/svdtools) documentation
for full details of the patch file format.


### Style Guide

* Enumerated values should be named in the past tense ("enabled", "masked",
  etc).
* Descriptions should start with capital letters but do not end with a period

## Releasing

Notes for maintainers:

1. Create PR preparing for new release:
    * Update `CHANGELOG.md` with changes since last release and new contributors
    * Update `README.md` to bump version number in example snippet
    * Update `scripts/makecrates.py` to update version number for generated PACs
2. Merge PR once CI passes, pull master locally.
3. `make clean`
4. `make -j16 form`
5. `for f in stm32f0 stm32f1 stm32f2 stm32f3 stm32f4 stm32f7 stm32h7 stm32l0 stm32l1 stm32l4 stm32l5 stm32g0 stm32g4 stm32mp1 stm32wl stm32wb; cd $f; pwd; cargo publish --allow-dirty --no-default-features; cd ..; end`
6. `git tag -a vX.X.X -m vX.X.X`
7. `git push vX.X.X`

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
