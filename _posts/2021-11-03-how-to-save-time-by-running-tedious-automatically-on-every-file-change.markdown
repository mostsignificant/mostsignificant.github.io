---
layout: post
title: "How to Save Time by Running Tedious Tasks Automatically on Every File Change with entr"
date: 2021-12-12 17:00:00 +0200
categories: automation
comments: true
published: true
excerpt: |
  If you recompile often when writing software then you might tlike this little timesaver: automatically running a
  command whenever a file changes in a given file directory.
image_url: /assets/images/unsplash/jenil-gogari-2JZ9Q24f82g-unsplash-2.jpg
image_description: |
  Photo by [Jenil Gogari](https://unsplash.com/@jgog?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/s/photos/timelapse?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

## Introducing entr

Let me introduce you to a tool called [`entr`][1]. This tool uses [kqueue][2] and [inotify][3] to watch for file changes
and is able to execute arbitrary commands. This allows us to run all kinds of commands during software development when
source or configuration files change, for example:

- build commands
- test commands
- restarting a server

You can also use it to set up a whole automation workflow. However, be aware of the increased complexity when chaining
`entr` commands and their triggers together. I prefer to keep it simple and set the tool up as helpful helper to save me
some time. And to get rid of repetitive, monotonous tasks. Because I don't like repetitive, monotonous tasks.

## Installation

On Linux use your package manager to install `entr` if not already installed:

```shell
sudo apt-get install entr
```

On Mac you can install `entr` with the [Homebrew][4] package manager:

```shell
brew install entr
```

Or you clone from its [GitHub repository][5] and build from source:

```shell
./configure
make test
make install
```

Unfortunately I could not test a solution for Windows, but the respository's [README][6] mentions Windows and the WSL -
which might be a reasonable workaround because inotify and kqueue do not exist within the Microsoft universe.

## Usage

The `entr` tool offers a few options, as you can see from its synopsis:

```shell
entr [-acdnprsz] utility [argument /_ ...]
```

You can pipe the output of a command into entr to trigger a command, for example launching and and auto-reloading a
node.js server whenever a Javascript file changes within the current directory:

```shell
ls *.js | entr -r node app.js
```

I had problems with the combination of the `ls` command and `entr` on Mac OS so I used the `find` command. The `find`
command offers additional options for filtering which proved useful.

### CMake Build and Test Example

Run from your build directory and use the `-s` option to pass chained commands:

```shell
find .. -name "*.h" -o -name "*.cc" | entr -s 'cmake --build . && ctest'
```

This command will watch changes in header or implementation files and start a build via CMake plus CTest run on success.

### Cargo Build and Test Example

Run from your main directory and use the `-s` option to execute cargo build and test:

```shell
find .. -name "*.rs" | entr -s 'cargo build && cargo test'
```

### Run a Single Python File

Execute a single Python file if this file changes by piping the `echo` command into `entr`:

```shell
echo main.py | entr python main.py
```

## Command Manual

You can have a look at the manual to see all available options: [`man entr`][7]. I found the following options the most
useful:

- `-c` to clear the console and not having to scroll through old command output
- `-r` to reload a whole process if something changes, for example a web server
- `-s` to execute more complicated commands

I hope `entr` helps you to automate repetitive tasks and get your results faster. Keep on coding and keep on
creating!

[1]: http://eradman.com/entrproject/
[2]: http://man.openbsd.org/kqueue.2
[3]: http://man.he.net/?section=all&topic=inotify
[4]: https://brew.sh
[5]: https://github.com/eradman/entr
[6]: https://github.com/eradman/entr/blob/5.0/README.md
[7]: https://www.systutorials.com/docs/linux/man/1-entr/
