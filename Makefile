dist/static/%: src/static/%
	@mkdir -p $(@D)
	cp $< $@

dist/%.py: src/%.py
	@mkdir -p $(@D)
	ln $< $@

dist/%.yaml: src/%.yaml
	@mkdir -p $(@D)
	cp $< $@

dist/door/%.pem: src/ios/Keys/%.pem
	@mkdir -p $(@D)
	cp $< $@

clean:
	rm -rf dist

# rcswitch build instructions & other native code.

CXXFLAGS=-O2 -fPIC

dist/rcswitch_wrap.cxx: third_party/rcswitch-pi/RCSwitch.h third_party/rcswitch-pi/rcswitch.i
	@mkdir -p $(@D)
	swig -c++ -python -o $@ third_party/rcswitch-pi/rcswitch.i

dist/rcswitch_wrap.o: dist/rcswitch_wrap.cxx
	$(CXX) $(CXXFLAGS) -c $+ -o $@ -I/usr/include/python2.7 -Ithird_party/rcswitch-pi

dist/RCSwitch.o: third_party/rcswitch-pi/RCSwitch.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -c $+ -o $@

dist/_rcswitch.so: dist/rcswitch_wrap.o dist/RCSwitch.o
	$(CXX) -shared $(LDFLAGS) $+ -o $@ -lwiringPi

dist/fswatch/fswatch: third_party/fswatch/fswatch.o
	@mkdir -p $(@D)
	gcc -framework CoreServices -o $@ $<

live: dist/fswatch/fswatch
	dist/fswatch/fswatch . 'make dist'

# third party python
define THIRD_PARTY_py_template
dist/third_party/%.py: third_party/py/$(1)/%.py
	@mkdir -p $$(@D)
	cp $$< $$@
endef

third_party_py := $(shell find third_party/py/* -maxdepth 0 -type d | sed 's,^[^/]*/[^/]*/,,' | tr "\\n" " ")
$(foreach dir,$(third_party_py),$(eval $(call THIRD_PARTY_py_template,$(dir))))

third_party_pyfiles := $(shell find third_party/py -name *.py \
	| egrep -v "example|doc|setup|testsuite"		\
	| sed 's,^third_party/[^/]*/[^/]*/,,'				\
	| egrep -v "^__init__.py" | tr "\\n" " ")
third_party_pyfiles := $(patsubst %,dist/third_party/%,$(third_party_pyfiles))

# UI targets
dist/static/css/bootstrap.css: third_party/static/bootstrap/dist/css/bootstrap.css
	@mkdir -p $(@D)
	cp $< $@

dist/static/css/bootstrap.css.map: third_party/static/bootstrap/dist/css/bootstrap.css.map
	@mkdir -p $(@D)
	cp $< $@

dist/static/js/jquery.js: third_party/static/jquery/jquery-2.1.1.js
	@mkdir -p $(@D)
	cp $< $@

dist/static/js/sprintf.js: third_party/static/sprintf.js/src/sprintf.js
	@mkdir -p $(@D)
	cp $< $@

dist/static/js/handlebars.js: third_party/static/handlebars/handlebars-v2.0.0.js
	@mkdir -p $(@D)
	cp $< $@

# final actual targets
py_files := $(patsubst src/%,dist/%,$(shell find src -name *.py))
static_js = $(patsubst %,dist/static/%,js/jquery.js js/app.js js/sprintf.js js/handlebars.js)
static_files := $(patsubst %,dist/static/%,index.html css/screen.css css/bootstrap.css css/bootstrap.css.map)
key_files := dist/door/DomicsKey.pem dist/door/DomicsCert.pem

dist/static: $(static_files) $(static_js) $(third_party_js_files) $(third_party_css_files)

dist: dist/app.yaml dist/cron.yaml $(py_files) $(third_party_pyfiles) $(key_files) dist/static

upload: dist
	appcfg.py --oauth2 update dist

devapp: dist
	PYTHONPATH=${PYTHONPATH}:./dist:./dist/third_party dev_appserver.py --use_mtime_file_watcher=true dist/app.yaml

runonpi: dist
	rsync -arvz dist/ pi@domicspi.local:~/dist/
	ssh -t pi@domicspi.local 'sudo PYTHONPATH=$${PYTHONPATH}:~/dist:~/dist/third_party python ~/dist/pi/control.py'

