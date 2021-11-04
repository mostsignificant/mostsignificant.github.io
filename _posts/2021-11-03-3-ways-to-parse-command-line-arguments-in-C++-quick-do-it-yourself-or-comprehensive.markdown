---
layout: post
title: "3 Ways To Parse Command Line Arguments in C++: Quick, Do-It-Yourself, Or Comprehensive"
date: 2021-11-03 17:00:00 +0200
categories: C++
published: true
excerpt: |
  If you are writing a C++ tool you often need the user to pass in arguments via the command line. And like many other
  topics in C++ there are also many ways to handle command line arguments in C++. In this post I want to introduce
  three different methods to do this. You can decide for the method you see fit for your project depending on the pros
  and cons.
image_url: /assets/images/unsplash/zhang-kaiyv-rkyfaZ1vkAs-unsplash-2.jpg
image_description: |
  Photo by [zhang kaiyv](https://unsplash.com/@zhangkaiyv?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/s/photos/skyline?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

## More than One Way to Skin a Command Line

I will describe the following three methods to parse command line arguments:

- A **quick-and-dirty** method if you just need to pass a few arguments in a controlled environment
- Your own **do-it-yourself** command line arguments parser if you need a little bit more, are a fan of homemade C++, or
  if you suffer from dependophobia (the medical term for being afraid of managing dependencies in your code)
- Setting up an **external library** which does the heavy lifting for you

## Command Line Arguments: Collect Them All

The first question is a basic one: How do these command line arguments find their way into my C++ source code? The C++
standard mentions two valid signatures for the [main function](https://en.cppreference.com/w/c/language/main_function):

```cpp
(1) int main(void) { /* ... */ }
(2) int main(int argc, char *argv[]) { /* ... */ }
```

Yes, you guessed right, the second one is the one we are after here. It supplies an array of strings (`argv`) and the
number of elements in this array (`argc`). We as C++ developers who find happiness in iterating over things, we very
much like the following quote::

> The size of the array pointed to by argv is at least argc+1, and the last element, argv[argc], is guaranteed to be
> a null pointer.

This means we can easily plug those into functions and containers from the C++ standard library. Rewrite your main
function signature to `int main(int argc, char *argv[])` if you haven't already. Next, you can easily print the command
line arguments passed to your application with a single line (and some includes) which is useful for quick "debugging"
(in my book, printf-ing qualifies as debugging):

```cpp
#include <algorithm>
#include <iostream>

int main(int argc, char *argv[]) {
    std::copy(argv, argv + argc,
              std::ostream_iterator<char *>(std::cout, "\n"));
  // ...
}
```

This line will output every passed command line argument on stdout on separate lines. If you execute this, you will see
that the first argument is the program's calling name itself.

```shell
$ ./build/bin/example INPUTFILE.txt -xyz
./build/bin/example
INPUTFILE.txt
-xyz
```

_Bonus:_ I had my aha-moment when I read that there exists a third form for the main function signature which
additionally supplies the host's environment variables:

```cpp
(3) int main(int argc, char *argv[], char *envp[]) { /* ... */ }
```

You can read more about this [here](https://pubs.opengroup.org/onlinepubs/9699919799/functions/exec.html). However, this
is out of scope for this blog post. Additionally, the authors recommend that:

> Applications should use the getenv() function rather than accessing the environment directly via either envp or
> environ

## The dog Example

For showcasing the three methods we are using a simple example application. The application will be called `dog` and
prints to the stdout command line whatever file we give as command line parameter (a simplified
[cat](https://www.man7.org/linux/man-pages/man1/cat.1.html) command). We will make additional features available for
the user as command line arguments to display the individual command line parsing methods.

The example can be found on my github repository
[https://github.com/mostsignificant/dog](https://github.com/mostsignificant/dog) in three different branches. I might
use the main branch for further development or future blog posts.

- [/dog/tree/method-quick-and-dirty](https://github.com/mostsignificant/dog/tree/method-quick-and-dirty)
- [/dog/tree/method-diy](https://github.com/mostsignificant/dog/tree/method-diy)
- [/dog/tree/method-external-library](https://github.com/mostsignificant/dog/tree/method-external-library)

## Quick-And-Dirty

The first method is the quick hack. Useful if you have only a few arguments and little additional logic (as in: mutual
exclusive options, arbitrary ordering, and such). As already shown, you get the number of arguments passed to your
application via an extra argument. Our dog application needs an input file that is going to be printed to stdout. The
first argument of the program call shall be this input file (can be relative or absolute path, ifstream will try to open
and read it).

Accessing the first `argv` should do the trick and get us the user-supplied file name. However, we do remember that the
first `argv` entry is actually the called program name. So our input file name is supposed to be at `argv[1]`. But even
this wild-west style of accessing command line arguments is not outlaw enough to brush over boundary checking. At the
beginning of the program, we can check if we have the minimum required amount of command line parameters.

```cpp
if (argc < 2) {
    std::cerr << "dog: missing input file!\n"
              << "usage: dog <input_file>\n";
  return EXIT_FAILURE;
}
```

Next, you just pass the `argv[1]` input file's name like a good old, tried and tested C-style string to open via
`ifstream`.

```cpp
std::ifstream input_file(argv[1], std::ios::in);
if (!input_file.is_open()) {
    std::cerr << "dog: could not open input file '" << argv[1] << "'!\n";
    return EXIT_FAILURE;
}
```

As you might have already noticed, this methods works best for a fixed number of command line arguments. Say you want to
add an optional argument for outputting line numbers, you would need to add more code for checking, maybe similar to
this:

```cpp
if (argc >= 3 && strcmp(argv[2], "-n") == 0)
```

But this will make your argument count checking more convoluted. And the loop. And any wish for more optional arguments.
And this clearly works only for a fixed order of arguments. If you introduce further command line arguments, this code
breaks when the user passes them in inverted order, for example -v -n. And honestly, arbitrary order of command line
arguments is expected by users since many years BC (before C++).

Further problems arise if you want to pass these arguments to underlying functions. Code becomes more unreadable quickly
and workarounds with additional argument checking functions will pile up. Soon you will be refactoring this code and
arrive at the next method, your full command line argument parsing do-it-yourself solution.

You can checkout the code of the described quick-and-dirty method in my github repository on the corresponding branch
[/dog/tree/method-quick-and-dirty](https://github.com/mostsignificant/dog/tree/method-quick-and-dirty).

## Do-It-Yourself

As real C++ sapiens neanderthalensis we are naturally drawn to build stuff from scratch. In our compiler habitats we
contrive the endless amount of features that our code [opus](<https://en.wikipedia.org/wiki/Magnum_opus_(disambiguation)>)
shall support. We recognized that it needs a proper solution for parsing and accessing the command line arguments
throughout the code.

First, let us setup a separate file for the command line parsing related stuff. We will call this `program_options` for
creativity bonus points. It will be a basic namespace with pure functions. The argument values will be stored in
file-scope variables. The solution will be tailored to our application needs and not feature a fully generic solution.

```cpp
#include <string_view>
#include <vector>

namespace program_options {

void parse(int argc, char* argv[]);

const std::vector<std::string_view>& input_files();
bool show_ends();
bool show_line_numbers();

};  // namespace program_options
```

Within the implementation of the parse method, you can once again use the iterative power of standard containers and do
the following:

```cpp
void program_options::parse(int argc, char* argv[]) {
    const std::vector<std::string_view> args(argv + 1, argv + argc);
    // ...
}
}
```

If you are stuck in pre-C++17, let me feel sorry for you and just use
[`std::string`](https://en.cppreference.com/w/cpp/string) instead of
[`std::string_view`](https://en.cppreference.com/w/cpp/string/basic_string_view). We are putting them in a vector for
convenience's sake. But what about the allocation you say? Based on input from the outside world you say?
IT security 0/10. So what happens if somebody gives you `INT_MAX` command line arguments? Is this even possible in an OS
and how many can you pass into a program?
[If you have to ask, you're probably doing something wrong](https://devblogs.microsoft.com/oldnewthing/20070301-00/?p=27803).
So keep it simple and just check again at the start of the `parse()` method:

```cpp
if (argc > 64) {
    throw std::runtime_error("too many input parameters!");
}
```

So why even put everything in a container? Why not plain old cowboy-style C++ and slap
`for (int i = 0; i < argc; ++i) { /* doing stuff with argv[i] */ }` over the command line arguments like before?

1. Safety: I prefer not to have index variables being thrown around, especially with C-style arrays and loose boundary
   checking.
2. Readability: It helps the reader to scan the code faster. The variable name arg is more concise than `argv[i]`.
3. Performance: Even if the user is supplying a whopping 256 command line arguments, the vector will allocate this memory
   very fast. There is not much to be gained here performance-wise.

> Premature optimization is the root of all evil
>
> **- Donald Knuth**

Let us use exceptions to exit early on any input argument errors. Let us use alternative argument names and let us store
the values in file-local variables. We will end up with a loop like this:

```cpp
for (const auto& arg : args) {
    if (_input_files.empty()) {
        if (arg == "-n" || arg == "--number") {
            if (_show_line_numbers) {
                throw std::runtime_error("cannot use -n/--number twice!");
            }
            _show_line_numbers = true;
            continue;
        }

        if (arg == "-E" || arg == "--show-ends") {
            if (_show_ends) {
                throw std::runtime_error("cannot use -E/--show-ends twice!");
            }
            _show_ends = true;
            continue;
        }
    }

    if (!std::filesystem::exists(arg)) {
        throw std::runtime_error(std::string(arg) + ": No such file");
    }
    _input_files.push_back(arg);
}
```

Yes, exceptions. This means a friendly try-and-catch block in the `main` method will help us output readable error descriptions.

```cpp
try {
  program_options::parse(argc, argv);
} catch (const std::exception &x) {
  std::cerr << "dog: " << x.what() << '\n';
  std::cerr << "usage: dog [-n|--number] [-E|--show-ends] <input_file> ...\n";
  return EXIT_FAILURE;
}
```

And for the rest of the program just access the parameters through the methods from the program_options namespace.

```cpp
for (const auto &file_name : program_options::input_files()) {
    std::ifstream input_file(file_name, std::ios::in);

    // ...

    while (std::getline(input_file, line)) {
        if (program_options::show_line_numbers())
            std::cout << std::setw(6)
                      << std::setfill(' ')
                      << line_count++
                      << "  ";

        // ...

        if (program_options::show_ends())
            std::cout << '$';

        // ...
    }
}
```

The full solution is shown in the GitHub dog repository in the corresponding branch
[dog/tree/method-diy](https://github.com/mostsignificant/dog/tree/method-diy). If your program uses simple arguments
according to a predefined schema like `-<OptionName> <OptionValue>` or simple switches like `-<OptionValue>` then the
following methods might be sufficient for your purposes:

```cpp
std::string_view get_option(
    const std::vector<std::string_view>& args,
    const std::string_view& option_name) {
    for (auto it = args.begin(), end = args.end(); it != end; ++it) {
        if (*it == option_name)
            if (it + 1 != end)
                return *(it + 1);
    }

    return "";
}
```

```cpp
bool has_option(
    const std::vector<std::string_view>& args,
    const std::string_view& option_name) {
    for (auto it = args.begin(), end = args.end(); it != end; ++it) {
        if (*it == option_name)
            return true;
    }

    return false;
}
```

The following example shows how to get a -m flag or -d parameter from the command line parameters with these two
methods:

```cpp
const std::vector<std::string_view> args(argv, argv + argc);

const bool modify = has_option(args, "-m");
const std::string_view date = get_option(args, "-d");
```

## External library

Your last resort is a fully-fledged solution using an external library if you want some of these out-of-the-box
features:

- GNU style syntax for options
- Help messages
- Error robustness
- Default values
- Option flexibility

There are several libraries out there - but these libraries stood out for me:

### boost::program_options

To no-one's surprise the famous [boost libraries](https://www.boost.org) also feature a module for parsing command line
arguments called [boost::program_options](https://github.com/boostorg/program_options). Very straight-forward to use
with detailed [documentation](https://www.boost.org/doc/libs/1_77_0/doc/html/program_options.html). However I am not the
biggest fan of having to include boost libraries. But if the project is using boost libraries already, this is the
obvious way for parsing command line arguments.

```cpp
namespace po = boost::program_options;

// Declare the supported options.
po::options_description desc("Allowed options");
desc.add_options()
    ("help", "produce help message")
    ("compression", po::value<int>(), "set compression level");

po::variables_map vm;
po::store(po::parse_command_line(ac, av, desc), vm);
po::notify(vm);

if (vm.count("help")) {
    cout << desc << "\n";
    return 1;
}

if (vm.count("compression")) {
    cout << "Compression level = " << vm["compression"].as<int>() << '\n';
} else {
    cout << "Compression level was not set.\n";
}
```

### GNU getopt

> getopt is a C library function used to parse command-line options of the Unix/POSIX style
>
> **- [wikipedia](https://en.wikipedia.org/wiki/Getopt)**

Similar to the program getopt for parsing arguments in shell scripts, there is a
[GNU extension](https://www.gnu.org/software/libc/manual/html_node/Getopt.html) providing the same functionality for
C/C++ programs. Simpler than the other external libraries presented here, but certainly a good alternative if you don't
trust your own self-knitted code.

```cpp
#include <getopt.h>

int main(int argc, char* argv[]) {
    option longopts[] = {
        {"number", optional_argument, NULL, 'n'},
        {"show-ends", optional_argument, NULL, 'E'}, {0}};

    while (1) {
        const int opt = getopt_long(argc, argv, "nE::", longopts, 0);

        if (opt == -1) {
            break;
        }

        switch (opt) {
            case 'n':
                // ...
            case 'E':
                // ...
        }
    }

    //...
}
```

### cxxopts

For the external library in our dog example, we picked [cxxopts](https://github.com/jarro2783/cxxopts). Let us add this
library by simply adding the GitHub repository as git submodule with a single simple command:

```shell
git submodule add https://github.com/jarro2783/cxxopts extern/cxxopts
```

The CMakeLists.txt needs additional entries to know about this newly included project and the include paths (although
the project has only one header, so copy-paste would be fine for our toy-project, too):

```shell
add_subdirectory(extern/cxxopts)
target_include_directories(${TARGET_NAME} PUBLIC cxxopts)
target_link_libraries(${TARGET_NAME} PUBLIC cxxopts)
```

Dependencies are included, so we can get to work. The workflow is as follows:

- Declare a `cxxopts::Options` instance
- Define available program options and their types (default is bool)
- Declare our input file names to be positional arguments
- Call `parse()` method
- Use options

```cpp
int main(int argc, char *argv[]) {
    cxxopts::Options options("dog");

    options.add_options()
        ("n,number", "Show line numbers")
        ("E,show-ends", "Show line endings")
        ("version", "Show the version")
        ("input_files", "Input file(s) to concatenate",
            cxxopts::value<std::vector<std::string>>());

    options.parse_positional({"input_files"});
    cxxopts::ParseResult result;

    try {
        result = options.parse(argc, argv);
    } catch (const cxxopts::OptionParseException &x) {
        std::cerr << "dog: " << x.what() << '\n';
        std::cerr << "usage: dog [options] <input_file> ...\n";
        return EXIT_FAILURE;
    }

    if (result.count("version")) {
        std::cout << "dog version " << DogVersion << '\n';
        return EXIT_SUCCESS;
    }

    if (!result.count("input_files")) {
        std::cerr << "dog: missing input file(s)!\n";
        std::cerr << "usage: dog [options] <input_file> ...\n";
        return EXIT_FAILURE;
    }

    const auto files = result["input_files"].as<std::vector<std::string>>();
    for (const auto &file : files) {
      // ...

      if (result.count("number"))
        // ...

      if (result.count("show-ends"))
        // ...
    }
}
```

The solution provided a lot of functionality without significantly more effort than the other solutions. It allows
arbitrary order of command line arguments being passed in, short and long options, positional options, etc. However,
the naming of the options might be best handled by constants, in order to not mistype option names like `show-ends`. I
am also not very keen on the builder-pattern-like syntax for adding options - nor the clang-format tool, which tends to
mess it up. The working implementation for the dog example can be found on the branch
[dog/tree/method-lib](https://github.com/mostsignificant/dog/tree/method-lib). There are a lot more options in `cxxopts`
that I haven't used yet, for example `allow_unrecognised_options()`, `default_value(...)`, or `std::vector<T>` support
for options. They can be checked out in the README file or example source code.

## Conclusion

We checked three different approaches to achieve a similar goal: parsing arguments passed via command line to our
program. The method which fits your needs depends heavily on your requirements. You need to determine where your command
line input will come from: end users, test or automation environments, etc. You need to be clear about what kind of
arguments you need, if order is arbitrary, if there are listed and/or optional arguments etc. And you need to decide
which solution brings the best return of investment - investment being time in this case.

The first shown method involved a quick hack to iterate over the given arguments. This fits use cases for testing, and
an arbitrary list of arguments passed via command line, for example a simple list of files.

The second approach demonstrated how to start your own self-made solution. In my opinion it works best if it is directly
tailored to your solution with parsing the options directly and implementing custom error cases. These errors during
parsing the command line arguments can be easily propagated by throwing exceptions. However, things like more a advanced
order of arguments can lead to messy code if conditions are not structured correctly.

The final third approach was using an external library. I preferred a header-only library called `cxxopts` which was
easy to include and use. It provided sufficient functions to support option ordering and handling, and followed the
quasi-standardised GNU style of command line arguments (for example short and long options).

I hope this demonstration of the three methods helps you find the best method for your program to parse command line
arguments in C++. Keep on coding and keep on creating!
