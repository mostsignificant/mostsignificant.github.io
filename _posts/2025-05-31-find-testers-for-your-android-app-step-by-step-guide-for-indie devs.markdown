---
layout: post
title: "Find Testers for Your Android App: Step-by-Step Guide for Indie Devs"
date: 2025-05-31 12:00:00 +0200
categories:
comments: true
published: true
excerpt: |
  The Google Play Store requires your app to be tested by at least twelve testers before it can be submitted for review for publishing. Those testers can be hard to find if you don't know that man people with Android devices.
image_url: /assets/images/posts/2025_05_31_android_testing.png
image_description: |
  Android App Testing
---

These testers are not just necessary for Google's review requirements: you also want to get real-world feedback, find bugs, or catch glitches on devices that you can't find in the simulator. At the same time, most indie developers don't have a fully fledged quality assurance department with a dozen testers. This article shows you some alterative ways to find testers without a budget.

## Google Play Store Closed Testing

Before you can apply with your app for access to production, your app has to to fulfill these requirements:

- Publish a closed testing release
- Have at least 12 testers opted-in to your closed test
- Run your closed test with at least 12 testers, for at least 14 days

When your app met these criteria, you can apply for production and start the review process to publish your app.

A closed testing release can be created easily. Within the [Google Play Console](https://play.google.com/console/u/0/developers), you go to "Test and release" and select "Testing". In the drop-down-menu, you select "Closed testing". On the "Closed testing" page you click the "Create track" button to create a new track for closed testing. Within each track, you can add several releases, so you don't have to create a new track for every release.

![Google Play Console Closed Testing](/assets/images/posts/2025_05_31_closed_testing.png "Google Play Console Closed Testing")

After you created a closed testing track, you assign a release. This is the release that the testers will be able to test. Be cautious with release naming, I recommend a [semantic versioning](https://semver.org) scheme: `<Major Version>.<Minor Version>.<Patch Version>`, for example `3.0.3`. You can also add meaning to your major version numbers, for example 2.x.x versions being for internal testing and 3.x.x for closed testing. Any system you come up with should help you to select the correct release version.

## Tester Group

For your managing your testers' accounts using a Google Group is recommended. It also makes it easier for outside testers to join your closed testing track and install any test versions. Head to [Google Groups](https://groups.google.com) and create a tester group with a meaningful name. Your group needs to be set to "Anyone can join" or "Anyone can ask to join" if you're more cautious, but not private/invite-only.

![Google Groups Testing Group](/assets/images/posts/2025_05_31_google_groups.png "Google Groups Testing Group")

After your group is setup, you need to add the group in your Google Play Console's closed testing track underneath the "Tester" tab. There are two options: "Email Lists" and "Google Groups". The option "Emails Lists" allows you to maintain a manual list of email addresses of your testers. If you have enough testers, this option would be sufficient. However, with the "Google Groups" option you are also able to manually add email addresses to the Google group directly. Choose Google Group and add the name of your created group.

Do not forget to save the changes and publish them for review. If you don't publish them you will run in to the same problem as me: while your testers can join the testing group, they are unable to get the app, because the Play Store shows it as non-existing. This took me some time to figure out the root cause, but the notification mark on the "Publishing overview" option in the side menu indicates non-published changes. This page also has the "Managed publishing" option, where Google will publish your changes automatically as soon as they're approved.

## Find Testers

Before reaching out to potential testers, you have to prepare an inviting text that lets them join your Google tester group. Also add the links your app's Android Play Store page and the corresponding web page. You can find those two links in the "Testers" tab on your app's closed testing track in the Google Play Console.

This was the simple text I was using for inviting testers to my app:

> Testing my first game ABZ – would love your feedback! Join the closed test here:
>
> Google Group: https://groups.google.com/g/abzgameclosedtesting
> Android: https://play.google.com/store/apps/details?id=com.mostsignificant.ABZ
> Web: https://play.google.com/apps/testing/com.mostsignificant.ABZ
>
> Thanks in advance!

When it comes to finding testers, you have these options: friends and family, if they have an Android device, your social media followers, if you have any, or open communities like on Reddit, where people help each other out with testing.

Regarding friends and family, I recommend asking them for their Google account email address and adding it directly to the Google group for testing. Then you can send them the link to your Google Play Store where they can install your app test version.

On your social media account, post some screenshots or actual screen recordings of your app with the prepared invitation text. This way people on social media can easily join your testing program if they are interested.

Since my friends and family are mostly Apple users and my social media following is not that big, I had to search for alternatives. There is a community on Reddit called [r/AndroidClosedTesting](https://www.reddit.com/r/AndroidClosedTesting/). On this community, you can tests other people's apps and they will in turn test your app. I was very happy with this community, because the people are very friendly and helping each other out. I made real progress in finding the remaining testers to reach the goal of 12 testers.

![Reddit's r/AndroidClosedTesting Community](/assets/images/posts/2025_05_31_google_groups.png "Reddit's r/AndroidClosedTesting Community")

## Finally

After finding the required testers I was very relieved to read that this requirement was checked off. Now it only requires the 14 days waiting period of testers having the app installed - it does not actually matter if they really test the app for a certain time, testing out real functionality.

> ~~Have at least 12 testers opted-in to your closed test~~

I hope this helps you and your app finding the required testers for your app and speeding up the process in reaching your goal: publishing your app. I wish you all good luck with your apps and as always: keep on coding and keep on creating!
