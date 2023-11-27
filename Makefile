all: patch svd2rust

.PHONY: extract patch crates svd2rust svdconv form check clean_mmaps clean-rs clean-patch clean-html clean-svd clean_svdconv clean lint mmaps
.PRECIOUS: svd/%.svd .deps/%.d

SHELL := /usr/bin/env bash

# Path to `python3` executable binary
PYTHON ?= python3

# Path to `svd`/`svdtools`
SVDTOOLS ?= svdtools

CRATES ?= stm32c0 stm32f0 stm32f1 stm32f2 stm32f3 stm32f4 stm32f7 \
          stm32h5 stm32h7 stm32l0 stm32l1 stm32l4 stm32l5 stm32g0 stm32g4 \
          stm32mp1 stm32wl stm32wb stm32u5

# All yaml files in devices/ will be used to patch an SVD
YAMLS := $(foreach crate, $(CRATES), \
	       $(wildcard devices/$(crate)*.yaml))

# Each yaml file in devices/ exactly name-matches an SVD file in svd/
EXTRACTED_SVDS := $(patsubst devices/%.yaml, svd/%.svd, $(YAMLS))
PATCHED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.patched, $(YAMLS))
FORMATTED_SVDS := $(patsubst devices/%.yaml, svd/%.svd.formatted, $(YAMLS))

# Each yaml file also corresponds to a mmap in mmaps/
MMAPS := $(patsubst devices/%.yaml, mmaps/%.mmap, $(YAMLS))

# Each yaml file also corresponds to svdconv report in svdconv/
SVDCONV_REPORTS := $(patsubst devices/%.yaml, svdconv/%.txt, $(YAMLS))

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

# Generate svdconv reports from patched SVD
svdconv/%.txt: svd/%.svd.patched
	@mkdir -p svdconv
	svdconv --suppress-warnings $< > $@ | true

# Generates the common crate files: Cargo.toml, build.rs, src/lib.rs, README.md
crates:
	$(PYTHON) scripts/makecrates.py devices/ -y --families $(CRATES)

define crate_template
$(1)/src/%/mod.rs: svd/%.svd.patched $(1)/Cargo.toml
	mkdir -p $$(@D)
	cd $$(@D); svd2rust -m -g --strict --pascal_enum_values --max_cluster_size --atomics --atomics_feature atomics -i ../../../$$<
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
	cd $(1) && cargo check --target-dir ../target/check/ --features rt,atomics,$$*
	touch $$@

$(1)/Cargo.toml: crates

endef

$(foreach crate,$(CRATES),$(eval $(call crate_template, $(crate))))

svd/%.svd: svd/.extracted ;

svd/.extracted:
	cd svd && ./extract.sh && touch .extracted

extract: $(EXTRACTED_SVDS)

patch: $(PATCHED_SVDS)

svd2rust: $(RUST_SRCS) crates

form: $(FORM_SRCS) crates

svdformat: $(FORMATTED_SVDS)

check: $(CHECK_SRCS)

html/index.html: $(PATCHED_SVDS)
	@mkdir -p html
	svdtools html html/ $(PATCHED_SVDS)

html/comparisons.html: $(PATCHED_SVDS) scripts/htmlcomparesvdall.sh
	scripts/htmlcomparesvdall.sh

html: html/index.html html/comparisons.html

lint: $(PATCHED_SVDS)
	xmllint --schema svd/cmsis-svd.xsd --noout $(PATCHED_SVDS)

mmaps: $(MMAPS)

svdconv: $(SVDCONV_REPORTS)

clean-rs:
	rm -rf $(RUST_DIRS)
	rm -f */src/generic.rs

clean-patch:
	rm -f $(PATCHED_SVDS)
	rm -f $(FORMATTED_SVDS)

clean-html:
	rm -rf html

clean-mmaps:
	rm -rf mmaps

clean-svdconv:
	rm -rf svdconv

clean-crates:
	rm -rf $(CRATES)

clean-svd:
	rm -f svd/*.svd
	rm -f svd/.extracted

clean: clean-rs clean-patch clean-html clean-svd clean-mmaps clean-svdconv
	rm -rf .deps

# As alternative to `pip install --user svdtools`:
# run `make venv update-venv` and `source venv/bin/activate'
venv:
	$(PYTHON) -m venv venv

update-venv:
	venv/bin/pip install -U pip
	venv/bin/pip install -U -r requirements.txt

install:
	scripts/tool_install.sh

# Generate dependencies for each device YAML
.deps/%.d: devices/%.yaml
	@mkdir -p .deps
	$(SVDTOOLS) makedeps $< $@

-include .deps/*
