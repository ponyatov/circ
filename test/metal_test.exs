defmodule MetalTest do
  use ExUnit.Case

  test "greets the world" do
    assert Metal.hello() == :world
  end

  test "greets Erlang" do
    assert :hello.world() == 'World'
  end
end
