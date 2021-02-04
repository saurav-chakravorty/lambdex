<h1 style="text-align: center">lambdex</h1>

**lambdex** allows you to write multi-line anonymous function expression (called a _lambdex_) in an idiomatic manner. Below is a quick example of a recursive Fibonacci function:

```python
fib = def_(lambda n: [
    if_[n <= 0] [
        raise_[ValueError(f'{n} should be positive')]
    ],
    if_[n <= 2] [
        return_[1]
    ],
    return_[fib(n - 1) + fib(n - 2)]
])
fib(10)  # 55
```

Compared with ordinary lambda, which only allows single expression as body, lambdex may contain multiple "statements" in analogue to imperative control flows, whilst does not violate the basic syntax of Python.

<details open>
<summary> <em>Table of Content</em></summary>

- [More about lambdex](#more-about-lambdex)
- [Installation & Usage](#installation--usage)
- [Supported Features](#supported-features)
  - [Parameters](#parameters)
  - [Variable assignment](#variable-assignment)
  - [Conditional statement](#conditional-statement)
  - [Looping](#looping)
  - [With statement](#with-statement)
  - [Try statement](#try-statement)
  - [Yield statement](#yield-statement)
  - [Miscellaneous](#miscellaneous)
  - [Nested lambdexes](#nested-lambdexes)
  - [Bytecode caching](#bytecode-caching)
- [Declaration Disambiguity](#declaration-disambiguity)
- [Code Formatting](#code-formatting)
  - [Standalone lambdex formatter](#standalone-lambdex-formatter)
  - [Lambdex formatter as post-processor](#lambdex-formatter-as-post-processor)
  - [Mocking existing formatter executable](#mocking-existing-formatter-executable)
- [Known Issues & Future](#known-issues--future)
- [Q & A](#q--a)
- [License](#license)
</details>

## More about lambdex

An anonymous function is a function definition that is not bound to an identifier, which is ubiquitous in most languages with first-class functions. The language feature could be handy for logics that appear to be short-term use, and therefore adopted widely in some functional programming paradigms.

Python provides `lambda <arg>: <expr>` for such purpose. Lambdas are good for simple functionalities, but appear limited if logical complexity goes up. Consequently, higher-order functions (e.g., decorators) are often implemented as nested named functions, which is not concise enough.

**lambdex** as an experimental complement to lambdas, aims to provide a syntax similar to Python for anonymous functions. The syntax itself is built upon valid Python expressions, and therefore requires no modification to the interpreter. This package transpiles lambdexes into Python bytecodes at runtime, and therefore ensures the efficiency.

## Installation & Usage

Currently you can install **lambdex** from Github by:

```bash
pip install git+https://github.com/hsfzxjy/lambdex
```

The package will be available on PyPI once it's stablized.

To use lambdex, a simple import is required:

```python
from lambdex import def_

my_sum = def_(lambda a, b: [
    return_[a + b]
])
```

That's it! You don't even need to import other keywords such as `return_`.

## Supported Features

We are going to explore a wide range of features supported by **lambdex** in the following sections.

### Parameters

The parameter declaration of lambdexes appears after the `lambda`. The syntax supports most variants of declaration just as ordinary functions.

<details>
    <summary><em>show code</em></summary>

```python
# ordinary parameters
def_(lambda a, b: [...])

# parameters with default values
def_(lambda a, b=1: [...])

# starred arguments
def_(lambda *args, **kwargs: [...])

# keyword-only arguments
def_(lambda *, a, b: [...])

# positional-only arguments (Python 3.8+)
def_(lambda a, b, /: [...])
```

</details>

### Variable assignment

Lambdexes use `<` instead of `=` for assignments, since `=` in Python is valid only in statements.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    foo < "bar",
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    foo = "bar"
```

</details>

`<` is chainable like ordinary `=`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    foo < baz < "bar",
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    foo = baz = "bar"
```

</details>

Note that `<` has a higher precedence than `not`, `and`, `or` and `if...else...`. R-value with these operators should be enclosed by parentheses:

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    foo < (a or b and not c),
    foo < (a if cond else b),
])
```

</details>

In Python 3.8 or above, the walrus operator `:=` might also be used. But be careful that Python enforces parentheses around `:=` in many cases.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    foo := "bar",           # OK
    foo := baz := "bar",    # syntax error
    foo := (baz := "bar"),  # syntax error
    if_[condition] [
        foo := "bar",       # syntax error
        (foo := "bar"),     # OK
    ]
])
```

</details>

### Conditional statement

Lambdexes use `if_`, `elif_` and `else_` for conditional control flows.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    if_[condition_1] [
        ...,
    ].elif_[condition_2] [
        ...,
    ].else_[
        ...,
    ]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    if condition_1:
        ...
    elif condition_2:
        ...
    else:
        ...
```

</details>

### Looping

Lambdexes support the two kinds of looping by keywords `for_` and `while_`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    # for...in...else...
    for_[i in range(10)] [
        print_(i),
    ].else_[
        print("the optional else clause"),
    ],

    # while...else...
    while_[condition] [
        ...,
    ].else_[
        print("the optional else clause"),
    ]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    # for...in...else...
    for i in range(10):
        print(i)
    else:
        print("the optional else clause")

    # while...else...
    while condition:
        print("the optional else clause")
```

</details>

`break_` and `continue_` are also supported.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    for_[i in range(10)] [
        if_[i >= 5] [
            break_
        ].else_[
            continue_
        ]
    ]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    for i in range(10):
        if i >= 5:
            break
        else:
            continue
```

</details>

### With statement

With statements are supported by the `with_` keyword. The optional `as` aliasing is written using `>`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    # simple `with`
    with_[open("foo")] [
        ...
    ]

    # `with` with aliasing
    with_[open("foo") > fd] [
        ...
    ]

    # multiple `with`, equiv to
    with_[open("foo"), open("bar") > fd] [
        ...
    ]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    # simple `with`
    with open("foo"):
        ...

    # `with` with aliasing
    with open("foo") as fd:
        ...

    # multiple `with`, equiv to
    with open("foo"), open("bar") as fd:
        ...
```

</details>

### Try statement

The ordinary try statements are supported by keywords `try_`, `except_`, `else_` and `finally_`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    try_[
        ...
    ].except_[RuntimeError] [
        ...
    ].except_[
        ...
    ].else_[
        ...
    ].finally_[
        ...
    ]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    try:
        ...
    except RuntimeError:
        ...
    except:
        ...
    else:
        ...
    finally:
        ...
```

</details>

The optional `as` in `except` clause is written as `>`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    try_[
        ...
    ].except_[RuntimeError > e] [
        ...
    ]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    try:
        ...
    except RuntimeError as e:
        ...
```

</details>

### Yield statement

The `yield` and `yield...from...` structures are supported by keywords `yield_` and `yield_from_`. A lambdex contains one or more `yield_` or `yield_from_` will automatically become a generator.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    yield_[1, 2],
    yield_from_[range(3, 10)],
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    yield (1, 2)
    yield from range(3, 10)
```

</details>

`yield_` itself is an expression, and thus can appear in anywhere an expression is allowed. Note that parentheses might be added.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    a < (yield_),

    if_[a < (yield_)] [...],

    with_[(yield_) > cm] [...],

    for_[i in (yield_)] [...]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    a = (yield)
    if a < (yield): ...
    with (yield) as cm: ...
    for i in (yield): ...
```

</details>

### Miscellaneous

Lambdexes support some other keywords in Python too.

The `return_` is analogue to keyword `return`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    return_[a, b]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    return a, b
```

</details>

The `pass_` is analogue to keyword `pass`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    pass_
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    pass
```

</details>

The `raise_` is analogue to keyword `raise`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    try_[
        raise_[RuntimeError]
    ].except_[ValueError > e] [
        # the optional from clause
        raise_[RuntimeError].from_[e]
    ].except_[
        # the bare raise
        raise_
    ]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    try:
        raise RuntimeError
    except ValueError as e:
        raise RuntimeError from e
    except:
        raise
```

</details>

The `global_` and `nonlocal_` are analogue to keywords `global` and `nonlocal`.

<details open>
    <summary><em>show code</em></summary>

```python
def_(lambda: [
    global_[a],

    return_[def_(lambda: [
        nonlocal_[a],
    ])]
])
```

</details>
<details>
    <summary><em>show equivalent function</em></summary>

```python
def anonymous():
    global a

    def _inner():
        nonlocal a

    return _inner
```

</details>

### Nested lambdexes

Lambdexes can be nested to construct more complicated logics. Lambdexes regard the nested scoping rules in Python, i.e., inner lambdex captures names defined in its parent scopes. For example, we can define [IIFE](https://en.wikipedia.org/wiki/Immediately_invoked_function_expression) like in JavaScript to capture looping variables.

<details open>
    <summary><em>show code</em></summary>

```python
# without IIFE
arr = []
for i in range(10):
    arr.append(def_(lambda: [
        print(i)
    ]))
for func in arr:
    func()  # print "9" x10 times

# with IIFE
arr = []
for i in range(10):
    func = def_(lambda i: [
        return_[def_(lambda: [
            print(i)
        ])]
    ])(i)
    arr.append(func)
for func in arr:
    func()  # print from "0" to "9"
```

</details>

### Bytecode caching

Each lambdex will be compiled at the time `def_(...)` is executed, and only compiled once. The bytecode of lambdex will be cached and reused in the future execution.

As an example below, each call of `foo()` returns a new lambdex object, with different closures but the same code object.

```python
def foo():
    a = 1
    return def_(lambda: [
        a < a + 1,
        return_[a],
    ])

f1 = foo()
f2 = foo()
f1()  # 2
f2()  # 2
f1.__code__ is f2.__code__  # True
```

The feature ensures no redundant computation is done when compiling lambdexes sharing the same lexical context.

## Declaration Disambiguity

We are going to discuss an edge case in this section.

Suppose you are running the following code:

```python
f1, f2 = def_(lambda a, b: [return_[a + b]]), def_(lambda a, b: [return_[a * b]])
```

The code yields an exception `SyntaxError: Ambiguious identifier None`.

What's going on here? The problem is that **there are more than one lambdexes defined on the same line**. Since CPython provides no effective way but a line number for locating a given lambda, the lambdex compiler fails to obtain the source code of the lambda in this case. A workaround is to prepend an identifier after `def_` of lambdex:

```python
f1, f2 = def_.f1(lambda a, b: [return_[a + b]]), def_.f2(lambda a, b: [return_[a * b]])
```

With this, the compiler can now tell them from each other.

In the example above, it's not necessary to add identifier for both lambdexes. The following is also acceptable, as long as their declarations are different:

```python
f1, f2 = def_.f1(lambda a, b: [return_[a + b]]), def_(lambda a, b: [return_[a * b]])
```

## Code Formatting

The proposed lambdex syntax violates the convention of most code formatters. In order to keep the code tidy, this library provides a light-weight formatter **lxfmt** for lambdex syntax, which can either work standalonely or cooperate with existing formatters.

Here's an example of what **lxfmt** does:

<details open>
    <summary><em>show code</em></summary>

```python
from lambdex import def_

def f():
    return def_.myfunc(  # comment1
        lambda a, b:   [# comment2
  if_[condition] [
      f2 < def_(lambda:[a+b]),
      return_[f2],
            ],try_[# comment3
      body,
  ].except_[Exception > e] [
      except_handler
  ] # comment4
  ,         ],# comment5
        )
```

</details>

<details open>
    <summary><em>show code</em></summary>

```python
from lambdex import def_


def f():
    return def_.myfunc(lambda a, b: [  # comment1
        # comment2
        if_[condition] [
            f2 < def_(lambda: [
                a+b
            ]),
            return_[f2],
        ],
        try_ [  # comment3
            body,
        ].except_[Exception > e] [
            except_handler
        ],  # comment4
        # comment5
    ])
```

</details>

### Standalone lambdex formatter

The usage of standalone **lxfmt** is shown below:

```
usage: lxfmt [-h] [-d | -i | -q] [-p] [files [files ...]]

Default formatter for lambdex

positional arguments:
  files           reads from stdin when no files are specified.

optional arguments:
  -h, --help      show this help message and exit
  -d, --diff      print the diff for the fixed source
  -i, --in-place  make changes to files in place
  -q, --quiet     output nothing and set return value
  -p, --parallel  run in parallel when formatting multiple files.
```

For example, use `lxfmt -i file.py` to format in-place, or `lxfmt -d file.py` to show the difference before and after formatting.

### Lambdex formatter as post-processor

**lxfmt** can work as a post-processor of existing formatter, such as [yapf](https://github.com/google/yapf). One can specify a formatter backend by prepending `-- -b BACKEND` to the command. The overall usage is shown below:

```
usage: lxfmt [ARGS OF BACKEND] -- [-h] [-b BACKEND] [-e EXECUTABLE]

Lambdex formatter as a post-processor for specific backend

optional arguments:
  -h, --help            show this help message and exit
  -b BACKEND, --backend BACKEND
                        name of formatter backend (default: dummy)
  -e EXECUTABLE, --executable EXECUTABLE
                        executable of backend
```

**Note that `[ARGS OF BACKEND]` are the arguments fed to the specified backend.**

For example, to use **lxfmt** after **yapf**, with yapf style configuration at `~/.config/yapf/style`, one may use:

```bash
lxfmt file.py --style ~/.config/yapf/style -- -b yapf
```

_Currently **lxfmt** supports only yapf. Adapters for other formatters will be added in the future._

### Mocking existing formatter executable

The `-- -b BACKEND` appears to be verbose, and sometimes you may want to alias the command of "formatter backend + post-processor" to save the typing work. The library provides another tool `lxfmt-mock` to do the job.

```
usage: lxfmt-mock [-h] [-r] BACKEND

Mock or reset specified formater backend

positional arguments:
  BACKEND      The backend to be mocked/reset

optional arguments:
  -h, --help   show this help message and exit
  -r, --reset  If specified, the selected command will be reset
```

For example, running `lxfmt-mock yapf`, the tool will search for and list out available yapf executables to be mocked:

```bash
$ lxfmt-mock yapf
[?] Which one do you want to mock?:
 ❯ /home/me/.local/bin/yapf
   /usr/data/anaconda3/bin/yapf
```

By choosing a executable, e.g. `/home/me/.local/bin/yapf`, `/home/me/.local/bin/yapf <args>` will become a shorthand for `lxfmt <args> -- -b yapf -e /home/me/.local/bin/yapf`. The original executable will be stored at `/home/me/.local/bin/original_yapf`.

To reset a mocked executable, simply run `lxfmt-mock yapf -r` and choose from the list.

Mocking a formatter backend could be very useful when you want to enable lambdex code formatting in your IDE/editor. By mocking the executable your IDE/editor uses, you can enjoy the feature on the fly without modifying any settings.

## Known Issues & Future

Currently lambdex doesn't support:

1. coroutines (async functions)
2. augmented assignments like `+=`, `-=`, etc.
3. type annotation
4. `import` statements
5. executed in an REPL environment

Coroutines [1] support is guaranteed to add in the future. Augmented assignments [2] support is planned, but no suitable solution for the operators yet.

Type annotation [3] and `import` statements [4] will not be supported.

REPL [5] support will be available if there's any workaround to obtain the source code, since the compiler requires the code for further parsing.

Lambdexes also violate linters, which is inevitable.

Besides, the upcoming versions will:

- improve the error message of compilation failures or runtime panics;
- make keywords and operators customizable;
- add style options for **lxfmt**

, in order to provide a better developing experience.

## Q & A

**Why using brackets "[]" to enclose statement heads and bodies instead of parentheses "()"?**

Brackets are easier to type than parentheses on most of the keyboards.

---

**Why using "<" and ">" for assignment and aliasing?**

The design is from three considerations. _1)_ Comparators such as "<", "<=", ">" or ">=" [have lower precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence) than most of the other operators, thus allowing R-values without parentheses for most of the time; _2)_ in AST representation, chained comparators have a flat structure, which is easier to parse; _3)_ "<" and ">" visually illustrate the direction of data flows.

The preference of "<" ">" over "<=" "=>" is that the previous ones consume only one character and are easier to type. Options may be included in the future to allow customized operators.

---

**Lambdex appears to be less readable than functions and will mess up my code. Why should I use it?**

The project is not to criticize the present design of Python, but an experimental attempt to provide alternative for the ones who need a better anonymous function expression. The need may be from a second language they are familiar with, or the paradigms they want to use.

**lambdex** decides not to perform any modification on the interpreter, but build the new syntax upon existing Python syntax. The choice determines that keywords should be aliased and artifacts like "[]" would appear everywhere, which reduces the readability. To mitigate this, **lambdex** is paying effort to make the lambdex syntax resemble the Python syntax.

It is true that there's a trade-off between readability and functionality. The decision should depend on your own requirements.

---

**What's the magic behind lambdex?**

`def_` or `def_.<ident>` are actually callables, which take a lambda object as input, transpile it into an ordinary function and then return. The definition is in [lambdex.keywords](lambdex/keywords.py) module.

The transpilation process can be roughly separated into three stages.

In the first stage, we try to find the source code of given lambda object and parse it into AST. Source code searching is performed by [lambdex.utils.ast::ast_from_source](lambdex/utils/ast.py#L59), which is modified from _inspect.getsourcelines_ to work more robust on lambdas. The obtained source is parsed into AST, which then pattern-matched to locate the Lambda node. The entry of this stage is [lambdex.ast_parser::lambda_to_ast](lambdex/ast_parser.py#L43).

In the second stage, we traverse the AST of lambda object, replacing some node patterns with correponding Python statements, recursively building up the body of new function. Inner lambdexes are detached from where they lay, and become nested functions within the constructed body. This part is at [lambdex.compiler.dispatcher](lambdex/compiler/dispatcher.py) and [lambdex.compiler.rules](lambdex/compiler/rules.py).

In the last stage, we compile the new AST into code object, restore metadata (globals, closures, etc.) from the original lambda object, and wrap it by a Function object. Modification might be applied to AST to correct the compilation result, e.g., wrap AST in a dummy function to make specific names nonlocal instead of global. This is done in [lambdex.compiler.core::compile_lambdex](lambdex/compiler/core.py#L70). Bytecode caching also happens in this stage.

For better understanding, you may look into the source code and check the detailed implementation.

## License

Copyright (c) 2021 Jingyi Xie (hsfzxjy). Licensed under the [GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0).
