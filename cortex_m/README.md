# Cortex-M SVD files

We can use the existing SVD patching framework to build SVD files which define
the peripherals common to all Cortex-M devices.

The base SVD files are `armv6m.svd`, `armv7m.svd`, and `armv7em.svd`, which do
not contain any peripherals. They are patched to create `armv6m.svd.patched`
and `armv7m.patched` using `svd patch` and the `armv6m.yaml` and
`armv7m.yaml` device files. The peripheral definitions all come from
the `peripherals/` directory.
