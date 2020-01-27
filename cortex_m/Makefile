all: patch

YAMLS := $(wildcard *.yaml)
PATCHED_SVDS := $(patsubst %.yaml, %.svd.patched, $(YAMLS))

%.svd.patched: %.yaml %.svd
	svd patch $<

patch: $(PATCHED_SVDS)

clean:
	rm -f $(PATCHED_SVDS)
