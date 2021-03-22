#  `metaL`
## homoiconic [meta]programming [L]anguage / [L]ayer

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT

github: http:///github.com/ponyatov/metaL

* object graph database
* homoiconic metaprogramming language
* web platform

## Idea

* take Lisp homoiconic nature and port it to Python stack (VM & libs)
* provide light environment for generative metaprogramming (scripted code generation)
  * writing programs that write other programs
  * system bootstrap via metacircular definition
  * automated source code generation for typical tasks
* integrate best features from multiple languages:
  * `Python` dynamics, readable syntax, lib batteries and ease of use
  * `Erlang`/`Elixir` network-oriented programming: fault tolerance, fast light VM,
    transparent clustering, bit arrays (for IoT)
  * `Clojure` homoiconic extendable language
  * `Smalltalk` message-based OOP

### `metaL` is not a programming language

`metaL` is a method of programming in Python, or any other language you prefer.
It works over two key features:
* homoiconic self-modifying executable data structures (EDS)
* metaprogramming via code generation

All `metaL` structures should be defined directly in the *host language*
(Python), and there is no syntax parser, as all you need for parsing you already
has in your compiler.

The idea of the `metaL` originates from an idea of the *generic code
templating*. Any mainstream programming language we're using any day at work or
for a hobby is limited by its vendors. If we want to use some features from cool
but low-used language, we can't do it because it is prohibited by our
contractors and teammates.

The idea about code templating is a way of using the power of your own custom
language still having no incompatibles with your production team. In most cases,
nobody locks you on the IDE you use for development, so if you also add some
shadow tool that generates human-readable code in the mainstream language of
your team, you'll have a chance to use the power without the risks shown above.

### Concept Programming

CP here is a programming model described in the works of Enn Heraldovich Tyugu
about model-based software development. It is not mean the term by Alexsandr
Stepanov here. The common idea is about making domain models describe the
problem in a wide in the form of relation networks, and automatic program (code)
synthesis from specifications to solve concrete tasks. This synthesis works over
these networks using them as generic knowledge representation.

* http://www.cs.ioc.ee/~tyugu/
* J. Symbolic Computation (1988) 5, 359-375\ The Programming System PRIZ [sym88]
* Marvin Minsky [A Framework for Representing Knowledge](https://web.media.mit.edu/~minsky/papers/Frames/frames.html)

## Links


