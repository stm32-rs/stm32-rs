all: patch svd2rust

.PHONY: patch crates svd2rust form check clean-rs clean-patch clean-html clean-svd clean lint mmaps
.PRECIOUS: svd/%.svd .deps/%.d

SHELL := /usr/bin/env bash

# Path to `svd`/`svdtools`
SVDTOOLS ?= svd

CRATES ?= stm32f0 stm32f1 stm32f2 stm32f3 stm32f4 stm32f7 stm32h7 \
          stm32l0 stm32l1 stm32l4 stm32l5 stm32g0 stm32g4 stm32mp1 \
          stm32wl stm32wb

# All yaml files in devices/ will be used to patch an SVD
YAMLS := $(foreach crate, $(CRATES), \
	       $(wildcard devices/$(crate)*.yaml))

# Each yaml file in devices/ exactly name-matches an SVD file in svd/
PATCHED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.patched, $(YAMLS))
FORMATTED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.formatted, $(YAMLS))

# Each yaml file also corresponds to a mmap in mmaps/
MMAPS := $(patsubst devices/%.yaml, mmaps/%.mmap, $(YAMLS))

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
	$(SVDTOOLS) patch $<

svd/%.svd.formatted: svd/%.svd.patched
	xmllint $< --format -o $@

# Generate mmap from patched SVD
mmaps/%.mmap: svd/%.svd.patched
	@mkdir -p mmaps
	$(SVDTOOLS) mmap $< > $@

# Generates the common crate files: Cargo.toml, build.rs, src/lib.rs, README.md
crates:
	python3 scripts/makecrates.py devices/ -y --families $(CRATES)

define crate_template
$(1)/src/%/mod.rs: svd/%.svd.patched $(1)/Cargo.toml
	mkdir -p $$(@D)
	cd $$(@D); svd2rust -m -g -i ../../../$$<
	rustfmt --config-path="rustfmt.toml" $$@
	rm $$(@D)/build.rs
	mv -f $$(@D)/generic.rs $$(@D)/../

$(1)/src/%/.form: $(1)/src/%/mod.rs
	form -i $$< -o $$(@D)
	rm $$<
	mv $$(@D)/lib.rs $$<
	rustfmt --config-path="rustfmt.toml" $$<
	touch $$@

$(1)/src/%/.check: $(1)/src/%/mod.rs
	cd $(1) && cargo check --target-dir ../target/check/ --features rt,$$*
	touch $$@

$(1)/Cargo.toml: crates

endef

$(foreach crate,$(CRATES),$(eval $(call crate_template, $(crate))))

svd/%.svd: svd/.extracted ;

svd/.extracted:
	cd svd && ./extract.sh && touch .extracted

patch: $(PATCHED_SVDS)

svd2rust: $(RUST_SRCS) crates

form: $(FORM_SRCS) crates

svdformat: $(FORMATTED_SVDS)

check: $(CHECK_SRCS)

html/index.html: $(PATCHED_SVDS) scripts/makehtml.py scripts/makehtml.index.template.html scripts/makehtml.template.html
	@mkdir -p html
	python3 scripts/makehtml.py html/ $(PATCHED_SVDS)

html/comparisons.html: $(PATCHED_SVDS) scripts/htmlcomparesvdall.sh scripts/htmlcomparesvd.py
	scripts/htmlcomparesvdall.sh

html: html/index.html html/comparisons.html

lint: $(PATCHED_SVDS)
	xmllint --schema svd/cmsis-svd.xsd --noout $(PATCHED_SVDS)

mmaps: $(MMAPS)

clean-rs:
	rm -rf $(RUST_DIRS)
	rm -f */src/generic.rs

clean-patch:
	rm -f $(PATCHED_SVDS)
	rm -f $(FORMATTED_SVDS)

clean-html:
	rm -rf html

clean-crates:
	rm -rf $(CRATES)

clean-svd:
	rm -f svd/*.svd
	rm -f svd/.extracted

clean: clean-rs clean-patch clean-html clean-svd
	rm -rf .deps

# As alternative to `pip install --user svdtools`:
# run `make venv update-venv` and `source venv/bin/activate'
venv:
	python3 -m venv venv

update-venv:
	venv/bin/pip install -U pip
	venv/bin/pip install -U -r requirements.txt

# Generate dependencies for each device YAML
.deps/%.d: devices/%.yaml
	@mkdir -p .deps
	$(SVDTOOLS) makedeps $< $@

-include .deps/*
