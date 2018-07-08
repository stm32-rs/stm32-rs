# Cortex-M SVD files

We can use the existing SVD patching framework to build SVD files which define
the peripherals common to all Cortex-M devices.

The base SVD files are `armv6m.svd` and `armv7m.svd` which are empty. They are
patched to create `armv6m.svd.patched` and `armv7m.patched` using `svdpatch.py`
and the `armv6m.yaml` and `armv7m.yaml` device files. The peripheral
definitions all come from the `peripherals/` directory.
