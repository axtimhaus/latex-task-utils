# Some Utilities for Building Scientific LaTeX Documents Backed by Python Tasks

The focus lies on usage with [PyTask](https://pytask-dev.readthedocs.io), but this is not a strict requirement.
Code which requires PyTask is behind an try-import guard.

## Provided Modules

The modules are meant to be imported one-by-one as needed.

### `latex_task_utils.jinja`

Configure a Jinja environment with custom control sequences to avoid collision with LaTeX syntax. The default config is stored in `ENVIRONMENT_CONFIG` and the environment is obtained with `get_env(loader, **kwargs)`, where the `kwargs` override the default config.

### `latex_task_utils.matplotlib`

Configure Matplotlib to output figures suitable for LaTeX documents by applying a config with `use_default_config(overrides)` and optionally use a preamble file with `use_preamble(path)`.

The default config sets the figure size to 160 mm x 120 mm, the resolution to 600 dpi, configures some linewidths, uses constrained layout and lualatex/pgf as renderer.

If `pytask` is installed, a `FigureNode` class is provided which follows the `PPathNode` protocol an can be used to store a figure in multiple formats simultaneously. The figure is stored in the format defined by the main node path extension and additionally in those configured by `DEFAULT_FORMATS` or the `additional_formats` field of the node. For example with task returns:

```python
def task_plot_something() -> Annotated[Figure, FigureNode.from_path(Path("test.pdf"), ["png", "svg"])]:
    fig = plt.figure()
    ...
    return fig
```

### `latex_task_utils.symbols`

Define mathematical symbols in a TOML file and generate respective command definitions as well as a symbol index for LaTeX. This allows for single-source-of-truth definitions of your symbols. The commands are defined with `\gdef` to avoid creating groups around the symbols and thus make further sub- and superscripts work as with handwritten symbols (unlike other existing pure LaTeX packages like glossaries). These definitions also work usually without problems with the setups in scientific journals' production offices.

For flat symbol list use the following format:

```toml
SymI = { code = 'abc', doc = "A symbol." }
SymII = '\dot{#1}'
SymIII = { name = "Symbol 3", code = '\frac{#1}{#2}', doc = "Another symbol." }
```

For a categorized list the following:

```toml
doc = "The Root"

[symbols]

SymI = { code = 'abc', doc = "A symbol." }
SymII = '\dot{#1}'

[categories.CatI]
name = "Category 1"
doc = "SubCat"

[categories.CatI.symbols]
SymIII = { name = "Symbol 3", code = '\frac{#1}{#2}', doc = "Another symbol." }
```

The `doc`-strings and `name`s are used in the symbols index to describe the meaning of the symbol.
The key is used to generate the command name. Note that LaTeX does not allow numbers in command names. `#1`, `#2` and so on can be used to include mandatory arguments in the symbols.

The flat file will lead to the following command usage:

```latex
$\SymI$
$\SymII{something}$
$\SymIII{some}{other}$
```

The categorized file will lead to the following command usage:

```latex
$\SymI$
$\SymII{something}$
$\CatISymIII{some}{other}$
```

Load the symbols from file with the `read_toml(file)` function and generate:

- the command definitions with `write_symbols_sty(file, symbols)`
- the symbols index with `write_symbols_index(file, symbols, template, toplevel, heading)`.

```python
symbols = read_toml("symbols.toml")
write_symbols_sty("symbols.sty", symbols)
write_symbols_index(
    "symbols.sty",
    symbols,
    template=SymbolsIndexTemplates.DESCRIPTION, # optional
    toplevel=0, # optional
    heading="List of Symbols" # optional
)
```
