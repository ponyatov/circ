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
        if not self.value: return '\n'
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

class cssFile(File):
    def __init__(self, V, ext='.css', comment='//'):
        super().__init__(V, ext, comment=comment)

class htmlFile(File):
    def __init__(self, V, ext='.html', comment='//'):
        super().__init__(V, ext, comment=comment)

class mkFile(File):
    def __init__(self, V='Makefile', ext=''):
        super().__init__(V, ext)

class mdFile(File):
    def __init__(self, V, ext='.md'):
        super().__init__(V, ext)

class pyFile(File):
    def __init__(self, V, ext='.py', tab=' ' * 4):
        super().__init__(V, ext, tab=tab)

class erlFile(File):
    def __init__(self, V, ext='.erl', tab=' ' * 2):
        super().__init__(V, ext, tab=tab)

class exFile(File):
    def __init__(self, V, ext='.ex', tab=' ' * 2):
        super().__init__(V, ext, tab=tab)

class exsFile(exFile):
    def __init__(self, V, ext='.exs'):
        super().__init__(V, ext)


circ = Dir('circ')
Dir('.') // circ

MODULE = 'metaL'
TITLE = 'homoiconic [meta]programming [L]anguage / [L]ayer'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
GITHUB = f'http:///github.com/ponyatov/{MODULE}'

README = mdFile('README'); circ // README
README \
    // f'#  `{MODULE}`' \
    // f'## {TITLE}' \
    // '' \
    // f'(c) {AUTHOR} <<{EMAIL}>> 2020 MIT' \
    // '' \
    // f'github: {GITHUB}' \
    // '' \
    // '* object graph database' \
    // '* homoiconic metaprogramming language' \
    // '* web platform' \
    // '' \
    // '## Idea' \
    // '' \
    // '* take Lisp homoiconic nature and port it to Python stack (VM & libs)' \
    // '* provide light environment for generative metaprogramming (scripted code generation)' \
    // '  * writing programs that write other programs' \
    // '  * system bootstrap via metacircular definition' \
    // '  * automated source code generation for typical tasks' \
    // '* integrate best features from multiple languages:' \
    // '  * `Python` dynamics, readable syntax, lib batteries and ease of use' \
    // '  * `Erlang`/`Elixir` network-oriented programming: fault tolerance, fast light VM,' \
    // '    transparent clustering, bit arrays (for IoT)' \
    // '  * `Clojure` homoiconic extendable language' \
    // '  * `Smalltalk` message-based OOP' \
    // '' \
    // '### `metaL` is not a programming language' \
    // '' \
    // '`metaL` is a method of programming in Python, or any other language you prefer.' \
    // 'It works over two key features:' \
    // '* homoiconic self-modifying executable data structures (EDS)' \
    // '* metaprogramming via code generation' \
    // '' \
    // 'All `metaL` structures should be defined directly in the *host language*' \
    // '(Python), and there is no syntax parser, as all you need for parsing you already' \
    // 'has in your compiler.' \
    // '' \
    // 'The idea of the `metaL` originates from an idea of the *generic code'\
    // 'templating*. Any mainstream programming language we\'re using any day at work or'\
    // 'for a hobby is limited by its vendors. If we want to use some features from cool'\
    // 'but low-used language, we can\'t do it because it is prohibited by our'\
    // 'contractors and teammates.'\
    // '' \
    // 'The idea about code templating is a way of using the power of your own custom' \
    // 'language still having no incompatibles with your production team. In most cases,' \
    // 'nobody locks you on the IDE you use for development, so if you also add some' \
    // 'shadow tool that generates human-readable code in the mainstream language of' \
    // 'your team, you\'ll have a chance to use the power without the risks shown above.' \
    // '' \
    // '### Concept Programming' \
    // '' \
    // 'CP here is a programming model described in the works of Enn Heraldovich Tyugu' \
    // 'about model-based software development. It is not mean the term by Alexsandr' \
    // 'Stepanov here. The common idea is about making domain models describe the' \
    // 'problem in a wide in the form of relation networks, and automatic program (code)' \
    // 'synthesis from specifications to solve concrete tasks. This synthesis works over' \
    // 'these networks using them as generic knowledge representation.' \
    // '' \
    // '* http://www.cs.ioc.ee/~tyugu/' \
    // '  * Тыугу Э.Х. **Концептуальное программирование**.' \
    // '    М.: Наука, 1984. 255 с' \
    // '  * М.И.Кахро, А.П.Калья, Энн Харальдович Тыугу' \
    // '    **Инструментальная система программирования ЕС ЭВМ (ПРИЗ)**' \
    // '    М.: Финансы и статистика, 1988' \
    // '  * J. Symbolic Computation (1988) 5, 359-375\ The Programming System PRIZ [sym88]' \
    // '* Marvin Minsky [A Framework for Representing Knowledge](https://web.media.mit.edu/~minsky/papers/Frames/frames.html)' \
    // '' \
    // '## Links' \
    // '' \
    // ''

giti = gitiFile()
circ // (giti
         // '*~' // '*.swp' // '*.log' // ''
         // '/pyvenv.cfg' // '/lib/python*/' // '/lib64' // '/share/python*/'
         // '/include/site/python*/'
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

def pyFiles():
    return (Sec('py')
            // '"**/__pycache__/**":true,'
            // '"**/bin/**":true,'
            // '"**/lib/**":true, "**/lib64/**":true,'
            // '"**/share/**":true, "**/include/site/**":true,'
            // '"**/pyvenv.cfg":true, "**/*.pyc":true,'
            )

def exFiles():
    return (Sec('ex') // '"**/_build/**":true,')


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
            // (S('"files.watcherExclude": {', '},') // pyFiles() // exFiles())
            // (S('"files.exclude": {', '},') // pyFiles() // exFiles())
            // (S('"files.associations": {', '},') // '"requirements.*": "config",')
            )
        // (Sec('editor')
            // '"editor.tabSize": 4,'
            // '"editor.rulers": [80],'
            // '"workbench.tree.indent": 32,')
        // '"browser-preview.startUrl": "127.0.0.1:12345/"'
        )

tasks = jsonFile('tasks'); vscode // tasks

def vscodeTask(category, task):
    return S('{', '},') \
        // f'"label":          "{category}: {task}",' \
        // '"type":           "shell",' \
        // f'"command":        "make {task}",' \
        // '"problemMatcher": []'


tasks \
    // (S('{', '}')
        // '"version": "2.0.0",'
        // (S('"tasks": [', ']')
            // vscodeTask('project', 'install')
            // vscodeTask('project', 'update')
            ))

extensions = jsonFile('extensions'); vscode // extensions

extensions \
    // (S('{', '}')
        // (S('"recommendations": [', ']')
            // '"ryuta46.multi-command",'
            // '"stkb.rewrap",'
            // '"auchenberg.vscode-browser-preview",'
            // '// "tabnine.tabnine-vscode",'
            // '"ms-python.python",'
            // '// "betterthantomorrow.calva",'
            // '"pgourlain.erlang",'
            // '"jakebecker.elixir-ls",'
            ))

launch = jsonFile('launch'); vscode // launch

bin = Dir('bin'); circ // bin
bin // (gitiFile() // '*' // '!.gitignore')

doc = Dir('doc'); circ // doc
doc // (gitiFile() // '*' // '!.gitignore')

src = Dir('src'); circ // src
src // (gitiFile() // '!.gitignore')

tmp = Dir('tmp'); circ // tmp
tmp // (gitiFile() // '*' // '!.gitignore')

mk = mkFile(); circ // mk
mkAll = Sec('all')
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
        // 'ERL    = erl'
        // 'ERLC   = erlc'
        // 'MIX    = mix'
        // 'IEX    = iex'
        )\
    // (Sec('src')
        // 'P     += config.py'
        // 'S     += metaL.py test_metaL.py'
        # // 'S     += $(MODULE).py test_$(MODULE).py'
        )\
    // Sec('obj')\
    // Sec('cfg')\
    // (mkAll \
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
        ) \
    // (Sec('doc') \
        // (S('doc: \\', pfx='.PHONY: doc') \
            // 'doc/Armstrong_ru.pdf') \
        // (S('doc/Armstrong_ru.pdf:') \
        // '\t$(CURL) $@ https://github.com/dyp2000/Russian-Armstrong-Erlang/raw/master/pdf/fullbook.pdf') \
        ) \
    // (Sec('install')
        // '.PHONY: install'
        // 'install: $(OS)_install js doc'
        // '\t$(MAKE) $(PIP)'
        // '\t$(MAKE) update'
        // '.PHONY: update'
        // 'update: $(OS)_update'
        // '\t$(PIP) install -U    pip autopep8'
        // '\t$(PIP) install -U -r requirements.txt'
        // '\t$(MIX) deps.get'
        // '.PHONY: Linux_install Linux_update'
        // 'Linux_install Linux_update:'
        // '\tsudo apt update'
        // '\tsudo apt install -u `cat apt.txt apt.dev`'
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
apt \
    // 'git make curl' \
    // 'python3 python3-venv' \
    // 'erlang elixir' \
    // 'sqlite3'

aptdev = File('apt', '.dev'); circ // aptdev
aptdev \
    // 'sqlitebrowser'

reqs = File('requirements', '.txt'); circ // reqs
reqs // 'Flask' // 'Flask-SQLAlchemy'

py = pyFile('metaL'); circ // py
pytest = pyFile('test_metaL'); circ // pytest
pytest // 'def test_any(): assert True'

config = pyFile('config'); circ // config
config \
    // f'{"SECRET_KEY":<11} = {os.urandom(0x11)}' \
    // f'{"HOST":<11} = "127.0.0.1"' \
    // f'{"PORT":<11} = 12345'

static = Dir('static'); circ // static

css = cssFile('css'); static // css
css \
    // '* { background: #222; color: lightgreen; }'

templates = Dir('templates'); circ // templates

index = htmlFile('index'); templates // index

index // '{% extends "all.html" %}'

allhtml = htmlFile('all'); templates // allhtml
allhtml \
    // '<!DOCTYPE html>' \
    // (S('<html lang="ru">', '</html>')
        // (S('<head>', '</head>')
            // '<title>{{glob.head()}}</title>'
            // '<link rel="shortcut icon" href="/static/logo.png" type="image/png">'
            // '<meta charset="utf-8">'
            // '<meta http-equiv="X-UA-Compatible" content="IE=edge">'
            // '<meta name="viewport" content="width=device-width, initial-scale=1">'
            // '<link href="/static/js/bootstrap.min.css" rel="stylesheet">'
            // '<link href="/static/js/bootstrap.dark.css" rel="stylesheet">'
            // (S('<!--[if lt IE 9]>', '<![endif]-->')
                // '<script src="/static/js/html5shiv.min.js"></script>'
                // '<script src="/static/js/respond.min.js"></script>')
            // '<link href="/static/highlight.css" rel="stylesheet">'
            // '<link href="/static/css.css" rel="stylesheet">'
            // '{% block head %}{% endblock %}'
            )
        )

giti // '' // '*.beam'

erl = erlFile('hello'); src // erl
erl // '-module(hello).'

giti // '' // '/_build/' // '/deps/' // '/mix.lock'

formatter = exsFile('.formatter'); circ // formatter
formatter \
    // (S('[', ']')
        // 'inputs: ["{mix,.formatter}.exs", "{config,lib,test}/**/*.{ex,exs}"]')

mix = exsFile('mix'); circ // mix
mix \
    // (S('defmodule Metal.MixProject do', 'end')
        // 'use Mix.Project'
        // ''
        // (S('def project do', 'end') // (S('[', ']')
            // 'app: :metal,'
            // 'version: "0.0.1",'
            // 'elixir: "~> 1.11",'
            // 'deps: deps()'))
        // ''
        // (S('def application do', 'end') // (S('[', ']')
            // 'extra_applications: [:logger],'
            // 'mod: {Metal.Application, []}'))
        // ''
        // (S('defp deps do', 'end') // (S('[', ']')
            // '{:cowboy, "~> 2.8"},'
            // '{:exsync, "~> 0.2", only: :dev}'))
        )

mkAll \
    // (S('iex:', pfx='.PHONY: iex') // '$(IEX) -S $(MIX)')

# print(circ)
circ.sync()
