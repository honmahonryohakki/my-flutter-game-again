#!/bin/bash

# Google Play Store 自動デプロイメントスクリプト
# 使用方法: ./deploy_to_play_store.sh

set -e

echo "🚀 Google Play Store へのデプロイメントを開始します..."

# 環境変数チェック
if [ -z "$ANDROID_KEYSTORE_PATH" ] || [ -z "$ANDROID_KEYSTORE_PASSWORD" ] || [ -z "$ANDROID_KEY_ALIAS" ] || [ -z "$ANDROID_KEY_PASSWORD" ]; then
    echo "❌ 署名用の環境変数が設定されていません"
    echo "必要な環境変数:"
    echo "  ANDROID_KEYSTORE_PATH"
    echo "  ANDROID_KEYSTORE_PASSWORD" 
    echo "  ANDROID_KEY_ALIAS"
    echo "  ANDROID_KEY_PASSWORD"
    exit 1
fi

# Flutterプロジェクトかチェック
if [ ! -f "pubspec.yaml" ]; then
    echo "❌ Flutterプロジェクトではありません"
    exit 1
fi

echo "📦 依存関係をインストール中..."
flutter pub get

echo "🧪 テストを実行中..."
flutter test

echo "🔧 Androidリリースビルドを作成中..."
flutter build appbundle --release

# APKも生成（テスト用）
echo "📱 APKを作成中..."
flutter build apk --release

# ビルド成果物のパス
APP_BUNDLE_PATH="build/app/outputs/bundle/release/app-release.aab"
APK_PATH="build/app/outputs/flutter-apk/app-release.apk"

# ビルド成果物の存在確認
if [ ! -f "$APP_BUNDLE_PATH" ]; then
    echo "❌ App Bundle ビルドに失敗しました"
    exit 1
fi

if [ ! -f "$APK_PATH" ]; then
    echo "❌ APK ビルドに失敗しました"
    exit 1
fi

echo "✅ ビルド完了"
echo "📦 App Bundle: $APP_BUNDLE_PATH"
echo "📱 APK: $APK_PATH"

# ファイルサイズを表示
echo "ファイルサイズ:"
ls -lh "$APP_BUNDLE_PATH"
ls -lh "$APK_PATH"

# Google Play Console APIを使用してアップロード（オプション）
if [ -n "$GOOGLE_PLAY_SERVICE_ACCOUNT_JSON" ]; then
    echo "🚀 Google Play Console にアップロード中..."
    # fastlane や google-play-cli を使用してアップロード
    # ここではスケルトンのみ
    echo "⚠️  自動アップロード機能は後で実装します"
else
    echo "📋 手動アップロード用のファイルが準備されました"
    echo "Google Play Console (https://play.google.com/console) にログインして"
    echo "以下のファイルをアップロードしてください:"
    echo "  $APP_BUNDLE_PATH"
fi

echo "🎉 デプロイメントプロセス完了!"