defmodule MetalTest do
  use ExUnit.Case
  doctest Metal

  test "greets the world" do
    assert Metal.hello() == :world
  end
end
