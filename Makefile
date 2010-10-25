# Simple makefile to quickly access handy build commands for Cython extension
# code generation.  Note that the actual code to produce the extension lives in
# the setup.py file, this Makefile is just meant as a command
# convenience/reminder while doing development.

PYTHON?=python
PKGDIR=dipy
DOCDIR=${PKGDIR}/doc
TESTDIR=${PKGDIR}/tests


help:
	@echo "Numpy/Cython tasks.  Available tasks:"
	@echo "ext  -> build the Cython extension module."
	@echo "html -> create annotated HTML from the .pyx sources"
	@echo "test -> run a simple test demo."
	@echo "all  -> Call ext, html and finally test."

all: ext html test

ext: track_performance.so track_volumes.so reconstruction_performance.so

test:   ext
	nosetests .

html:  ${PKGDIR}/core/track_performance.html ${PKGDIR}/io/track_volumes.html ${PKGDIR}/io/reconstrunction_performance.html

track_performance.so: ${PKGDIR}/core/track_performance.pyx
track_volumes.so: ${PKGDIR}/io/track_volumes.pyx
reconstruction_performance.so: ${PKGDIR}/core/reconstruction_performance.pyx

	python setup.py build_ext --inplace

# Phony targets for cleanup and similar uses

.PHONY: clean

clean:
	- find ${PKGDIR} -name "*.so" -print0 | xargs -0 rm
	- find ${PKGDIR} -name "*.c" -print0 | xargs -0 rm
	- find ${PKGDIR} -name "*.html" -print0 | xargs -0 rm
	rm -rf build

# Suffix rules
%.c : %.pyx
	cython $<

%.html : %.pyx
	cython -a $<

# Print out info for possible install methods
check-version-info:
	$(PYTHON) -c 'from nisext.testers import info_from_here; info_from_here("dipy")'

# Run tests from installed code
installed-tests:
	$(PYTHON) -c 'from nisext.testers import tests_installed; tests_installed("dipy")'

# Run tests from installed code
sdist-tests:
	$(PYTHON) -c 'from nisext.testers import sdist_tests; sdist_tests("dipy")'

# Update nisext subtree from remote
update-nisext:
	git fetch nisext
	git merge --squash -s subtree --no-commit nisext/master
