# STM32 Peripheral Access Crates - Nightly Builds

This repository contains automated builds of the [stm32-rs] crates, rebuilt
whenever a PR is merged to the master branch. Consult the [stm32-rs] README
for full details.

[stm32-rs]: https://github.com/stm32-rs/stm32-rs

## Using These Builds

Edit your `Cargo.toml`:

```toml
[dependencies.stm32f4]
git = "https://github.com/stm32-rs/stm32-rs-nightlies"
features = ["stm32f405", "rt"]
```

The nightlies should always build and be as stable as the latest release, but
typically with the latest patches and updates.

