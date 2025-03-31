---
layout: post
title: "React Native Release Build Crashes on Android? ProGuard Might Be the Cause"
date: 2025-03-22 23:23:57 +0200
categories:
comments: true
published: false
excerpt: |
  My app ran perfectly fine in Expo Go, in the Android simulator, but got stuck on release builds running on physical devices. After long debugging I found out: ProGuard was the culprit.
image_url: /assets/images/unsplash/PATH.jpg
image_description: |
  Photo by [NAME](https://unsplash.com/USERNAME?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/HASH?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

## Debugging an Android with ADB

The Android Debug Bridge (ADB) is a program to debug apps running on an Android device. It will help you getting to the bottom of crashes, hangs and other glitches. The ADB streams logs from your phone directly to your console so you can dig through them to find the root cause.

## What is ProGuard

```json
{
  "expo": {
    // ...
    "plugins": [
      [
        "expo-build-properties",
        {
          "android": {
            "enableProguardInReleaseBuilds": true,
            "extraProguardRules": "-keep class com.facebook.react.fabric.** { *; }"
          }
        }
      ]
    ]
  }
}
```
