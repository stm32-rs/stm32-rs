# STM32 Crates

_formerly [adamgreig/stm32-rs](https://github.com/adamgreig/stm32-rs)_

This repository contains device support for all STM32 microcontrollers,
providing a safe API to that device using [svd2rust] and an extensive hierarchy
of SVD patches. Each supported device is a feature-gated module in a crate for
that device family.

[svd2rust]: https://github.com/rust-embedded/svd2rust

**Please note many parts of most libraries will not have been tested on every
possible chip yet! While they're all generated from ST-provided SVD files,
we can't make any guarantee of correctness. Please report any bugs you find!**

You can see current coverage status for each chip
[here](https://stm32.agg.io/rs). Coverage means that individual fields are
documented with possible values, but even devices with low coverage should
have every register and field available in the API. That page also allows you
to drill down into each field on each register on each peripheral.

## Using Device Crates In Your Own Project

In your own project's `Cargo.toml`:
```toml
[dependencies.stm32f4]
version = "0.4.0"
features = ["stm32f405", "rt"]
```
The `rt` feature is optional but helpful. See
[svd2rust](https://docs.rs/svd2rust/0.12.0/svd2rust/#the-rt-feature) for
details.

Then, in your code:

```rust
extern crate stm32f4;
use stm32f4::stm32f405;

let mut peripherals = stm32f405::Peripherals::take().unwrap();
```

Refer to `svd2rust` [documentation](https://docs.rs/svd2rust) for further usage.

Replace `stm32f4` and `stm32f405` with your own device; see the individual
crate READMEs for the complete list of supported devices. All current STM32
devices should be supported to some level.

## Generating Device Crates / Building Locally

* Install `svd2rust`: `cargo install svd2rust`
* Install `form`: `cargo install form`
* Install latest rustfmt: `cargo uninstall rustfmt; rustup component add rustfmt-preview`
* Install PyYAML: `pip install pyyaml`
* Unzip bundled SVD zip files: `cd svd; ./extract.sh`
* Generate patched SVD files: `cd ..; make patch`
* Generate svd2rust device crates: `make svd2rust` (you probably want `-j` for this)
* Optional: Format device crates: `make form` (you probably want `-j` for this)

## Motivation and Objectives

This project serves two purposes:

* Create a source of high-quality STM32 SVD files, with manufacturer errors
  and inconsistencies fixed. These files could be used with svd2rust or other
  tools, or in other projects. They should hopefully be useful in their own
  right.
* Create and publish svd2rust-generated crates covering all STM32s, using
  the SVD files.

At present many individual crates exist for specific STM32 devices, typically
maintained by many seprate users with hand-edited updates to the SVD files.
This means that support for less-common STM32s is completely missing, and
the hand-edited SVDs may be inconsistent with other crates. Plus, it's a huge
duplication of work, since so many peripherals are the same between devices.

This project hopes to reduce the duplication of effort, and hopefully in the
future enable further automation / code generation based on automatically
identifying similarities between different devices.

## Helping

This project is still young and there's a lot to do!

* More peripheral patches need to be written, most of all. See what we've got
  in `peripherals/` and grab a reference manual!
* Also everything needs testing, and you can't so easily automate finding bugs
  in the SVD files...
* Is this really the best way to support a lot of devices? We end up with a
  handful of crates, each with a lot of features, and each feature enables a
  gigantic module, but they all share a lot of code. Can we automatically
  factor out the shared structures?

## Supported Device Families

* [STM32F0](stm32f0/) [![crates.io](https://img.shields.io/crates/v/stm32f0.svg)](https://crates.io/crates/stm32f0)
* [STM32F1](stm32f1/) [![crates.io](https://img.shields.io/crates/v/stm32f1.svg)](https://crates.io/crates/stm32f1)
* [STM32F2](stm32f2/) [![crates.io](https://img.shields.io/crates/v/stm32f2.svg)](https://crates.io/crates/stm32f2)
* [STM32F3](stm32f3/) [![crates.io](https://img.shields.io/crates/v/stm32f3.svg)](https://crates.io/crates/stm32f3)
* [STM32F4](stm32f4/) [![crates.io](https://img.shields.io/crates/v/stm32f4.svg)](https://crates.io/crates/stm32f4)
* [STM32F7](stm32f7/) [![crates.io](https://img.shields.io/crates/v/stm32f7.svg)](https://crates.io/crates/stm32f7)
* [STM32L0](stm32l0/) [![crates.io](https://img.shields.io/crates/v/stm32l0.svg)](https://crates.io/crates/stm32l0)
* [STM32L1](stm32l1/) [![crates.io](https://img.shields.io/crates/v/stm32l1.svg)](https://crates.io/crates/stm32l1)
* [STM32L4](stm32l4/) [![crates.io](https://img.shields.io/crates/v/stm32l4.svg)](https://crates.io/crates/stm32l4)
* [STM32H7](stm32h7/) [![crates.io](https://img.shields.io/crates/v/stm32h7.svg)](https://crates.io/crates/stm32h7)

Please see the individual crate READMEs for the full list of devices each crate
supports. All SVDs released by ST for STM32 devices are covered, so probably
your device is supported to some extent!

**Devices that are nearly identical, like the STM32F405/F415, are supported by
ST under a single SVD file STM32F405, so if you can't find your exact device
check if its sibling is supported instead.**

Many peripherals are not yet patched to provide the type-safe friendly-name
interface; please consider helping out with this!

Check out the full list of supported devices [here](https://stm32.agg.io/rs).

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
* Run `make` to rebuild all the crates using `svdpatch.py` and `svd2rust`.
* Test your new stuff compiles: `cd stm32f4; cargo build --features stm32f405`

If you've added a new peripheral, consider using the `matchperipherals.py`
script to see which devices it would cleanly apply to.

To generate a new peripheral file from scratch, consider using
`periphtemplate.py`, which creates an empty peripheral file based on a single
SVD file, with registers and fields ready to be populated. For single bit wide
fields with names ending in 'E' or 'D' it additionally generates sample
"Enabled"/"Disabled" entries to save time.

## Device and Peripheral YAML Format

The patch specifications are in YAML and have the following general format:

```yaml
# Path to the SVD file we're targetting. Relative to this file.
# This must be included only in the device YAML file.
_svd: "../svd/STM32F0x0.svd"

# Include other YAML files. Path relative to this file.
_include:
    - "../peripherals/gpio_v2.yaml"

# Alter top-level information and peripherals for this device
_modify:
    version: 1.1
    description: bla bla
    addressUnitBits: 8
    width: 32
    cpu:
        revision: r1p2
        mpuPresent: true
    # Peripherals can either live directly at this level (but other top-level
    # fields will name match first)
    C_ADC:
        name: ADC_Common
    # Or they can be inside a _peripherals block, to avoid name conflicts.
    _peripherals:
        FSMC:
            description: Flexible static memory controller

# Add whole new peripherals to this device.
# Incredibly this feature is required.
_add:
    ADC_Common:
        description: ADC Common registers
        groupName: ADC
        baseAddress: 0x40012300
        addressBlock:
            offset: 0x0
            size: 0x400
        registers:
            CSR:
                description: ADC Common status register
                addressOffset: 0x0
                access: read-only
                resetValue: 0x00000000
                fields:
                    OVR3:
                        description: Overrun flag of ADC3
                        bitOffset: 21
                        bitWidth: 1
        interrupts:
            ADC1_2:
                description: ADC global interrupt
                value: 18

# Reorder the heirarchy of peripherals with 'deriveFrom'.
_rebase:
    # The KEY peripheral steals everything but 'interrupt', 'name',
    # and 'baseAddress' elements from the VALUE peripheral.
    # Peripherals that were 'deriveFrom="VALUE"' are now 'deriveFrom="KEY"'.
    I2C1: I2C3

# An STM32 peripheral, matches an SVD <peripheral> tag.
# Does not match any tag with derivedFrom attribute set.
"GPIO*":
    # We can include other YAML files inside this peripheral
    _include:
        - "path/to/file.yaml"

    # Alter fields on existing registers inside this peripheral
    _modify:
        # Rename this badly named register. Takes effect before anything else.
        # Don't use wildcard matches if you are changing the name!
        # We could have specified name or description or other tags to update.
        GPIOB_OSPEEDR:
          name: OSPEEDR
        # Equivalently the register could go in a '_registers' block
        _registers:
            GPIOB_OSPEEDR:
                name: OSPEEDR
        # Change the value of an interrupt in this peripheral
        _interrupts:
            EXTI0:
                value: 101


    # Add new registers and interrupts to this peripheral.
    # Entries are registers by default, which can also go inside a '_registers'
    # block, or interrupts go in an '_interrupts' block.
    _add:
        EXAMPLER:
            description: An example register
            addressOffset: 0x04
            access: read-write
            fields:
                EXR1:
                    description: Example field
                    bitOffset: 16
                    bitWidth: 4
        _registers:
            EXAMPLR2:
                description: Another example register
        _interrupts:
            EXAMPLEI:
                description: An example interrupt
                value: 100

    # Anywhere you can '_add' something, you can also '_delete' it.
    # Wildcards are supported. Note that the value here is a YAML list,
    # not a mapping like for most other keys.
    _delete:
        - GPIO*_EXTRAR

    # A register on this peripheral, matches an SVD <register> tag
    MODER:
        # As in the peripheral scope, rename or redescribe a field.
        # Don't use wildcard matches if you are changing the name!
        _modify:
            FIELD:
              description: NEWDESC

        # Add new fields to this register
        _add:
            NEWFIELD:
              description: DESCRIPTION
              bitOffset: 12
              bitWidth: 4
              access: read-write

        # Often fields that should be one contiguous integer are specified
        # as a number of individual bits instead. This merges any matching
        # registers into a single field with the combined bitwidth and lowest
        # bit offset, and the shared description and access.
        _merge:
            - "FIELD*"

        # A field in this register, matches an SVD <field> tag
        FIELD:
            # By giving the field a dictionary we construct an enumerateValues
            VARIANT: [VALUE, DESCRIPTION]
            VARIANT: [VALUE, DESCRIPTION]

        # Another field. A list of two numbers gives a range writeConstraint.
        FIELD: [MINIMUM, MAXIMUM]

        # Another field with separate enumuerated values for read and write
        FIELD:
            _read:
                VARIANT: [VALUE, DESCRIPTION]
                VARIANT: [VALUE, DESCRIPTION]
            _write:
                VARIANT: [VALUE, DESCRIPTION]
                VARIANT: [VALUE, DESCRIPTION]
        # Sometimes fields are to big so we need to split them into smaller fields
        EXTI:
          IMR:
            # This would split MR into MRi where i = 0 ... bitlength
            _split: [MR]
```

### Name Matching
Peripheral, register, and field names can be specified:
* Directly
* Using `?` and `*` for single- and multi- character wildcards
* Using `[ABC]` to give a list of possible matching characters
* Using commas to separate a list of possible matches

You must quote the name if using any special characters in YAML.

### Style Guide

* Enumerated values should be named in the past tense ("enabled", "masked",
  etc).
* Descriptions should start with capital letters but do not end with a period

## Releasing

```
$ make -j16 form
$ make -j16 check
$ vi scripts/makecrates.py # update version number
$ python3 scripts/makecrates.py devices/
$ vi CHANGELOG.md # add changelog entry
$ git commit -am "vX.X.X"
$ git push origin master
# wait for travis build to succeed
$ git tag -a 'vX.X.X' -m 'vX.X.X'
$ git push origin vX.X.X
$ git push origin master
$ for f in stm32f0 stm32f1 stm32f2 stm32f3 stm32f4 stm32f7 stm32h7 stm32l0 stm32l1 stm32l4; cd $f; pwd; carg o publish --allow-dirty; cd ..; end
```

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
