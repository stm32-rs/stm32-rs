# STM32 Crates

This repository contains device support for as many STM32 devices as possible,
providing a safe API to that device using [svd2rust] and an extensive hierarchy
of SVD patches. Each supported device is a feature-gated module in a crate for
that device family.

[svd2rust]: https://github.com/japaric/svd2rust

**Please note most parts of most libraries will not have been tested on every
possible chip yet! While they're all generated from ST-provided SVD files,
we can't make any guarantee of correctness. Please report any bugs you find!**

## Prerequirement
Make sure that you use latest rustfmt. First remove installed rustfmt by 
`cargo uninstall rustfmt`
Install rustfmt via rustup
`rustup component add rustfmt-preview`

## Usage

In your own project's `Cargo.toml`:
```toml
[dependencies.stm32f4]
version = "0.1.0"
features = ["stm32f405"]
```

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

* STM32F0
* STM32F1
* STM32F2
* STM32F3
* STM32F4
* STM32F7
* STM32L0
* STM32L1
* STM32L4
* STM32H7

Please see the individual crate READMEs for the full list of devices each crate
supports. All SVDs released by ST for STM32 devices are covered, so probably
your device is supported to some extent!

**Devices that are nearly identical, like the STM32F405/F415, are supported by
ST under a single SVD file STM32F405, so if you can't find your exact device
check if its sibling is supported instead.**

Many peripherals are not yet patched to provide the type-safe friendly-name
interface; please consider helping out with this!

## Adding New Devices

* Update SVD zips in `svd/vendor` to include new SVD.
* Run `svd/extract.sh` to extract the zips into `svd` (ignored in git).
* Add new YAML file in `devices/` with the new SVD path and include any
  required SVD patches for this device, such as renaming or merging fields.
* You can run `scripts/matchperipherals.py` script to find out what existing
  peripherals could be cleanly applied to this new SVD. If they look sensible,
  you can include them in your device YAML.
* Re-run `scripts/makecrates.py` to update the crates with the new devices.
* Run `make` to rebuild, which will make a patched SVD and then run `svd2rust`
  on it to generate the final library.

## Updating Existing Devices/Peripherals

* You'll need to run `svd/extract.sh` at least once to pull the SVDs out.
* Edit the device or peripheral YAML (see below for format).
* Run `make` to rebuild all the crates using `svdpatch.py` and `svd2rust`.
* Test your new stuff compiles: `cd stm32f4; cargo build --features stm32f405`

If you've added a new peripheral, consider using the `matchperipherals.py` 
script to see which devices it would cleanly apply to.

## Device and Peripheral YAML Format

The patch specifications are in YAML and have the following general format:

```yaml
# Path to the SVD file we're targetting. Relative to this file.
# This must be included only in the device YAML file.
_svd: "../svd/STM32F0x0.svd"

# Include other YAML files. Path relative to this file.
_include:
    - "../peripherals/gpio_v2.yaml"

# Alter peripherals for this device
_modify:
    C_ADC:
        name: ADC_Common

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

# An STM32 peripheral, matches an SVD <peripheral> tag.
# Does not match any tag with derivedFrom attribute set.
"GPIO*":
    # We can include other YAML files inside this peripheral
    _include:
        - "path/to/file.yaml"

    # Alter fields on existing registers inside this peripheral
    _modify:
        # Rename this badly named registed. Takes effect before anything else.
        # Don't use wildcard matches if you are changing the name!
        # We could have specified name or description or other tags to update.
        GPIOB_OSPEEDR:
          name: OSPEEDR

    # Add new registers to this peripheral
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
            # Optional usage key specifies read, write, or read-write (default)
            _usage: read

        # Another field. A list of two numbers gives a range writeConstraint.
        FIELD: [MINIMUM, MAXIMUM]
```

### Name Matching
Peripheral, register, and field names can be specified:
* Directly
* Using `?` and `*` for single- and multi- character wildcards
* Using `[ABC]` to give a list of possible matching characters
* Using commas to separate a list of possible matches

You must quote the name if using any special characters in YAML.

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
