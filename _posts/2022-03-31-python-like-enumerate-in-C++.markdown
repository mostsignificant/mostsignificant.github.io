---
layout: post
title: "More Python-esque functionality in C++ that makes your life better"
date: 2022-03-31 12:30:00 +0200
categories: C++
published: false
---

Sometimes I am missing a few helpers for iterating in C++. It gives me a envy-ing look to other programming languages,
for example python with its `enumerate(...)` function to have the value and the index of a range easily accessible
within a loop.

> **`enumerate(iterable, start=0)`**
>
> Return an enumerate object. _iterable_ must be a sequence, an iterator, or some other object which supports iteration.
> The `__next()__` method of the iterator returned by `enumerate()` returns a tuple containing a count (from start which
> defaults to 0) and the values obtained from iterating over _iterable_.
>
> &mdash; <cite>[python docs: functions enumerate][1]</cite>

The Python documentation does not go into detail about the usability in loops, but it is apparent:

```python
langs = ['C++', 'Rust', 'Python']

for i, lang in enumerate(langs):
    print(i, lang)
```

This prints the following:

```term
0 C++
1 Rust
2 Python
```

This should not be too complicated to implement in C++. Additionally it fits perfectly with the
[structured binding declarations][2] introduced in C++17.

## Let's start with a sketch

I was aiming for a syntax together with the mentioned structured bindings which would look somewhat like the following
and print the same lines as in the Python example.

```cpp
const auto langs = std::vector<std::string>{ "C++", "Rust", "Python" };

for (const auto&& [i, lang] : enumerate(langs))
    std::cout << i << ' ' << lang << '\n';
```

To achieve this I needed the following: a range-like object for the container and a corresponding iterator to get from
begin to end with an additional index. The range needs a `begin()` and an `end()` member function returning a custom
iterator. This custom iterator needs to return a std::pair on dereferencing and voilá - the enumerate should work
similar to the Python model. So much for the theory. Here are some sources that proved helpful during implementation.

- Range-based for loops: [en.cppreference.com/w/cpp/language/range-for][3]
- Structured bindings: [hen.cppreference.com/w/cpp/language/structured_binding][2]
- Iterator requirements: [en.cppreference.com/w/cpp/named_req/Iterator][4]
- Range requirements: [en.cppreference.com/w/cpp/ranges/range][5]

## Implementation

For starting I declare an enumerate(...) function, an enumerate_range and an enumerate_iterator. I outline the following
code to have a rough concept of how it could look like. For these small helpers I prefer to do this within the fantastic
[Compiler Explorer][6] by [Matt Godbolt][7] - because if it compiles at least I know I am venturing in the right
direction.

```cpp
template <class Iter, class T, bool Const = false>
class enumerate_iterator {
public:
    using pointer = typename std::conditional_t<Const, const T* const, T*>;
    using reference = typename std::conditional_t<Const, const T&, T&>;

    enumerate_iterator(Iter iterator, std::size_t index);

    auto operator!=(const enumerate_iterator& other) -> bool;
    void operator++();
    auto operator*() const -> std::pair<std::size_t, reference>;

private:
    Iter iterator;
    std::size_t index;
};
```

The `enumerate_range` does two things only: holding a reference to the container and giving begin- and end-iterators if
the corresponding methods are called. Additionally, some typedefs are used to make the signatures more readable and
generally collect some more C++ karma points.

```cpp
template <class Container, bool Const = false>
struct enumerate_range {
    using value_type = typename Container::value_type;
    using container_iterator =
        typename std::conditional_t<Const, typename Container::const_iterator,
                                    typename Container::iterator>;
    using iterator = enumerate_iterator<container_iterator, value_type, Const>;
    using reference = typename std::conditional_t<Const, const Container&, Container&>;

    explicit enumerate_range(reference container);

    auto begin() -> iterator;
    auto end() -> iterator;

private:
    reference container;
};
```

Finally two `enumerate(...)` functions: one for the const containers, and one for the non-const containers. These
functions should be the main interface for the user to instantiate an `enumerate_range` without having to call it
manually and supplying the template parameters.

```cpp
template <class Container>
auto enumerate(const Container& container) -> enumerate_range<Container, true> {
    return enumerate_range<Container, true>(container);
}
```

```cpp
template <class Container>
auto enumerate(Container& container) -> enumerate_range<Container, false> {
    return enumerate_range<Container, false>(container);
}
```

You might have already spotted some points to improve the code but this should just be a starting point. The
`enumerate(...)` function returns an instance of `enumerate_range` providing both `begin()` and `end()` functions. The
range-based for loop is happy as long as these methods return an iterator with dereferencing, operator++, and comparison
support. Under the hood it is not much more than an elobarate for loop with iterators - we could also write the
following (but who doesn't like saving a few keystrokes and make things a little bit more readable):

```cpp
const auto range = enumerate(langs);
for (auto it = range.begin(), end = range.end(); it != end; ++it)
    std::cout << it->first << ' ' << it->second << '\n';
```

After doing a quick polish here and there, running it through some basic tests, I had a first iteration of the code
finished. Time to post it on [codereview.stackexchange.com][8] and sleep over it and wait for feedback. And this
feedback and tips proved to be very helpful because:

- the `Const` template parameter could be saved just by adapting the typedefs
- the operator++() signature was wrong
- enumerate_range's `end()` function could be improved performance-wise
- the enumerate_iterator fits better to be a implementation detail of enumerate_range
- enumerate_range could be extended with container-like accessors

Okay, valid points. Time to write some serious code and wrap this thing up.

## Refactoring and refining

## Testing and documenting

[1]: https://docs.python.org/3/library/functions.html#enumerate
[2]: https://en.cppreference.com/w/cpp/language/structured_binding

[3]: https://en.cppreference.com/w/cpp/language/range-for]
[4]: https://en.cppreference.com/w/cpp/named_req/Iterator
[5]: https://en.cppreference.com/w/cpp/ranges/range
[6]: https://godbolt.org
[7]: https://twitter.com/mattgodbolt
[8]: https://codereview.stackexchange.com
