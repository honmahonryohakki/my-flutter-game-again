# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flutter game project "my_flutter_game" using Flame engine. Target: fastest possible deployment to Google Play Store with automated CI/CD pipeline.

## Development Commands

### Setup
```bash
# Install Flutter SDK (if not available)
export PATH="$PATH:$HOME/flutter/bin"
flutter doctor

# Initialize project structure
flutter create --platforms=android,ios --org com.katoryo --project-name my_flutter_game .
flutter pub get
```

### Build Commands
```bash
# Development build
flutter run

# Test
flutter test

# Release builds
flutter build appbundle --release  # For Google Play Store
flutter build apk --release       # For testing

# Deploy script
./deploy_to_play_store.sh
```

### Deployment
```bash
# Manual deployment
ANDROID_KEYSTORE_PATH="android/app/keystore.jks" \
ANDROID_KEYSTORE_PASSWORD="android" \
ANDROID_KEY_ALIAS="key" \
ANDROID_KEY_PASSWORD="android" \
./deploy_to_play_store.sh

# Automated deployment (via GitHub Actions)
git tag v1.0.0 && git push origin v1.0.0
```

## Architecture

- **Engine**: Flutter + Flame (v1.15.0)
- **Platform**: Android (primary target), iOS (future)
- **Dependencies**: 
  - audioplayers: v5.2.0
  - google_mobile_ads: v3.1.0
- **Assets**: images/ and sounds/ directories

## Automation

- **CI/CD**: GitHub Actions (`.github/workflows/deploy-android.yml`)
- **Signing**: Keystore-based Android app signing
- **Deployment**: Automated Google Play Console upload via API