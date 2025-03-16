---
layout: post
title: "Introducing Lynx: How TikTok’s New Framework Compares to React Native"
date: 2025-03-16 20:00:00 +0200
categories:
comments: true
published: true
excerpt: |
  ByteDance introduced a brand-new mobile app development framework called Lynx. Although directly aimed at React Native, is worth to switch?
image_url: /assets/images/posts/2025_03_17_lynx.jpeg
image_description: |
  ByteDance's Lynx Framework
---

## Who is ByteDance And What Is Lynx?

ByteDance is the Chinese company responsible for TikTok. On March 5th they released [Lynx](https://lynxjs.org/blog/lynx-unlock-native-for-more), a cross-platform app development framework for Android, iOS and the Web. In their announcement they promised better performance, native styling support, and a flexible architecture. The company open-sourced Lynx on [GitHub](https://github.com/lynx-family/lynx), where it already collected more than 10k stars.

The company is already using Lynx in their own products: TikTok's search panel, studio, Shop, and LIVE, as well as Disney100 and The Met Gala on TikTok. It'll probably only be a question of time until they switch the whole application to Lynx. And the ecosystem will profit from it by getting new features and support.

Of course, this is a direct attack on React Native, one of the most widely used cross-platform app development frameworks in use today. Lynx makes it tempting for React Native developers to switch by supporting React.

## What's The Difference: Lynx vs. React Native

Both frameworks are Javascript and both frameworks are for mobile app development. Lynx is the newcomer while React Native exists since 2015.

Lynx offers a new architecture that works with two threads: a main thread for processing user events and triggering events for drawing the user interface, and a background thread for tasks that do not involve user interaction (for example API calls, file system interaction, etc.). The goal is to decouple the UI and time-intense tasks to improve [user perceived performance](https://en.wikipedia.org/wiki/Perceived_performance). Lynx focuses on these three metrics:

- First Contentful Paint (FCP): Time to first content rendering completion.
- Actual First Meaningful Paint (ActualFMP): Time to rendering of truly meaningful content.
- Time to interactive (TTI): Time until page reaches interactive state.

These metrics can be measured with their [Performance API](https://lynxjs.org/api/lynx-api/performance-api.html).

![Lynx Dual-thread Architecture](/assets/images/posts/2025_03_17_Lynx_Dual_Thread_Architecture.png "Lynx Dual-thread Architecture")

Lynx ships with its own custom JavaScript engine: [PrimJS](https://github.com/lynx-family/primjs). PrimJS is built on top of [QuickJS](https://bellard.org/quickjs/), a JavaScript engine released end of 2023 by Fabrice Bellard and Charlie Gordon. Fabrice Bellard launched a lot of other famous projects like [FFMPEG](http://ffmpeg.org/) and [QEMU](https://www.qemu.org): yes, the one that emulates your devices in Android Studio. PrimJS is written in C++ and designed specifically for Lynx. Lynx itself is written in C++ too, but the tool-chain is actually from the Rust ecosystem: interesting choice.

There are a lot of native CSS features supported by Lynx:

- Animations and transitions
- Selectors and variables for theming
- Gradients, clipping, and masking

The support for native CSS and React makes it easy for web developers to switch to app development with Lynx. And since Lynx also supports Web as a platform, it might be the best choice for app development between all three major platforms as integrated experience.

Lynx comes by default with [ReactLynx](https://lynxjs.org/react.html), the package for using React with components and declarative UI. However, they also support other JavaScript frameworks like Vue or Svelte. They intentionally kept Lynx framework-agnostic for greater acceptance in the dev community and further reach. This could prove a clever decision in a constantly changing landscape of JavaScript frameworks.

The ecosystem of compatible libraries is still in its early stages. React Native has a ten year head start on this. However, as adoption grows, the open source community will probably get more and more libraries Lynx-ready. They'll need help doing this and it may be your calling to help the open source community to grow the Lynx ecosystem, if you like this new framework.

| Feature       | Lynx                         | React Native                |
| ------------- | ---------------------------- | --------------------------- |
| Rendering     | Dual-thread architecture     | Fabric Renderer             |
| JS Engine     | PrimJS                       | Hermes                      |
| Styling       | Native CSS                   | StyleSheet API              |
| Compatibility | React, Vue, Svelte           | React-based only            |
| Ecosystem     | Early stages                 | Extensive libraries         |
| Adoption      | Growing, backed by ByteDance | Established, backed by Meta |

## Should You Use Lynx For Your Next Project?

What about your next project? Start testing Lynx by following their [hello world](https://lynxjs.org/guide/start/quick-start.html#ios-simulator-platform=macos-arm64,explorer-platform=ios-simulator) example. After completing the first _hello world_ you can get into more advanced tutorials like this [dual waterfall gallery](https://lynxjs.org/guide/start/tutorial-gallery.html).

If you're building a small mobile app and are open to try something new, Lynx might be the right choice for you. It looks promising: the better animations and smoother UI interactions could enhance the native feeling for your app. However, if your app is enterprise-grade and requires a lot of libraries, React Native seems to be the safer choice for now.

Let me know your thoughts about Lynx in the comments and as always: keep on coding and keep on creating.
