# \ var
MODULE = $(notdir $(CURDIR))
OS     = $(shell uname -s)
NOW    = $(shell date +%d%m%y)
REL    = $(shell git rev-parse --short=4 HEAD)
CORES  = $(shell grep processor /proc/cpuinfo| wc -l)
# / var
# \ dir
CWD    = $(CURDIR)
BIN    = $(CWD)/bin
DOC    = $(CWD)/doc
TMP    = $(CWD)/tmp
# / dir
# \ tool
CURL   = curl -L -o
PY     = bin/python3
PIP    = bin/pip3
PEP    = bin/autopep8
PYT    = bin/pytest
# / tool
# \ src
P     += config.py
S     += metaL.py test_metaL.py
# / src
# \ obj
# / obj
# \ cfg
# / cfg
# \ all
.PHONY: all
all: $(PY) metaL.py
	$^ $@
	$(MAKE) format
.PHONY: test
test: $(PYT) test_metaL.py
	$^
	$(MAKE) format
.PHONY: format
format: $(PEP)
$(PEP): $(S)
	$@ --ignore=E26,E302,E401,E402,E701,E702 --in-place $? && touch $@
# / all
# \ doc
.PHONY: doc
doc:
# / doc
# \ install
.PHONY: install
install: $(OS)_install js doc
	$(MAKE) $(PIP)
	$(MAKE) update
.PHONY: update
update: $(OS)_update
	$(PIP) install -U    pip autopep8
	$(PIP) install -U -r requirements.txt
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# \ py
$(PY) $(PIP):
	python3 -m venv .
	$(MAKE) update
$(PYT):
	$(PIP) install -U pytest
# / py
# \ js
.PHONY: js
js:
# / js
# / install
# \ merge
# / merge
