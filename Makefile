all: patch svd2rust

.PHONY: patch svd2rust form check clean-rs clean-patch clean-html clean

SHELL := /bin/bash

CRATES := stm32f0 stm32f1 stm32f2 stm32f3 stm32f4 stm32f7 stm32h7 \
          stm32l0 stm32l1 stm32l4

# All yaml files in devices/ will be used to patch an SVD
YAMLS := $(wildcard devices/*.yaml)

# Each yaml file in devices/ exactly name-matches an SVD file in svd/
PATCHED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.patched, $(YAMLS))

# Each device will lead to a crate/src/device/mod.rs file
RUST_SRCS := $(foreach crate, $(CRATES), \
               $(patsubst devices/$(crate)%.yaml, \
                          $(crate)/src/$(crate)%/mod.rs, \
                          $(wildcard devices/$(crate)*.yaml)))
RUST_DIRS := $(foreach crate, $(CRATES), \
               $(patsubst devices/$(crate)%.yaml, \
                          $(crate)/src/$(crate)%/, \
                          $(wildcard devices/$(crate)*.yaml)))
FORM_SRCS := $(foreach crate, $(CRATES), \
               $(patsubst devices/$(crate)%.yaml, \
                          $(crate)/src/$(crate)%/.form, \
                          $(wildcard devices/$(crate)*.yaml)))
CHECK_SRCS := $(foreach crate, $(CRATES), \
               $(patsubst devices/$(crate)%.yaml, \
                          $(crate)/src/$(crate)%/.check, \
                          $(wildcard devices/$(crate)*.yaml)))

# Turn a devices/device.yaml and svd/device.svd into svd/device.svd.patched
svd/%.svd.patched: devices/%.yaml svd/%.svd
	python3 scripts/svdpatch.py $<

define crate_template
$(1)/src/%/mod.rs: svd/%.svd.patched
	mkdir -p $$(@D)
	cd $$(@D); svd2rust -i ../../../$$<
	rustfmt $$(@D)/lib.rs
	sed "1,6d;10d;s/crate::Interrupt/crate::$$(<F:.svd.patched=)::Interrupt/" $$(@D)/lib.rs > $$@
	rm $$(@D)/build.rs $$(@D)/lib.rs

$(1)/src/%/.form: $(1)/src/%/mod.rs
	form -i $$< -o $$(@D)
	rm $$<
	mv $$(@D)/lib.rs $$<
	find $$(@D) -name "*.rs" -exec rustfmt {} +
	touch $$@

$(1)/src/%/.check: $(1)/src/%/mod.rs
	cd $(1) && cargo check --target-dir ../target/check/$$* --features $$*
	touch $$@

endef

$(foreach crate,$(CRATES),$(eval $(call crate_template, $(crate))))

svd/%.svd:
	cd svd && ./extract.sh

patch: $(PATCHED_SVDS)

svd2rust: $(RUST_SRCS)

form: $(FORM_SRCS)

check: $(CHECK_SRCS)

html/index.html: $(PATCHED_SVDS)
	@mkdir -p html
	python3 scripts/makehtml.py html/ svd/stm32*.svd.patched

html: html/index.html

clean-rs:
	rm -rf $(RUST_DIRS)

clean-patch:
	rm -f $(PATCHED_SVDS)

clean-html:
	rm -rf html

clean: clean-rs clean-patch clean-html
	rm -rf .deps

# Generate dependencies for each device YAML
.deps/%.d: devices/%.yaml
	@mkdir -p .deps
	python3 scripts/makedeps.py $< > $@

-include $(patsubst devices/%.yaml, .deps/%.d, $(YAMLS))
