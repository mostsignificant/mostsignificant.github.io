---
layout: post
title: "Forge Stronger Code: Emulating Rust's Approach for Unit Testing in C++"
date: 2024-04-24 22:09:10 +0200
categories: C++ Testing Rust
comments: true
published: true
excerpt: |
  Testing in C++ or any programming language requires a certain kind of discipline to keep it efficient and well-organized. Here I am advocating for
  a more direct approach to organize unit tests inspired by Rust: placing them in the same file as the actual
  implementation.

image_url: /assets/images/unsplash/frankie-lopez-aTEo-OzcMnM-unsplash.jpg
image_description: |
  Photo by [Frankie Lopez](https://unsplash.com/@frankielopez?utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/road-during-golden-hour-aTEo-OzcMnM?utm_content=creditCopyText)
---

The source code for this example can be found in my GitHub [repo](https://github.com/mostsignificant/inline_cpp_testing).

## Inspired by Rust

Testing in Rust is pretty straight-forward: Annotating test with a corresponding test-attribute, running `cargo test`
and getting the results. The tests can and are advocated to be written in the source file itself rather than separate
files in a different directory. The following snippet is an example from their excellent Rust
[documentation](https://doc.rust-lang.org/rust-by-example/testing/unit_testing.html) about unit testing.

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(1, 2), 3);
    }
}
```

## C++ Example

There are a lot of C++ frameworks, but these two popular ones are standing out the most:

- [googletest](https://github.com/google/googletest) by the search engine giant themself and
- [Catch2](https://github.com/catchorg/Catch2), a header-only lightweight but powerful testing framework.

We are focusing on the second one in our examples here. But the proposed approach can be used with any unit testing
framework.

The following example shows a source code with the actual implementation (the `square()` function) and a unit test
(`square function`).

`square.cpp`

```cpp
int square(int num) {
    return num * num;
}

#ifdef BUILD_TESTS
#include <catch2/catch_test_macros.hpp>

TEST_CASE("square function", "[square]") {
    REQUIRE(square(2) == 4);
    REQUIRE(square(-1) == 1);
}

#endif // BUILD_TESTS
```

In a real world scenario, a square implementation would be more advanced, starting with protection against overflow
(especially since signed integer overflow is
[undefined behaviour](https://www.codalogic.com/blog/2022/11/01/Beware-C%2B%2B-Undefined-Behaviour)).

For this example, we will also add a main file, which just builds the square of the passed number and returns the
result. However, because the test build will define it's own `main()` method (running the actual unit test when calling
the executable), we have to exclude our real `main()` method with the same `BUILD_TESTS` flag - otherwise it will not
build having two definitions of `main()`.

`main.cpp`

```cpp
#ifndef BUILD_TESTS

#include "square.hpp"

#include <cstdlib>
#include <stdexcept>
#include <string>

auto main(int argc, char *argv[]) -> int {
  if (argc != 1)
    return EXIT_FAILURE;

  const auto num = std::stoi(std::string(argv[0]));
  return square(num);
}

#endif // !BUILD_TESTS
```

## Build Integration

Within CMakeLists.txt we include the required test framework, in this case Catch2. This example assumes that Catch2 is
included as git submodule within the project's directory. If using a different approach (FetchContent or a C++ package
manager like vcpkg), the instructions can be found in the Catch2
[documentation](https://github.com/catchorg/Catch2/blob/devel/docs/cmake-integration.md#top).

We are including the source file containing the actual implementation with the unit tests and the main file as usual:

```cmake
add_executable(square
    src/main.cpp
    src/square.cpp
)
```

Further within the CMakeLists.txt file, we define our TEST flag for being able to control whether we build with tests or
without the tests. This is important, as we need to exclude the test library from the final binary, that we want to
release or deploy.

```cmake
if (BUILD_TESTS)
    add_subdirectory(external/Catch2)
    target_link_libraries(square PRIVATE Catch2::Catch2WithMain)
    target_compile_definitions(square PRIVATE BUILD_TESTS=${BUILD_TESTS})
endif ()
```

At the end, we have essentially two possibilities for our build. We can either build without the `BUILD_TESTS` flag:
this results in the main executable with the intended square functionality from our example.

```sh
mdkir build && cd build
```

```sh
cmake ..
```

```sh
cmake --build .
```

```sh
./square 2
```

Or we can build with our `BUILD_TESTS` flag set, which will result in a unit test executable.

```sh
mdkir build && cd build
```

```sh
cmake .. -DBUILD_TESTS=ON
```

```sh
cmake --build .
```

```sh
./square
```

This results in our unit tests being run and the results printed to the command line.

```sh
Randomness seeded to: 2846031641
===============================================================================
All tests passed (2 assertions in 1 test case)
```

## Pro and Contra

The two main points that are

- Strong unit test convergence
  Since the unit tests are in the same file as the actual tested code, it is easier to implement features and write the
  according tests in one go. It is easier to maintain a consistent picture between code and test coverage and spot code
  that still misses unit testing.

- Ease of use
  It is very easy to include new tests in the files and the principle is also easy to understand: new source code means
  new tests in the same file, all unit tests in one file concerning only the contained source code.

But there are also two main pitfalls when using this approach:

- Not well-suited for a header-only library
  This approach does not fit well within a pure header-only library. If the unit tests are also included in the header
  files, this means that they are also shipped to the consumer - making the library unnecessary big and cluttered.
- More difficult build matrix
  In order to test both debug and release builds effectively, and at the same time ensuring a final efficiently packaged
  deliverable without test framework and test code requires additional build pipelines within the CI/CD.

So the presented approach has its pro's and cons. However, if you implement this approach, make sure to be consistent -
do not mix with the classic unit testing approach and have the inline unit tests and a separate folder with unit tests
for a separate unit testing executable.

Additionally, make sure that the tests stick to unit testing only - integration testing or system tests are not suitable
to be covered by the presented approach.

## Next Steps

It is easy to elaborate on unit testing and we did not have a look at the other important aspects. They apply to unit
testing in general and are not specific to the presented approach:

- Measure test coverage (get inspired by [this blog post](https://medium.com/@xianpeng.shen/use-gcov-and-lcov-to-perform-code-coverage-testing-for-c-c-projects-c85708b91c78) about `gcov` and `lcov`)
- Use mocking for components (have a look at [FakeIt](https://github.com/eranpeer/FakeIt) or
  [gMock](https://google.github.io/googletest/gmock_for_dummies.html))

Keep on coding and keep on creating!
