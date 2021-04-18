---
layout: post
title:  "Parsing command line arguments in C++"
date:   2021-04-18 18:05:00 +0200
categories: C++ cli
---
If you are writing a C++ tool you often need the user to pass in arguments via the command line. And like many other
topics in C++ there are also many ways to handle command line arguments in C++. In this post I want to introduce three
different methods to do this. You can decide for the method you see fit for your project depending on the pros and cons.

## More than one way to skin a command line

I will describe the following three methods to parse command line arguments:

- A **quick-and-dirty** method if you just need to pass a few arguments in a controlled environment
- Your own **DIY** command line arguments parser if you need a little bit more, are a fan of homemade C++, or if you
  suffer from dependophobia (the medical term for being afraid of managing dependencies in your code)
- Setting up an **external library** which does the heavy lifting for you

## Where to get the best command line arguments

The first question is a basic one: How do these command line arguments find their way into my C++ source code? The C++11
standard mentions two valid signatures for the [main function](https://en.cppreference.com/w/c/language/main_function):

```cpp
(1) int main(void) { /* ... */ }
(2) int main(int argc, char *argv[]) { /* ... */ }
```

Yes, you guessed right, the second one is the one we are after here. It supplies an array of strings (`argv`) and the
number of elements in this array (`argc`). As people who find happiness in iterating over things we very much like the
following quote:

> The size of the array pointed to by argv is at least argc+1, and the last element, argv[argc], is guaranteed to be
> a null pointer.

This means we can easily plug those into functions and containers from the C++ standard library. I will show more about
this in the quick-and-dirty and DIY example. Rewrite your main function signature to`int main(int argc, char *argv[])`
if it isn't already and read on.

*Bonus:* I had my aha-moment when I read that there exists a third form for the main function signature which 
additionally supplies the host's environment variables:

```cpp
(3) int main(int argc, char *argv[], char *envp[]) { /* ... */ }
```

You can read more about this [here](https://pubs.opengroup.org/onlinepubs/9699919799/functions/exec.html). However, this
is out of scope here and they recommend that

> Applications should use the getenv() function rather than accessing the environment directly via either envp or
> environ

## The example

For showcasing the three methods we are using a simple example application. The application will be called `dog` and
prints to the std::out command line whatever file we give as command line parameter (a simplified
[cat](https://www.man7.org/linux/man-pages/man1/cat.1.html) command). We will make additional features available for
the user as command line arguments to display the individual command line parsing methods.

## Quick-and-dirty

## DIY

## External library