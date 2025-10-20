# Artify Studio - Cross-Platform Build Instructions

This document provides the final instructions for building the Artify Studio application for Android, iOS, and the web.

## Prerequisites

-   Ensure you have `buildozer` installed (`pip install buildozer`).
-   Make sure you have the necessary dependencies for each platform (e.g., Android NDK/SDK, Xcode).

## Android

To build the Android APK, run the following command:

```bash
buildozer android debug
```

To build the Android AAB for release, run:

```bash
buildozer android release
```

## iOS

**Note:** Building for iOS requires a macOS environment with Xcode installed.

To create the Xcode project, run the following command on your Mac:

```bash
buildozer ios debug
```

This will create an Xcode project in the `ArtifyStudio-iOS` directory. You can then open this project in Xcode to build and run the application on the iOS simulator or a physical device.

## Web

To build the web version of the application, run the following command:

```bash
buildozer web debug
```

This will create a `bin` directory containing the necessary HTML, JS, and WASM files to run the application in a web browser.
