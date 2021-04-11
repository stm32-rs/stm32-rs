# Contributing Guidelines

Thank you for your interest in contributing to stm32-rs! Below are some guides
to help with common contribution tasks. If you think anything is missing,
please open an issue or PR to fix this file.

## Before you start

It's worth double-checking that the change you want hasn't already been made,
either in the current master branch (but not yet released), or in another
device but still applies to your device. Try using GitHub search or grepping
the repository for relevant register or field names; if someone else has
already described the peripheral or created the fix you need, you can simply
include it in the device that requires it, or you might be able to copy or
refactor their change to also apply to your situation.

Next, check where your changes should go:

* Fixes to the structure of an SVD file, such as adding a register, renaming a
  field, or deleting a peripheral, go in `devices/`, either in the
  device-specific file `devices/stm32xxxx.yaml` or the shared patches under
  `devices/common_patches/`.
* Descriptions of fields, which means either enumerated values ("you can write
  1 to this field to mean 'Start'") or write constraints ("this field can take
  any value from 2 to 30") go in `peripherals/`.

## Fixing bugs in SVD files

If there's an error in the SVD (or generated crate) for a device, for example
a missing register or field, or a field that's the wrong width or name, you
can fix these using the [svdtools](https://github.com/stm32-rs/svdtools) YAML
patching syntax.

If your fix is only for a specific device, the patch should go into the
`devices/stm32xxxx.yaml` file. If your fix applies to multiple devices,
there may already be a suitable file in `devices/common_patches/` which
you could edit, or otherwise please create a new file in that directory.

As an example, PR [#526](https://github.com/stm32-rs/stm32-rs/pull/526) added
a missing field for the L4x3 device. Here the missing field is specific to
that device, so the patch goes in `devices/stm32l4x3.yaml`, inside the existing
`RCC` top-level section:

```diff
  RCC:
    APB1ENR1:
      ...
+   APB1RSTR1:
+     _add:
+       USBFSRST:
+         description: USB FS reset
+         bitOffset: 26
+         bitWidth: 1
```

It's important to not duplicate top-level YAML keys: because the `RCC` section
already existed, adding a new one would cause the previous one to be ignored.

See the [svdtools](https://github.com/stm32-rs/svdtools) README for more
information on the YAML patching syntax, or have a look at some existing
patches to get an idea of how patching works.

## Adding descriptions

The SVD files supplied by ST do not contain any information on what values may
be written to fields, but [svd2rust](https://crates.io/crates/svd2rust) uses
such information to create its safe and user-friendly API in the crates we
generate. We place this sort of change in the `peripherals/` directory, and
then include them in each device that uses them. Typically it's possible to
cover a lot of devices, since many share the same peripherals, and someone may
have already described the peripheral you're interested in for another device,
in which case you can simply include their YAML file into your device.

There are two types of description: either "enumerated values", which describe
the list of possible named values the field may take, or "write constraints",
which are a set of integers that may be written to the field. The syntax is
described in the [svdtools] readme.

For example, PR [#486](https://github.com/stm32-rs/stm32-rs/pull/486) added
descriptions for the OPAMP peripheral in the STM32G4 family:

```yaml
OPAMP:
  OPAMP?_CSR:
    LOCK:
      ReadWrite: [0, "CSR is read-write"]
      ReadOnly: [1, "CSR is read-only, can only be cleared by system reset"]
    TRIMOFFSETN: [0, 31]
```

Here any register matching `OPAMP?_CSR` is updated, meaning any single digit
in place of the `?`. The `LOCK` field can be written with `ReadWrite` or
`ReadOnly`, corresponding to values 0 and 1, while the `TRIMOFFSETN` field can
take any value in the range 0 to 31 inclusive. With this information, svd2rust
generates safe APIs allowing code like `opamp1_csr.write(|w|
w.lock().read_write().trimoffsetn().bits(15))`.

For more complicated peripherals, it's common to split the descriptions into
separate files, as some devices may only use a subset of the full descriptions.

## Adding a new device

Before adding a new device, check if it's meant to be covered by an existing
device - for example, the STM32F415 is covered by the `stm32f405` feature,
because they are very similar and share an SVD file. You can check in the
`stm32_parts_table.yaml` file if this is the case.

If the device is not already supported, we need an SVD file to add it.
Sometimes the SVD file already exists but is not used yet -- in a local clone of
the repository, run `svd/extract.sh` and check if a suitable SVD file is
present. If not, you'll need to download it from ST's website, possibly
updating the entire family's zip file. See PR
[#514](https://github.com/stm32-rs/stm32-rs/pull/514) for an example.

Once the SVD file exists, create a new file `devices/stm32xxxxx.yaml` with the
`_svd` top-level key set to the path of the SVD file to use. You can then
include any patches or descriptions that are relevant to the new device;
the script `scripts/matchperipherals.py` might be helpful to find matching
patches. See PR [#532](https://github.com/stm32-rs/stm32-rs/pull/532) for an
example of adding a new device.

Finally, the new device must be added to the `stm32_parts_table.yaml` file,
along with some metadata about its reference manual, web page, and the list
of chips it covers (which may be just one chip).

## Adding a new family

To add a whole new family (for exmaple, STM32F4), in addition to the steps
above for adding a new device, the family must be added to a few other
locations:

* Update `.github/workflows/ci.yaml` to add the family to `crates`
* Update `.github/workflows/nightlies.yaml` and check the `Build and publish`
  step will move the generated files to `../nightly`
* Update `Makefile` to add the family to `CRATES`
* Update `scripts/makecrates.py` to add the family to `CRATE_DOC_FEATURES`
  and `CRATE_DOC_TARGETS`, and possibly update the family-name logic in `main`

For an example, see PR [#467](https://github.com/stm32-rs/stm32-rs/pull/467).

## Checking your work

If possible, run `make` in a local clone of the repository to rebuild the
patched SVDs and crates after your change. To build only the SVD files and
not generate the crate, run `make patch`. If you specify the `CRATES`
environment variable, only that family is updated: `CRATES=stm32f0 make`.

The continuous integration (CI) system will also build everything from scratch
when you submit a PR, and also generates a text-based memory map diff which
can help check your changes had the intended effect. These diffs won't show
changes to descriptions or reflect newly added SVD files, though.

## Getting help

Please open a draft PR or an issue if you want an error fixed or other change
made but aren't sure how to do it.

## Once your PR is merged

After your PR is merged, an updated crate is automatically pushed to
[stm32-rs/nightlies](https://github.com/stm32-rs/stm32-rs-nightlies) which you
can use as a git dependency in your `Cargo.toml`. The published crates on
crates.io are updated on a slower cadence, typically every few months.

## Licensing

As mentioned in the [README](https://github.com/stm32-rs/stm32-rs#readme),
the stm32-rs project contributions are dual licensed under the Apache license
version 2.0 and the MIT license, and:

> Unless you explicitly state otherwise, any contribution intentionally
> submitted for inclusion in the work by you, as defined in the Apache-2.0
> license, shall be dual licensed as above, without any additional terms or
> conditions.
