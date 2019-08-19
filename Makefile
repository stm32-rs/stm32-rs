all: patch svd2rust

.PHONY: patch svd2rust form check clean-rs clean-patch clean-html clean
.PRECIOUS: svd/%.svd .deps/%.d

SHELL := /usr/bin/env bash

CRATES ?= stm32f0 stm32f1 stm32f2 stm32f3 stm32f4 stm32f7 stm32h7 \
          stm32l0 stm32l1 stm32l4 stm32g0 stm32g4

# All yaml files in devices/ will be used to patch an SVD
YAMLS := $(foreach crate, $(CRATES), \
	       $(wildcard devices/$(crate)*.yaml))

# Each yaml file in devices/ exactly name-matches an SVD file in svd/
PATCHED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.patched, $(YAMLS))
FORMATTED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.formatted, $(YAMLS))

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
svd/%.svd.patched: devices/%.yaml svd/%.svd .deps/%.d
	python3 scripts/svdpatch.py $<

svd/%.svd.formatted: svd/%.svd.patched
	xmllint $< --format -o $@

define crate_template
$(1)/src/%/mod.rs: svd/%.svd.patched
	mkdir -p $$(@D)
	cd $$(@D); svd2rust -g -i ../../../$$<
	rustfmt --config-path="rustfmt.toml" $$(@D)/lib.rs
	sed "1,10d" $$(@D)/lib.rs > $$@
	rm $$(@D)/build.rs $$(@D)/lib.rs
	mv -f -t $$(@D)/.. $$(@D)/generic.rs

$(1)/src/%/.form: $(1)/src/%/mod.rs
	form -i $$< -o $$(@D)
	rm $$<
	mv $$(@D)/lib.rs $$<
	rustfmt --config-path="rustfmt.toml" $$<
	touch $$@

$(1)/src/%/.check: $(1)/src/%/mod.rs
	cd $(1) && cargo check --target-dir ../target/check/ --features rt,$$*
	touch $$@

endef

$(foreach crate,$(CRATES),$(eval $(call crate_template, $(crate))))

svd/%.svd:
	cd svd && ./extract.sh

patch: $(PATCHED_SVDS)

svd2rust: $(RUST_SRCS)

form: $(FORM_SRCS)

svdformat: $(FORMATTED_SVDS)

check: $(CHECK_SRCS)

html/index.html: $(PATCHED_SVDS)
	@mkdir -p html
	python3 scripts/makehtml.py html/ svd/stm32*.svd.patched

html: html/index.html

clean-rs:
	rm -rf $(RUST_DIRS)
	rm -f */src/generic.rs

clean-patch:
	rm -f $(PATCHED_SVDS)
	rm -f $(FORMATTED_SVDS)

clean-html:
	rm -rf html

clean: clean-rs clean-patch clean-html
	rm -rf .deps

# Generate dependencies for each device YAML
.deps/%.d: devices/%.yaml
	@mkdir -p .deps
	python3 scripts/makedeps.py $< > $@

-include .deps/*
