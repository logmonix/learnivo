# Mobile Environment Setup Guide

It appears your environment is missing the Android SDK, which is required to run the React Native app on an Android emulator or device directly from your machine.

## 🛑 The Issue
The error `Failed to resolve the Android SDK path` generally means:
1.  **Android Studio** is not installed.
2.  Or, the `ANDROID_HOME` environment variable is not set.

## ✅ Solution 1: Use the Web Version (Fastest)
The project is configured to run on the web as well. This is the easiest way to start developing without installing heavy Android tools.
1.  Navigate to `mobile` directory.
2.  Run `npm run web`.
3.  Open `http://localhost:8081` in your browser.

## 🛠️ Solution 2: Install Android Studio (Recommended for Mobile Dev)
1.  **Download Android Studio**: [https://developer.android.com/studio](https://developer.android.com/studio)
2.  **Install**: Follow the installation wizard. **Ensure you check the box for "Android SDK"** and "Android Virtual Device" during setup.
3.  **Set Environment Variables**:
    Add the following to your `~/.zshrc` or `~/.bash_profile`:
    ```bash
    export ANDROID_HOME=$HOME/Library/Android/sdk
    export PATH=$PATH:$ANDROID_HOME/emulator
    export PATH=$PATH:$ANDROID_HOME/platform-tools
    ```
4.  **Restart Terminal**: logical to apply changes.
5.  **Verify**: Run `adb --version`.

## 🍎 Solution 3: iOS (Mac Users Only)
If you have Xcode installed:
1.  Open Xcode and ensure "Command Line Tools" are selected in Settings.
2.  Run `npm run ios`.

---
**Current Status**: We are proceeding with the **Web** version for development to ensure progress while you tackle the setup if desired.
