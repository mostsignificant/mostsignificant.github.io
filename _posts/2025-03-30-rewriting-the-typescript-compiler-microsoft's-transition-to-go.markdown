---
layout: post
title: "Rewriting the TypeScript Compiler: Microsoft's Transition to Go"
date: 2025-03-30 12:00:00 +0200
categories:
comments: true
published: true
excerpt: |
  A major change is coming for TypeScript version 7: the compiler will no longer be written in TypeScript itself, but be implemented in Go. Why did Microsoft make this shift? Let's have a look.
image_url: /assets/images/posts/2025_03_30_typescript_compiler_go.jpeg
image_description: |
  TypeScript Compiler Rewritten in Go
---

Anders Hejlsberg announced on Microsoft's [developer blog](https://devblogs.microsoft.com/typescript/typescript-native-port/) that they will be porting the TypeScript compiler to Go in a project called _Corsa_. They are expecting a 10x speedup in compile times, faster editor startups and reductions in memory usage. The TypeScript compiler team is planning to release a feature-complete version built in Go by the middle of 2025. Meanwhile, enthusiasts can already built the most recent version in Go on their own machines from the source code available on their new [GitHub repository](https://github.com/microsoft/typescript-go).

What is the background of this shift and why did the team choose Go?

## What is a Self-hosting Compiler?

Let's start with a look at the compiler itself. The Typescript compiler was originally written and maintained in TypeScript. But how can a compiler be written in its own language? This concept is called self-hosting.

The first version of a compiler for a new programming language cannot be written in this language: it does not exist yet. The first version has to be written in an existing programming language. That process of writing the first version of a compiler is called bootstrapping. In the case of the TypeScript compiler, the first version was written in JavaScript itself. Every following version of the compiler was written in TypeScript.

In order to compile a compiler in its own language, new features have to be compiled with the previous version of the language. For example, a TypeScript compiler for TypeScript version 6 is implemented in TypeScript version 5, the previous version of the compiler for version 5 was implemented in version 4, and so on. This works back until you get to version 1 (or version 0, whatever is your first version). At this point you have to do the mentioned bootstrapping and use another already existing language. Rober Heaton has a [good blog article](https://robertheaton.com/2017/10/24/what-is-a-self-hosting-compiler/) about the whole process with his own compiler for Gluby.

![TypeScript Self-Hosting Compiler](/assets/images/posts/2025_03_30_typescript_self_hosting.png "TypeScript Self-Hosting Compiler")

## Why The Switch To Go?

Go is a programming language by Google, one of Microsoft's biggest competitors. Microsoft has its own programming languages, the most prominent being C#. Also, the software giant from Seattle switched a lot of in-house software development to Rust recently. So why did they decide to favor Go in the case of the TypeScript compiler?

Ryan Cavanaugh from the TypeScript compiler team wrote an answer in their FAQ: [Why Go?](https://github.com/microsoft/typescript-go/discussions/411). In this post he explains that the decision was depending on more than just one factor.

> Go strongly resembles the existing coding patterns of the TypeScript codebase, which makes this porting effort much more tractable.

The existing TypeScript compiler codebase contains around 100k lines of code (LOC). The codebase is already designed around existing patterns and concepts. If a rewrite of the compiler changes not only the actual programming language but also the patterns and concepts, it will make it harder for contributors to switch over to the new code base and continue maintaining the compiler. If the resemblance of coding patterns between TypeScript and Go are close, the transition of the code base can be carried out easier.

> Go also offers excellent control of memory layout and allocation ... without requiring that the entire codebase continually concern itself with memory management.

The use of memory is important in a compiler. When compiling a large code base you don't want to overload the user's development machine or a build machine in a CI/CD chain. The worst case for memory usage while compiling is when you run out of memory, so this has to be a high priority to stay inside usable boundaries.

Saving memory itself is not just good for the hardware but also the general energy consumption: if you dial down the machine's hunger for hardware resources just a little bit, it will add up over the big number of TypeScript developers and CI/CD pipelines in data centers. TypeScript is the third most used programming language on GitHub, and the performance improvements will have a huge impact on the open source community.

In his answer, Ryan emphasizes that Go does not require the compiler developer to implement a custom garbage collector or other memory mechanisms, because this comes already with the Go toolchain on-board. This means that the compiler team can concentrate on the compilation logic itself instead of building custom memory allocation mechanisms.

> Go does an excellent job of making [graph processing] ergonomic, especially in the context of needing to resemble the JavaScript version of the code.

Ryan probably refers to the need of the compiler to traverse the [abstract syntax tree (AST)](https://en.wikipedia.org/wiki/Abstract_syntax_tree). An abstract syntax tree represents the structure of the parsed source code by dividing it into operations, variables, and other syntax elements. Compiling source code requires working with this tree a lot - building it, traversing it, storing it in memory, etc. If Go supports the graph processing out of the box, the work with abstract syntax trees becomes easier.

## What Are The Results Yet?

Regarding speed, the numbers speak for themselves.

The TypeScript compiler team did some performance tests with the Go-based compiler. On average, it shows a 10x speedup compared to the previous TypeScript-based implementation. The tests showed that the speedup does not depend on the size of the codebase, measured in lines of code. Big projects like Visual Studio Code with 1.5 million lines of code showed a similar speedup as small projects like rxjs with just 2k lines of code.

| Project                | Lines of code | tsc in TypeScript | tsc in Go | Speedup |
| ---------------------- | ------------- | ----------------- | --------- | ------- |
| VS Code                | 1,505,000     | 77.8s             | 7.5s      | 10.4x   |
| Playwright             | 356,000       | 11.1s             | 1.1s      | 10.1x   |
| TypeORM                | 270,000       | 17.5s             | 1.3s      | 13.5x   |
| date-fns               | 104,000       | 6.5s              | 0.7s      | 9.5x    |
| tRPC (server + client) | 18,000        | 5.5s              | 0.6s      | 9.1x    |
| rxjs (observable)      | 2,100         | 1.1s              | 0.1s      | 11.0x   |

It is not just the compilation that profits from the speedup, but also the editor's features like auto-completion and general syntax checking. They tested it with the Visual Studio code base and experienced a "8x improvement in project load time". The memory usage seemed to be half of previous measurements, but they didn't show any further results in the blog article. In the [Youtube video explanation](https://www.youtube.com/watch?v=pNlq-EVld70) by Anders Hejlsberg, he explains that customers' no. 1 complaint was memory consumption. You can expect more reliable results with the final release of the compiler or run your own evaluations with the following TypeScript compiler flags:

```bash
tsc -b -f -diagnostics
```

## What Happens Next?

The compiler team announced that they will release the new compiler with TypeScript version 7, expected to be finished later in 2025. The new nomenclature for these releases are _TypeScript 6 (JS)_ for the compiler still being built with TypeScript, and _TypeScript 7 (native)_ for the compiler built in Go. The TypeScript version 6 will be supported further until the new native version reaches a certain level of maturity.

Further information can be found in their [GitHub repository](https://github.com/microsoft/typescript-go/discussions/categories/faqs) or the [TypeScript community Discord](https://discord.gg/typescript). If you want to, you can already build the current version for yourself with [Go 1.24 or higher](https://go.dev/dl/), [Node.js with npm](https://nodejs.org/), and [hereby](https://www.npmjs.com/package/hereby).

Let me know in the comments what you think about the new TypeScript compiler. And as always: keep on coding and keep on creating.
