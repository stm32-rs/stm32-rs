all: patch svd2rust

CRATES := stm32f0 stm32f1 stm32f2 stm32f3 stm32f4 stm32f7 stm32h7 \
          stm32l0 stm32l1 stm32l4

# All yaml files in devices/ will be used to patch an SVD
YAMLS := $(wildcard devices/*.yaml)

# Each yaml file in devices/ exactly name-matches an SVD file in svd/
PATCHED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.patched, $(YAMLS))

# Each device will lead to a crate/src/device.rs file
RUST_SRCS := $(foreach crate, $(CRATES), \
               $(patsubst devices/$(crate)%.yaml, \
                          $(crate)/src/$(crate)%.rs, \
                          $(wildcard devices/$(crate)*.yaml)))

# Turn a devices/device.yaml and svd/device.svd into svd/device.svd.patched
svd/%.svd.patched: devices/%.yaml svd/%.svd
	python3 scripts/svdpatch.py $<

# Please let me know if there's a better way to do this...
stm32f0/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32f1/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32f2/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32f3/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32f4/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32f7/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32l0/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32l1/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32l4/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

stm32h7/src/stm32%.rs: svd/stm32%.svd.patched
	- svd2rust -i $< | rustfmt > $@
	sed -i '1,3d;5,11d;13,16d;21s/interrupt/self::interrupt/' $@

patch: $(PATCHED_SVDS)

svd2rust: $(RUST_SRCS)

html: $(PATCHED_SVDS)
	python3 scripts/makehtml.py html/ svd/stm32*.svd.patched

clean-rs:
	rm -f $(RUST_SRCS)

clean-patch:
	rm -f $(PATCHED_SVDS)

clean: clean-rs clean-patch

# Generate dependencies for each device YAML
.deps/%.d: devices/%.yaml
	@mkdir -p .deps
	python3 scripts/makedeps.py $< > $@

-include $(patsubst devices/%.yaml, .deps/%.d, $(YAMLS))
