defmodule Metal.MixProject do
  use Mix.Project

  def project do
    [
      app: :metal,
      version: "0.0.1",
      elixir: "~> 1.11",
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:sasl, :logger],
      mod: {Metal, []}
    ]
  end

  defp deps do
    [
      {:cowboy, "~> 2.8"},
      {:exsync, "~> 0.2", only: :dev}
    ]
  end
end
