---
layout: post
title: "Why You Should Upgrade Now: All The New Goodness In Python 3.11"
date: 2022-10-26 12:00:00 +0200
categories: python
comments: true
published: true
excerpt: |
  The new Python 3.11 release is out and brings some nice new features and functionality. This overview lists the 
  most important changes to convince you to upgrade your Python.
image_url: /assets/images/unsplash/anders-jilden--N2UXcPBIYI-unsplash-2.jpg
image_description: |
  Photo by [anders jilden](https://unsplash.com/@zhangkaiyv?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/s/photos/skyline?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

The [new release](https://docs.python.org/3.11/whatsnew/3.11.html#) brings advancements to exceptions and exception
handling in Python, a new module for handling TOML files, improvements for the interpreter, new types and features, and
also deprecates some older modules and APIs of the language. Additionally, Python benchmarks claim that Python 3.11 is
between 10-60% faster than Python 3.10: you can see the results
[here](https://github.com/faster-cpython/ideas#published-results).

## How To Install And Upgrade

### Linux

On Linux (in this case: Ubuntu) you can install and update Python via the local package manager. You can use the
[deadsnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa) to install the most recent built versions of
Python.

```sh
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
```

After adding the repository you can install Python 3.11 via apt:

```sh
sudo apt-get update
sudo apt-get install python3.11
```

### macOS

On macOS, I recommend using the package manager [homebrew](https://brew.sh). You can install homebrew via:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installing homebrew, you can install Python 3.11:

```sh
brew install python@3.11
```

Or if you already installed an earlier version of Python via homebrew (and updated the package manager itself), upgrade
your Python package to version 3.11 via this command:

```sh
brew upgrade python -v 3.11
```

### Windows

On Windows, you have two methods to update Python: via the Python installer or the [Chocolatey](https://chocolatey.org)
package manager. You find the Python installer on the official [download page](https://www.python.org/downloads/) and it
will step you right through the process. If you want to use the package manager Chocolatey, you can install it via:

```sh
Set-ExecutionPolicy Bypass -Scope Process -Force; \
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

Then you can use Chocolatey to install Python 3.11 via command line:

```sh
choco install python -y --version 3.11
```

Or you upgrade Python if already installed:

```sh
choco upgrade python -y --version 3.11
```

## Exception Groups, Except*, And Notes

Multiple unrelated exceptions can now be raised and handled simultaneously. The newly introduced type `ExceptionGroup`
can bundle unrelated exceptions:

```python
exceptions = ExceptionGroup(
    "all",
    [
        TypeError(1),
        ExceptionGroup("ex", [TypeError(2), ValueError(3)]),
        ExceptionGroup("os", [OSError(4)])
    ]
)
```

These bundles give pretty printed hierarchies:

```python
import traceback
traceback.print_exception(exceptions)
```

```sh
  | ExceptionGroup: all (3 sub-exceptions)
  +-+---------------- 1 ----------------
    | TypeError: 1
    +---------------- 2 ----------------
    | ExceptionGroup: ex (2 sub-exceptions)
    +-+---------------- 1 ----------------
      | TypeError: 2
      +---------------- 2 ----------------
      | ValueError: 3
      +------------------------------------
    +---------------- 3 ----------------
    | ExceptionGroup: os (1 sub-exception)
    +-+---------------- 1 ----------------
      | OSError: 4
      +------------------------------------
```

You can use match conditions on these ExceptionGroups, you can subclass them, build your own handlers for
[handling](https://peps.python.org/pep-0654/#handling-exception-groups) so-called leaf exceptions, and much more.

Python 3.11 introduces a new (or enhanced) keyword for easier working with ExceptionsGroups: `except*`. The * character 
shall indicates that multiple exceptions can be handled:

```python
try:
    ...
except* CustomError:
    ...
except* OSError as e:
    ...
except* (TypeError, ValueError) as e:
    ...
```

The description of [PEP-0654](https://peps.python.org/pep-0654/) provides additional
[documentation](https://peps.python.org/pep-0654/#except) for the new `except*` keyword, for example
[recursive matching](https://peps.python.org/pep-0654/#recursive-matching),
[raising exceptions in a except* block](https://peps.python.org/pep-0654/#raising-exceptions-in-an-except-block), or
[chaining](https://peps.python.org/pep-0654/#chaining).

The base class of exceptions [`BaseException`](https://docs.python.org/3.11/library/exceptions.html#BaseException)
became a new method, too. This method was added because additional information can be added when exceptions are caught
and re-raised.

> `add_note(note)`
> 
> Add the string `note` to the exception’s notes which appear in the standard traceback after the exception string. A
> [`TypeError`](https://docs.python.org/3.11/library/exceptions.html#TypeError) is raised if `note` is not a string.

## Welcome The New Module: tomllib

Tom's Obvious Minimal Language ([TOML](Tom's Obvious Minimal Language)) is intended to be a configuration file format
that is minimal and easy to read. The syntax is similar to INI-files - but it provides an actual standard, whereas INI
comes in many flavors. TOML supports a variety of data types: String, Integer, Float, Boolean, Datetime, Array, and
Table. Because it consists of key-value-pairs, it structure parses comfortably into a hash map. The following is a
minimal example:

```toml
# this is a TOML config file example

title = "Config"

[general]
name = "Database"
created = 2022-11-26T08:30:00+02:00

[database]

  [database.connection]
  server = "192.168.1.1"
  ports = [ 8000, 8001, 8002 ]

  [database.auth]
  username = "root"
  password = "root"
```

Now Python 3.11 adds a module to the standard library to parse TOML files called
[tomllib](https://docs.python.org/3.11/library/tomllib.html#module-tomllib). Unfortunately at this point the module
only supports parsing TOML files, but not writing them. There are two alternatives suggested if you need the writing
capabilities: the [Tomli-W](https://pypi.org/project/tomli-w/) package and the
[TOML Kit](https://pypi.org/project/tomlkit/) package.

However, if you just need to read a TOML file, you can use the new module from the standard library. Be aware that any
TOML file must be opened in binary mode so that `tomllib` can handle UTF-8 encoding
[correctly](https://peps.python.org/pep-0680/#types-accepted-as-the-first-argument-of-tomllib-load) on all systems. The
following example shows how you could parse our example TOML file from above:

```python
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

    server = config['database']['connection']['server']
    for port in config['database']['connection']['ports']:
        print(f'{server}:{port}')
```

You can find additional tips and tricks for working with the `tomllib` module in
[RealPython's article](https://realpython.com/python311-tomllib/#tomllib-toml-parser-in-python-311), for example
specifying a float method to control how floating-point numbers are parsed and represented.

## Interpreter Improvements

Python 3.11 catches up with the capabilities of more modern compilers and will now also point out the
[specific expression](https://docs.python.org/3.11/whatsnew/3.11.html#whatsnew311-pep657) that caused the error instead
of just pointing to the line:

```sh
Traceback (most recent call last):
  File "distance.py", line 11, in <module>
    print(manhattan_distance(p1, p2))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "distance.py", line 6, in manhattan_distance
    return abs(point_1.x - point_2.x) + abs(point_1.y - point_2.y)
                           ^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'x'
```

Additionally there is a new command line option `-P` which - together with an environment variable called
[`PYTHONSAFEPATH`](https://docs.python.org/3.11/using/cmdline.html#envvar-PYTHONSAFEPATH) - disables automatically
prepending potentially unsafe paths to [`sys.path`](https://docs.python.org/3.11/library/sys.html#sys.path). This is a
feature which can be integrated in your Continuous Integration environment to ensure safety and portability.

> `-P`
>
> Don’t prepend a potentially unsafe path to [`sys.path`](https://docs.python.org/3.11/library/sys.html#sys.path):
>
> `python -m module` command line: Don’t prepend the current working directory.
>
> `python script.py` command line: Don’t prepend the script’s directory. If it’s a symbolic link, resolve symbolic
> links.
>
> `python -c code` and `python` (REPL) command lines: Don’t prepend an empty string, which means the current working
> directory.
>
> See also the [`PYTHONSAFEPATH`](https://docs.python.org/3.11/using/cmdline.html#envvar-PYTHONSAFEPATH) environment
> variable, and [`-E`](https://docs.python.org/3.11/using/cmdline.html#cmdoption-E) and
> [`-I`](https://docs.python.org/3.11/using/cmdline.html#cmdoption-I) (isolated) options.


## More Types And Type Features

The new release brings new typing features. They are shown briefly in the following sections.

### Variadic generics

Python 3.5 already brought `TypeVar` for generics parameterized with a single type. Python 3.11 brings `TypeVarTuple`
which allows for parameterization with an arbitrary number of types. The following example is from
[PEP-646](https://peps.python.org/pep-0646/) and shows the usage of this new feature:

```python
from typing import TypeVar, TypeVarTuple

DType = TypeVar('DType')
Shape = TypeVarTuple('Shape')

class Array(Generic[DType, *Shape]):

    def __abs__(self) -> Array[DType, *Shape]: ...
    def __add__(self, other: Array[DType, *Shape]) -> Array[DType, *Shape]: ...
```

```python
from typing import NewType

Height = NewType('Height', int)
Width = NewType('Width', int)

x: Array[float, Height, Width] = Array()
```

### Marking individual TypedDict items as required or not-required

Now individual items in a `TypedDict` can be marked if they must be present or not. By default all fields are still
required for backwards compatibility. However, there is also a `total` parameter which can be set to `False`: in this
case all fields of the `TypedDict` are not-required by default.

```python
class Movie(TypedDict):
   title: str
   year: NotRequired[int]

m1: Movie = {"title": "Black Panther", "year": 2018}  # OK
m2: Movie = {"title": "Star Wars"}  # OK (year is not required)
m3: Movie = {"year": 2022}  # ERROR (missing required field title)
```

### Self type

[PEP-673](https://peps.python.org/pep-0673/) introduces the `Self` annotation for methods which return an instance of
their class. The following example shows a use case for an alternative constructor:

```python
class MyInt:
    @classmethod
    def fromhex(cls, s: str) -> Self:
        return cls(int(s, 16))
```

### Arbitrary literal string type

Python 3.11 introduces a new annotation for additional safety regarding strings:
[`LiteralString`](https://docs.python.org/3.11/library/typing.html#typing.LiteralString). This annotation allows
functions to accept arbitrary literal string types, as well as strings created from other literal strings. You can
enforce requirements for sensitive functions, such as those that execute SQL statements for protection against SQL
injection attacks.

The according [PEP-675](https://peps.python.org/pep-0675/) shows how this annotation can be used for SQL queries:

```python
def run_query(sql: LiteralString) -> ...
    ...

def caller(
    arbitrary_string: str,
    query_string: LiteralString,
    table_name: LiteralString,
) -> None:
    run_query("SELECT * FROM students")       # ok
    run_query(query_string)                   # ok
    run_query("SELECT * FROM " + table_name)  # ok
    run_query(arbitrary_string)               # type checker error
    run_query(                                # type checker error
        f"SELECT * FROM students WHERE name = {arbitrary_string}"
    )
```

## The Old Must Go: Deprecations

The following legacy standard library modules have been deprecated and will be removed in Python 3.13:

- `aifc`
- `chunk`
- `msilib`
- `pipes`
- `telnetlib`
- `audioop`
- `crypt`
- `nis`
- `sndhdr`
- `uu`
- `cgi`
- `imghdr`
- `nntplib`
- `spwd`
- `xdrlib`
- `cgitb`
- `mailcap`
- `ossaudiodev`
- `sunau`

Additionally, `asynchat`, `asyncore` and `smtpd` modules (who have been deprecated already) have been updated to note
that they will be removed in Python 3.12. Also the `lib2to3` package and `2to3` tool are now deprecated and may not be
able to parse Python 3.10 or newer. The undocumented modules `sre_compile`, `sre_constants` and `sre_parse` are now also
deprecated.

The [Py_UNICODE](https://docs.python.org/3.11/c-api/unicode.html#c.Py_UNICODE)  encoder APIs have been
[removed](https://docs.python.org/3.11/whatsnew/3.11.html#whatsnew311-pep624) because they were already deprecated and
not used much anymore since there are better and more efficient alternatives. If you are still using those APIs, the
according [PEP-624](https://peps.python.org/pep-0624/) provides a migration guide.

Some macros have been converted to static inline functions to avoid
[macro pitfalls](https://gcc.gnu.org/onlinedocs/cpp/Macro-Pitfalls.html). You can find additional information on these
macros in the related [PEP-670](https://peps.python.org/pep-0670/).

## Conclusion

The new [Python release 3.11](https://docs.python.org/3.11/whatsnew/3.11.html#) brings a lot new and good stuff: better
performance, more possibilities for exception handling, a new module for parsing TOML files, interpreter improvements,
additional types, annotations, and type features, as well as the deprecations and removal of some older language
baggage.

Decide for yourself, if this is worth upgrading, but most of all: keep on coding and keep on creating!
