all: patch

YAMLS := $(wildcard *.yaml)
PATCHED_SVDS := $(patsubst %.yaml, %.svd.patched, $(YAMLS))

%.svd.patched: %.yaml %.svd
	python3 ../scripts/svdpatch.py < $(word 2,$^) $< > $@

patch: $(PATCHED_SVDS)

clean:
	rm -f $(PATCHED_SVDS)
