dist/static/jquery.js: third_party/jquery/jquery-2.0.3.js
	@mkdir -p $(@D)
	cp $< $@

dist/static/%: src/static/%
	@mkdir -p $(@D)
	cp $< $@

dist/%.py: src/%.py
	@mkdir -p $(@D)
	cp $< $@

dist/%.yaml: src/%.yaml
	@mkdir -p $(@D)
	cp $< $@

clean:
	rm -rf dist

define THIRD_PARTY_template
dist/%.py: third_party/py/$(1)/%.py
	@mkdir -p $$(@D)
	cp $$< $$@
endef

third_party := $(shell find third_party/py/* -maxdepth 0 | sed 's,^[^/]*/[^/]*/,,' | tr "\\n" " ")
$(foreach dir,$(third_party),$(eval $(call THIRD_PARTY_template,$(dir))))
static_files := $(patsubst %,dist/static/%,index.html jquery.js)
py_files := $(patsubst src/%,dist/%,$(shell find src -name *.py))
third_party_files := $(shell find third_party/py -name *.py \
	| egrep -v "example|doc|setup|test"						\
	| sed 's,^[^/]*/[^/]*/[^/]*/,,'							\
	| egrep -v "^__init__.py" | tr "\\n" " ")
third_party_files := $(patsubst %,dist/%,$(third_party_files))

dist: dist/app.yaml $(py_files) $(static_files) $(third_party_files)

upload: dist
	appcfg.py --oauth2 update dist

devapp: dist
	dev_appserver.py dist/app.yaml

runpi: dist
	PYTHONPATH=${PYTHONPATH}:./dist python dist/pi/control.py