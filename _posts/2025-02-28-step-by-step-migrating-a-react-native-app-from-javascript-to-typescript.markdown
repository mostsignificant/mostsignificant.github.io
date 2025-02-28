---
layout: post
title: "Step-by-Step: Migrating a React Native App from JavaScript to TypeScript"
date: 2025-02-28 00:00:00 +0200
categories:
comments: true
published: true
excerpt: |
  JavaScript is a powerful language. But it needs safeguards so you don't shoot yourself in the foot. That's what TypeScript is for. I made the mistake of starting my React Native mobile app written purely in JavaScript. Here's how to migrate to the safer alternative.
image_url: /assets/images/posts/2025_02_22_from_javascript_to_typescript.jpeg
image_description: |
  Migrating a React Native App from JavaScript to TypeScript
---

I was used to statically-typed languages like C++. But when I started mobile app development with React Native, I instantly liked the freedom of JavaScript. This introduced a whole new type of bugs that were related to the freedom of types in JavaScript (everything is an object).

That's where TypeScript comes into play. This language adds the missing static typing and type annotations to JavaScript. So I decided to leave pure JavaScript behind in favor of TypeScript and migrate my mobile app _ABZ Game_. There are different approaches for migration. I chose a one-and-done approach: convert every source code file from JavaScript to TypeScript at once. This might take longer, but a slow Sunday is perfect for a little bit of refactoring.

But why actually do all this extra work, which a user might not even notice directly? TypeScript will help you discover mistakes that you might not even have noticed yet. I expected to find some whoopsies that just didn't surface yet. If there are parts of your mobile app that you don't use or test often, a hidden bug can be very likely to hide there.

So these are the basic steps I took to migrate:

- Setting up TypeScript in the React Native project
- Renaming the file from JavaScript to TypeScript
- Convert the source code to TypeScript
- Rerun a clean build with tests

So let's get started.

## Setting Up TypeScript in a React Native Project

First up, the project has to get TypeScript-ready. There are two libraries that need to be installed:

- [`typescript`](https://www.npmjs.com/package/typescript) contains the actual compiler turning your TypeScript code into safe JavaScript, complaining if there are missing type annotations or variable declarations, mismatching types in function calls or other unsafe type usage.
- [`@types/react`](https://www.npmjs.com/package/@types/react) has all the type definitions that you need for React, for example the `useState<...>(...)` hook.

I also found on the internet the recommendation to install [`@types/react-native`](https://www.npmjs.com/package/@types/react-native). But this package is deprecated. Modern React Native already comes with its type definitions included.

Now install these necessary dependencies via npm:

```bash
npm install --save-dev typescript @types/react
```

Or install via Expo if you're using an Expo project:

```bash
npx expo install typescript @types/react
npx expo install --fix
```

Create a tsconfig.json with strict mode enabled:

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ESNext",
    "moduleResolution": "Node",
    "jsx": "react-native",
    "noImplicitAny": true,
    "skipLibCheck": true
  },
  "extends": "expo/tsconfig.base"
}
```

The `extends` option refers to Expo's included `tsconfig` file. If you are using pure React Native, you need to refer to this file:

```jsonc
{
  //...
  "extends": "@tsconfig/react-native/tsconfig.json"
}
```

At the beginning, TypeScript might be complaining about not finding any inputs. That is the case if your project like mine doesn't have any TypeScript files yet. Typescript files typically end in _.ts_ or _.tsx_. So let's start renaming files.

```bash
No inputs were found in config file '.../tsconfig.json'. Specified 'include' paths were '["**/*"]' and 'exclude' paths were '[]'.ts
```

## Renaming Files to TypeScript

We will fix the compiler's complaint by turning the existing JavaScript files into TypeScript files.

First step: we rename _.js_ to _.tsx_ for source files containing components. This can be done simply via command line. However, using command line requires that all component files are in a specific path or several paths, clearly separated from the rest (otherwise you've to do this manually). For my mobile app _ABZ Game_, this affected a few folders in the project structure: `/dialogs`, `/elements`, `/screens`, and `/views`. It also includes the `App.js` file, which becomes `App.tsx`. The following command assumes that you used the _.jsx_ file ending for components from the beginning. I did not, that is why I renamed the components by hand first.

### Unix or MacOS (bash)

```bash
find src -type f -name "*.js" -exec bash -c 'mv "$0" "${0%.js}.ts"' {} \;
find src -type f -name "*.jsx" -exec bash -c 'mv "$0" "${0%.jsx}.tsx"' {} \;
```

Replace the `src` part with the path to your project's' files. The command `find` searches through the directories, the option `-type f` only looks at files (not directories), the expression `-name "*.js"` looks at files ending only in _.js_ and, and the commando ` -exec bash -c 'mv "$0" "${0%.js}.ts"' {} \;` renames them to _.ts_. Then it does the same again for renaming _.jsx_ to _.tsx_.

### Windows (PowerShell)

```bash
Get-ChildItem -Path src -Recurse -Filter *.js | Rename-Item -NewName { $_.Name -replace '\.js$', '.ts' }
Get-ChildItem -Path src -Recurse -Filter *.jsx | Rename-Item -NewName { $_.Name -replace '\.jsx$', '.tsx' }
```

After renaming, the really fun part begins. Start by running the TypeScript compiler to identify errors:

```bash
npx tsc --noEmit
```

```bash
...
Found 360 errors in 48 files.
Errors  Files
     1  App.tsx:1
     5  src/context/GameContext.tsx:1
     5  src/dialogs/AchievementsResetDialog.tsx:6
     8  src/dialogs/ConfirmationDialog.tsx:6
     9  src/dialogs/DailyTimeLimitDialog.tsx:1
     7  src/dialogs/GameOverDialog.tsx:8
    46  src/dialogs/GameTutorialDialog.tsx:12
...
```

360 errors sounds like a lot of work (spoiler: it was).

## Converting To TypeScript

The new TypeScript files need type definitions and annotations.

If you're unfamiliar with the language, you can get started [here](https://www.typescriptlang.org/docs/handbook/intro.html). Microsoft even offers an online [Playground](https://www.typescriptlang.org/play).

You begin by converting the components to TypeScript. In my mobile app I had this pure-Javascript component which shows a confirmation dialog if the user wants to reset its achievements. It's compact and straight-forward to make it TypeScript-ready.

```javascript
export const AchievementsResetDialog = ({ onReset, onCancel }) => {
  return (
    <OverlayDialog title="Do You Really Want To Reset Stats And Achievements?">
      <View style={styles.buttonRow}>
        <Button
          title={"Cancel"}
          onPress={() => onCancel()}
          invertColors={true}
        />
        <Button
          title={"Yes, Reset!"}
          onPress={() => onReset()}
          invertColors={true}
        />
      </View>
    </OverlayDialog>
  );
};
```

TypeScript requires you to annotate the type of properties you're passing to the component. To achieve this you declare an extra `Props` type, named like your component for consistency. In my mobile app's example, this would be `AchievementsResetDialogProps`. There is no need to shy away from slightly longer variable and type names in my opinion.

```javascript
type AchievementsResetDialogProps = {
  onReset: () => void,
  onCancel: () => void,
};
```

When you created these props, you need to tell TypeScript that only properties of this type can be passed to the component. There are two ways to do this. The first way tells the component to conform to `React.FC<Props>`. The second way is more common in modern React and just tells the argument to be of your prop's type. I always go with the second option because of its readability.

```javascript
export const AchievementsResetDialog: React.FC<
  AchievementsResetDialogProps
> = ({ onReset, onCancel }) => {
  // ...
};
```

```javascript
export const AchievementsResetDialog = ({
  onReset,
  onCancel,
}: AchievementsResetDialogProps) => {
  // ...
};
```

### Redux

If you're using `react-redux` you noticed that the TypeScript compiler is complaining about every untyped `useSelector` and `useDispatch` call. To overcome these errors you do two things: Define types for your project's `RootState` and `AppDispatch` and create your own typed versions of `useSelector` and `useDispatch`.

At the end of your `store.ts` file (or wherever you defined your root state), you add the following two exports:

```javascript
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

In a separate file, you define your typed versions of `useSelector` and `useDispatch`. I use the file `hooks/react-redux.ts` so I can overwrite all existing imports from the original `react-redux` library with my own definitions.

```javascript
import {
  TypedUseSelectorHook,
  useDispatch as useReduxDispatch,
  useSelector as useReduxSelector,
} from "react-redux";

import type { AppDispatch, RootState } from "../store";

export const useDispatch = () => useReduxDispatch<AppDispatch>();
export const useSelector: TypedUseSelectorHook<RootState> = useReduxSelector;
```

### Navigation

The way you use navigation changes slightly, too. I am using the `@react-navigation/native-stack` library. Each use of navigation requires the definition of each route's parameters. Start by creating a `./types/navigation.ts` file and adding each used route.

```typescript
import { GridSize } from "../util/grid";

export type RootStackParamList = {
  Home: undefined;
  Game: { size: GridSize };
  GameSettings: undefined;
  Achievements: undefined;
  Options: undefined;
  About: undefined;
};
```

You create a navigation object with a typed function call. This created object can be used as always.

```typescript
const navigation =
  useNavigation<NativeStackNavigationProp<RootStackParamList>>();
```

Within your app's screen (where you create the stack navigation), you also need the typed version of the function call.

```typescript
const Stack = createNativeStackNavigator<RootStackParamList>();
```

## Rebuild From Scratch

When you're finished with all TypeScript changes, you have to run a clean build. In an Expo project, you remove the folder with build artifacts (`rm -rf ios && rm -rf android`). After cleaning up, you can start the build process when doing a native build (`npx expo run:ios`) or run Expo with a clean cache (`expo start -c`). Make sure that your project is starting up cleanly as it used to. My app worked as before, so there was no additional fixing of bugs required. I also fixed my tests to be TypeScript-ready and made sure every test was passing.

## Lessons Learned

I have to admit that converting all files from Javascript to Typescript took way longer than expected. But I did actually find some bugs and was able to fix them. Javascript's relaxed handling of definitions (or having none) lets some bugs slip away unnoticed.

During the refactoring I encountered problems with the `react-native-google-mobile-ads` package. Its library dependencies and my Expo and React Native versions lead to a workaround solution in my app. I had to disable the Typescript linter for the `BannerAd` component in my source code.

```typescript
/* tslint:disable */
const CustomBannerAd: any = BannerAd;
/* tslint:enable */
```

Switching to TypeScript was definitely worth it. Instead of a Sunday evening, I spent way more time on this (supposedly) little refactoring. But I am definitely starting my next app using TypeScript and I recommend you do, too. Bugs found in development are less troublesome than bugs found by a user.

So as always: keep on coding and keep on creating.
