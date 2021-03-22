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
* homoiconic self-modifying data structures
* metaprogramming via code generation

All `metaL` structures should be defined directly in the *host language*
(Python), and there is no syntax parser, as all you need for parsing you already
has in your compiler.

The idea of the `metaL` originates from an idea of the *generic code
templating*. Any mainstream programming language we're using any day at work or
for a hobby is limited by its vendors. If we want to use some features from cool
but low-used language, we can't do it because it is prohibited by our
contractors and teammates.

## Links


