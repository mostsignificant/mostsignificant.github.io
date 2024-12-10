---
layout: post
title: "Expo Meets React Native’s New Architecture: How to Make the Switch"
date: 2024-11-18 00:00:00 +0200
categories: React Native Expo
comments: true
published: false
excerpt: |
  React Native unveiled its new architecture with version 0.76. If you are planning to migrate your Expo project to this version, be prepared to navigate a few hurdles to get everything running smoothly again. Don’t worry—this guide has got you covered.

image_url: /assets/images/unsplash/PATH.jpg
image_description: |
  Photo by [NAME](https://unsplash.com/USERNAME?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/HASH?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

These are the basic steps involved in the migration:

- Backup your existing working app
- Check the compatibility of your library dependencies with Expo Doctor
- Enable the new architecture
- Build for Android and iOS
- Fix build issues

If you started your Expo app after version 0.76 you were greeted with the following warning messages:

```sh
 (NOBRIDGE) LOG  Bridgeless mode is enabled
 INFO
 💡 JavaScript logs will be removed from Metro in React Native 0.77! Please use React Native DevTools as your default tool. Tip: Type j in the terminal to open (requires Google Chrome or Microsoft Edge).
 (NOBRIDGE) WARN  🚨 React Native's New Architecture is always enabled in Expo Go, but it is not explicitly enabled your project app config. This may lead to unexpected behavior when you create a production or development build. Set "newArchEnabled": true in your app.json.
Learn more: https://docs.expo.dev/guides/new-architecture/
```

## Preparing for the Big Migration

Before you start, you should backup your working Expo project: either it is already checked in and pushed and even release-tagged or you should do so now. Then you can start either working directly on your main or create a new branch for the migration.

Expo provides a tool called Expo Doctor that helps you check the compatibility of your project’s libraries with the new architecture. It helps you identify the tasks ahead—and might just be the perfect excuse to tidy up and get rid of outdated, unused libraries. Use the following command to check your project’s libraries:

```sh
npx expo-doctor@latest
```

If you have not installed the latest version of the `expo-doctor` package yet, you will have to confirm this:

```sh
Need to install the following packages:
expo-doctor@1.12.4
Ok to proceed? (y) y
```

After running this command, Expo Doctor will check your project for issues, including compatibility with React Native’s new architecture. In my app’s case, it unearthed a lot of other issues I didn’t even know existed. So, if you’ve never used this tool before, brace yourself—you might be in for a _fun_ refactoring weekend.

For the compatibility issues, look out for the following lines in the command’s output:

```sh
✖ Validate packages against React Native Directory package metadata

...

The following issues were found when validating your dependencies against React Native Directory:
Unmaintained: ***
No metadata available: ***

```

In my case, most of my trouble came from the `react-redux` package, its dependencies and `redux-persist`—but more on that later.

You can exclude libraries like these from being checked by Expo Doctor by adding the following lines in your `package.json`. But be careful with this—the library you're excluding might end up being the trouble-maker later on. Think of these entries as your "watch list" of libraries. As the famous saying goes:

> A warning is just an error waiting to happen.

```json
  "expo": {
    "doctor": {
      "reactNativeDirectoryCheck": {
        "exclude": [
          "react-redux",
          "@reduxjs/toolkit",
          "redux-persist"
        ]
      }
    }
  }
```

Highlight the importance of using Expo SDK 52 or newer.
Mention that all expo-\* packages support the New Architecture as of SDK 51.

## Enabling the New Architecture

After the compatibility of the library dependencies are checked, it is time to enable the new architecture in the project.

Within the `app.json` configuration file of our Expo project there is a new option named `newArchEnabled` to enable the new architecture—this option needs to be set to true.

```json
{
  "expo": {
    "newArchEnabled": true
  }
}
```

Working with previous Expo SDK versions 51 and below (which is not encouraged) the option is a bit more embedded deeper in the configuration file’s json tree.

```json
{
  "expo": {
    "plugins": [
      [
        "expo-build-properties",
        {
          "android": {
            "newArchEnabled": true
          },
          "ios": {
            "newArchEnabled": true
          }
        }
      ]
    ]
  }
}
```

Personally, I use Expo Go to test the app initially since I don’t yet have a full iOS build setup on my development machine. My preferred approach is to start the Expo development server with a clean build and test the app live on my device. This helps me catch any initial errors with dependencies or anything else that might have gotten tangled up in the process.

```sh
npx expo start -c
```

After debugging the build on the Expo Go app, the next step is creating a native build. For this, you can either build locally (if you have the necessary tools installed) and then use the [Expo Application Service (EAS)](https://expo.dev/eas), or you can do what I do and rely entirely on EAS. I install the build on my developer device—in my case, an older iPhone in development mode. This helps track down any final issues with the native build, though digging through deeper layers of crash reports is a bit more challenging.

```sh
npx expo prebuild --clean && npx expo run:android
eas build -p android
```

```sh
npx expo prebuild --clean && npx expo run:ios
eas build -p ios
```

## Testing and Troubleshooting

My first build did not work as expected.

With my first app build I ran into a difficult problem–as in difficult to track down. The iOS app was crashing directly on opening. I tried a lot of different things, from attaching with the XCode console, going through the crash reports locally, the crash reports sent from the iOS AppConnect submission and whatnot. In the end, I discovered that a single older library did have the problem: `redux-persist`. I switched to [`redux-remember`](https://github.com/zewish/redux-remember) and the crashing became a thing of the past. Unfortunately this package was also not in the React Native Directory, so I had to exclude it from Expo Doctor's checks, too.

However, you cannot constantly try different things and hope to track down problems efficiently. So here a few things that might help you to get to the root-cause of problems more quickly:

- `npx expo-doctor` as already mentioned to find any issues in general in your Expo project
- `npx expo install --fix` as also already mentioned to find any outdated dependencies
- If you have problems in the Expo Go application already, you can use the available Expo [debugging tools](https://docs.expo.dev/debugging/tools/), for example:
  - opening the developer menu by pressing `m`
  - using the Chrome DevTools by pressing `j`
  - install the [Expo tools VS Code extension](https://github.com/expo/vscode-expo#readme) for debugging in VS Code
  - open the [React DevTools](https://docs.expo.dev/debugging/tools/#debugging-with-react-devtools) to debug components

Be careful with just mindlessly pasting your stack trace and error logs into an AI prompt!

Additionally, here are some still known issues with the new architecture and Expo:

- The background location in the `expo-location` package is not supported (yet) in Expo SDK 52
- Some issues still open in React Native's [GitHub](https://github.com/facebook/react-native/issues?q=is%3Aopen+is%3Aissue+label%3A%22Type%3A+New+Architecture%22)
- Issues with the following libraries:
  - @react-native-community/masked-view: use @react-native-masked-view/masked-view
  - @react-native-community/clipboard: use @react-native-clipboard/clipboard
  - rn-fetch-blob: use react-native-blob-util
  - react-native-fs: use expo-file-system or a fork of react-native-fs
  - react-native-geolocation-service: use expo-location
  - react-native-datepicker: use react-native-date-picker or @react-native-community/datetimepicker
  - (from my own experience) redux-persist: use redux-remember

If your dependency is not listed here, is unmaintained (last commit > 1 year) and your build is failing or app is crashing it might be likely that you need to switch to an alternative. You could fork the library and fix it yourself, but this depends entirely on the free time available to you. on the [React Native Directory](https://reactnative.directory) you will find libraries compatible with the new architecture so you might also be able to find alternatives for older non-compatible libraries.

So get up and bring those dependencies in order.

## Key Considerations for Third-Party Libraries

Discuss potential issues with third-party libraries and solutions:
Check compatibility using React Native Directory.
Replace or patch unsupported libraries.
Emphasize that modules built with the Expo Modules API are already compatible.

## Benefits You’ll Unlock Post-Migration

Recap the tangible and intangible benefits of migrating:
Cleaner architecture.
Better performance.
Easier updates and future-proofing.

## Conclusion

Reassure readers that while the migration process requires effort, it’s a worthwhile investment.
Encourage developers to start with small projects to build confidence.
End with a call to action: share experiences or questions in the comments.
