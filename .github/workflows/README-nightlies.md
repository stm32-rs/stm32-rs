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


## Using These Builds With Cargo.lock

Since no commit history is stored in this repository (to keep download sizes
small), if you depend on a specific git commit (for example if one ends up
in your `Cargo.lock` file) it will eventually be removed from this repository,
breaking your build until you update.

For local development builds this shouldn't be a problem, but for CI systems
it might be annoying. The recommended solution is to fork this repository;
your fork will not update automatically and so will persist the commit you
use until you manually update the fork (either by pushing a new commit to it
or by deleting and re-forking it).
