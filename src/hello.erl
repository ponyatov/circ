-module(hello).
-export([world/0]).
-compile(export_all).
-on_load(reload/0).

reload() -> ok.

world() -> "World".
