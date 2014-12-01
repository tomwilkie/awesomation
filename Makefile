dist/static/%:  third_party/static/bootstrap/%
	@mkdir -p $(@D)
	cp $< $@

dist/static/%:  third_party/static/jquery/%
	@mkdir -p $(@D)
	cp $< $@

dist/static/%:  third_party/static/snap.svg/%
	@mkdir -p $(@D)
	cp $< $@

dist/static/%:  third_party/static/sprintf.js/src/%
	@mkdir -p $(@D)
	cp $< $@

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

# rcswitch build instructions
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

# third party python

define THIRD_PARTY_template
dist/third_party/%.py: third_party/py/$(1)/%.py
	@mkdir -p $$(@D)
	cp $$< $$@
endef

third_party := $(shell find third_party/py/* -maxdepth 0 -type d | sed 's,^[^/]*/[^/]*/,,' | tr "\\n" " ")
$(foreach dir,$(third_party),$(eval $(call THIRD_PARTY_template,$(dir))))
py_files := $(patsubst src/%,dist/%,$(shell find src -name *.py))
third_party_files := $(shell find third_party/py -name *.py \
	| egrep -v "example|doc|setup|testsuite"		\
	| sed 's,^third_party/[^/]*/[^/]*/,,'				\
	| egrep -v "^__init__.py" | tr "\\n" " ")
third_party_files := $(patsubst %,dist/third_party/%,$(third_party_files))

bootstap_files := $(shell find third_party/static/bootstrap -type f)
bootstap_files := $(patsubst third_party/static/bootstrap/%,%,$(bootstap_files))
static_files := $(patsubst %,dist/static/%,index.html css/screen.css jquery-2.0.3.js sprintf.js snap.svg-min.js $(bootstap_files))
key_files := dist/door/DomicsKey.pem dist/door/DomicsCert.pem

dist: dist/app.yaml $(py_files) $(static_files) $(third_party_files) $(key_files)

upload: dist
	appcfg.py --oauth2 update dist

devapp: dist
	PYTHONPATH=${PYTHONPATH}:./dist:./dist/third_party dev_appserver.py --use_mtime_file_watcher=true dist/app.yaml

runpi: dist
	PYTHONPATH=${PYTHONPATH}:./dist:./dist/third_party python dist/pi/control.py

runonpi: dist
	rsync -arvz dist/ pi@domicspi.local:~/dist/
	ssh -t pi@domicspi.local 'sudo PYTHONPATH=$${PYTHONPATH}:~/dist:~/dist/third_party python ~/dist/pi/control.py'

rundoor: dist
	PYTHONPATH=${PYTHONPATH}:./dist:./dist/third_party python dist/door/door.py

dist/fswatch/fswatch: third_party/fswatch/fswatch.o
	@mkdir -p $(@D)
	gcc -framework CoreServices -o $@ $<

live: dist/fswatch/fswatch
	dist/fswatch/fswatch . 'make dist'
