import config

import os, sys

## base object graph node class
class Object:
    def __init__(self, V):
        ## scalar value: name, number, string,..
        self.value = V
        ## associative array = environment = hash map
        self.slot = {}
        ## ordered container = vector = stack = nested AST
        self.nest = []

    ## @name dump

    ## `print` callback
    def __repr__(self): return self.dump()

    ## full `<T:V>` tree dump
    def dump(self, cycle=[], depth=0, prefix=''):
        # head
        ret = self.pad(depth) + self.head(prefix)
        # cycle
        if not depth: cycle = []
        if self in cycle: return ret + '_/'
        else: cycle += [self]
        # slot{}s
        for i in self.keys():
            ret += self[i].dump(cycle, depth + 1, f'{i} = ')
        # nest[]ed
        for j, k in enumerate(self.nest):
            ret += k.dump(cycle, depth + 1, f'{j}: ')
        # subtree
        return ret

    ## short single line `<T:V>` header
    def head(self, prefix=''):
        return f'{prefix}{self.tag()}:{self.val()}'

    ## tree padding
    def pad(self, depth):
        return '\n' + '\t' * depth

    ## `<T:`
    def tag(self):
        return self.__class__.__name__.lower()

    ## `:V>`
    def val(self):
        return f'{self.value}'

    ## @name operator

    ## `A.keys()`
    def keys(self):
        return sorted(self.slot.keys())

    ## `A[key] = B`
    def __setitem__(self, key, that):
        assert isinstance(key, str)
        assert isinstance(that, Object)
        self.slot[key] = that; return self

    ## `A[key]`
    def __getitem__(self, key):
        assert isinstance(key, str)
        return self.slot[key]

    ## `A // B -> A.push(B)`
    def __floordiv__(self, that):
        if isinstance(that, str): that = S(that)
        assert isinstance(that, Object)
        self.nest += [that]; return self

class Primitive(Object): pass

class S(Primitive):
    def __init__(self, start, end=None, pfx=None):
        super().__init__(start)
        self.start = start
        self.end = end
        self.pfx = pfx

    def gen(self, depth, to):
        ret = ''
        # pfx
        if self.pfx != None:
            ret += f'{to.tab*depth}{self.pfx}\n'
        # start
        ret += f'{to.tab*depth}{self.start}\n'
        # nest[]
        for j in self.nest:
            ret += j.gen(depth + 1, to)
        # end
        if self.end != None:
            ret += f'{to.tab*depth}{self.end}\n'
        # subtree
        return ret

class Sec(Primitive):
    def __init__(self, V):
        super().__init__(V)

    def gen(self, depth, to):
        # start
        ret = f'{to.tab*depth}{to.comment} \\ {self.value}\n'
        # nest[]
        for j in self.nest:
            ret += j.gen(depth, to)
        # end
        ret += f'{to.tab*depth}{to.comment} / {self.value}\n'
        # subtree
        return ret

class IO(Object): pass

class Path(IO): pass

class Dir(IO):
    def __init__(self, V):
        super().__init__(V)
        self['path'] = Path(V)

    def sync(self):
        for j in self.nest: j.sync()

    def __floordiv__(self, that):
        assert isinstance(that, Object)
        that["path"].value = f'{self["path"].value}/{that["path"].value}'
        if isinstance(that, Dir):
            try: os.mkdir(that["path"].value)
            except FileExistsError: pass
        elif isinstance(that, File):
            that.sync()
        else:
            raise TypeError([type(that)])
        return super().__floordiv__(that)

class File(IO):
    def __init__(self, V, ext, tab='\t', comment='#', commend=None):
        super().__init__(V)
        self['path'] = Path(V + ext)
        self.ext = ext
        self.tab = tab
        self.comment = comment
        self.commend = commend

    def sync(self):
        with open(self["path"].value, 'w') as F:
            for j in self.nest:
                F.write(j.gen(0, self))

class gitiFile(File):
    def __init__(self, V='.gitignore', ext=''):
        super().__init__(V, ext)

class jsonFile(File):
    def __init__(self, V, ext='.json', comment='//'):
        super().__init__(V, ext, comment=comment)

class mkFile(File):
    def __init__(self, V='Makefile', ext=''):
        super().__init__(V, ext)

class pyFile(File):
    def __init__(self, V, ext='.py', tab=' ' * 4):
        super().__init__(V, ext, tab=tab)


circ = Dir('circ')
Dir('.') // circ

giti = gitiFile()
circ // (giti
         // '*~' // '*.swp' // '*.log' // ''
         // '/pyvenv.cfg' // '/lib/python*/' // '/lib64' // '/share/python*/'
         // '/__pycache__/'
         // ''
         // '/circ/')

vscode = Dir('.vscode'); circ // vscode

autopep8 = '--ignore=E26,E302,E401,E402,E701,E702'

settings = jsonFile('settings'); vscode // settings

def multiCommand(fkey, target):
    return (S('{', '},')
            // f'"command": "multiCommand.{fkey}",'
            // (S('"sequence": [', ']')
                // '"workbench.action.files.saveAll",'
                // (S('{"command": "workbench.action.terminal.sendSequence",')
                    // f'"args": {{"text": "\\u000D clear ; make {target} \\u000D"}}}}')
                ))

def pyfiles():
    return (Sec('py')
            // '"**/__pycache__/**":true,'
            // '"**/bin/**":true,'
            // '"**/lib/**":true, "**/lib64/**":true,'
            // '"**/share/**":true, "**/include/**":true,'
            // '"**/pyvenv.cfg":true, "**/*.pyc":true,'
            )


settings \
    // (S('{', '}')
        // (Sec('py')
            // '"python.pythonPath"              : "./bin/python3",'
            // '"python.formatting.provider"     : "autopep8",'
            // '"python.formatting.autopep8Path" : "./bin/autopep8",'
            // f'"python.formatting.autopep8Args" : ["{autopep8}"],')
        // (Sec('multi')
            // (S('"multiCommand.commands": [', '],')
                // multiCommand('f11', 'test')
                // multiCommand('f12', 'all')
                ))
        // (Sec('files')
            // (S('"files.watcherExclude": {', '},') // pyfiles())
            // (S('"files.exclude": {', '},') // pyfiles())
            // (S('"files.associations": {', '},') // '"requirements.*": "config",')
            )
        // (Sec('editor')
            // '"editor.tabSize": 4,'
            // '"editor.rulers": [80],'
            // '"workbench.tree.indent": 32,')
        // '"browser-preview.startUrl": "127.0.0.1:12345/"'
        )

tasks = jsonFile('tasks'); vscode // tasks
extensions = jsonFile('extensions'); vscode // extensions
launch = jsonFile('launch'); vscode // launch

bin = Dir('bin'); circ // bin
bin // (gitiFile() // '*' // '!.gitignore')

doc = Dir('doc'); circ // doc
doc // (gitiFile() // '*' // '!.gitignore')

tmp = Dir('tmp'); circ // tmp
tmp // (gitiFile() // '*' // '!.gitignore')

mk = mkFile(); circ // mk
mk \
    // (Sec('var')
        // 'MODULE = $(notdir $(CURDIR))'
        // 'OS     = $(shell uname -s)'
        // 'NOW    = $(shell date +%d%m%y)'
        // 'REL    = $(shell git rev-parse --short=4 HEAD)'
        // 'CORES  = $(shell grep processor /proc/cpuinfo| wc -l)') \
    // (Sec('dir')
        // 'CWD    = $(CURDIR)'
        // 'BIN    = $(CWD)/bin'
        // 'DOC    = $(CWD)/doc'
        // 'TMP    = $(CWD)/tmp'
        )\
    // (Sec('tool')
        // 'CURL   = curl -L -o'
        // 'PY     = bin/python3'
        // 'PIP    = bin/pip3'
        // 'PEP    = bin/autopep8'
        // 'PYT    = bin/pytest'
        )\
    // (Sec('src')
        // 'P     += config.py'
        // 'S     += metaL.py test_metaL.py'
        # // 'S     += $(MODULE).py test_$(MODULE).py'
        )\
    // Sec('obj')\
    // Sec('cfg')\
    // (Sec('all')
        // '.PHONY: all' \
        // 'all: $(PY) metaL.py' \
        // '\t$^ $@' \
        // '\t$(MAKE) format' \
        // '.PHONY: test' \
        // 'test: $(PYT) test_metaL.py' \
        // '\t$^' \
        // '\t$(MAKE) format' \
        // '.PHONY: format' \
        // 'format: $(PEP)' \
        // '$(PEP): $(S)' \
        // f'\t$@ {autopep8} --in-place $? && touch $@' \
        )\
    // (Sec('doc') // S('doc:', pfx='.PHONY: doc'))\
    // (Sec('install')
        // '.PHONY: install'
        // 'install: $(OS)_install js doc'
        // '\t$(MAKE) $(PIP)'
        // '\t$(MAKE) update'
        // '.PHONY: update'
        // 'update: $(OS)_update'
        // '\t$(PIP) install -U    pip autopep8'
        // '\t$(PIP) install -U -r requirements.txt'
        // '.PHONY: Linux_install Linux_update'
        // 'Linux_install Linux_update:'
        // '\tsudo apt update'
        // '\tsudo apt install -u `cat apt.txt`'
        // (Sec('py')
            // '$(PY) $(PIP):' \
            // '\tpython3 -m venv .' \
            // '\t$(MAKE) update' \
            // '$(PYT):' \
            // '\t$(PIP) install -U pytest')\
        // (Sec('js') // S('js:', pfx='.PHONY: js'))\
        )\
    // Sec('merge')

apt = File('apt', '.txt'); circ // apt
apt // 'git make curl' // 'python3 python3-venv'

reqs = File('requirements', '.txt'); circ // reqs

py = pyFile('metaL'); circ // py

# print(circ)
circ.sync()
