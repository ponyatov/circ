-module(hello).
-export([world/0]).
-on_load(reload/0).

reload() -> ok.

world() -> "World".
