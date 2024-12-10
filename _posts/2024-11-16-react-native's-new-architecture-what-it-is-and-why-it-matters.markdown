---
layout: post
title: "React Native's New Architecture: What It Is and Why It Matters"
date: 2024-11-15 00:00:00 +0200
categories: React Native
comments: true
published: false
excerpt: |
  React Native announced a new architecture which will be enabled by default in their new releases, starting with 0.76. So it is time to look at what they improved, why they actually changed the old architecture and how this matters to developers and users.

image_url: /assets/images/unsplash/PATH.jpg
image_description: |
  Photo by [NAME](https://unsplash.com/USERNAME?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/HASH?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

The new architecture was announced in a React Native [blog post](https://reactnative.dev/blog/2024/10/23/the-new-architecture-is-here) referencing their [0.76 release](https://reactnative.dev/blog/2024/10/23/release-0.76-new-architecture). The new release brings improved performance, modern React features, and a better developer experience. Let's have a closer look if this new release also delivers on these promises.

## Key Features Introduced in the New Architecture

The team states that they rewrote core components and workings of the system, for example the rendering, native code integration, or scheduling across threads.

The new architecture brings full support for these features from React to its React Native offspring:

- [Suspense](https://react.dev/blog/2022/03/29/react-v18#new-suspense-features)
- [Transitions](https://react.dev/blog/2022/03/29/react-v18#new-feature-transitions)
- [Automatic Batching](https://react.dev/blog/2022/03/29/react-v18#new-feature-automatic-batching)
- [useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)

Additionally, there are two new systems with type-safety built in that are coming with the new architecture:

- [Native Modules](https://reactnative.dev/docs/next/turbo-native-modules-introduction)
- [Native Components](https://reactnative.dev/docs/next/fabric-native-components-introduction)

There is a one-hour talk about the new architecture at [React Conf 2024](React Conf 2024 - Day 2 Keynote). This talk not just includes the new architecture but the general vision of the React Native team. So skip the Instagram doom-scrolling and watch something worthwhile instead.

The React Native team states that the most popular libraries already support the new architecture. This implies that migrating existing apps to the new release should be smooth and similar to previous migrations. However, for any not-so-easy to migrate cases, there is an "automatic interoperability layer to enable backward compatibility".

Backward Compatibility and Migration
Gradual migration process for most apps.
Automatic interoperability layer for libraries targeting the old architecture.
Wide library support for the new systems.
Performance Highlights
Lazy-loaded Native Modules for faster initialization.
Improved UI responsiveness and reduced rendering delays.
Why the Rewrite Was Necessary

Challenges of the Old Architecture
Asynchronous-only communication over the bridge.
Bottlenecks with serializing function calls and large objects.
Synchronization issues causing UI inconsistencies (e.g., empty frames, visual jumps).
Inability to properly support concurrent React features.
User Expectations and Performance Goals
The demand for immediate feedback and seamless UI interactions.
Difficulties achieving 60+ FPS with the old architecture.
Core Improvements in the New Architecture

The New Native Module System
Synchronous and asynchronous access to the native layer.
Lazy-loading for performance gains.
The New Renderer
Concurrent updates across multiple threads.
Improved layout processing for responsiveness.
The Event Loop
Prioritizing user input and urgent tasks.
Alignment with web specifications (e.g., microtasks and MutationObserver).
Eliminating the Bridge
Direct JavaScript-native communication.
Faster app startup, better error handling, and debugging.
Adoption and Production Readiness

Gradual Transition for Developers
Community efforts, such as the New Architecture Working Group, to ease adoption.
Resources like talks and documentation for developers.
Real-World Use Cases
Meta's large-scale use in Facebook, Instagram, and Quest devices.
Early adopters' success stories: Expensify, Kraken, and BlueSky.
Library Compatibility
Support from popular libraries and the broader ecosystem.
Resources for Developers

Talks and Presentations
Links to talks from React Native EU 2019, React Conf 2021/2024, and App.js 2022.
Migration Guides and Tools
Resources for upgrading apps to the New Architecture.
Community forums and working groups.
Looking Ahead: The Future of React Native

Impact on Cross-Platform Development
How the New Architecture solidifies React Native's position as a leading framework.
Long-term benefits for the React and React Native ecosystems.
Potential Challenges
Areas that may require developer attention during migration.
Addressing edge cases and unique project requirements.
Conclusion

Summary of Key Benefits
Better performance, enhanced user experience, and modern features.
Call to Action
Encouragement for developers to try React Native 0.76.
Explore new opportunities and resources available.
