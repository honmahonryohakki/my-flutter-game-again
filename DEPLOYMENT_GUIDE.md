# Flutter Game - Google Play Store 最速デプロイメントガイド

## 🚀 クイックスタート（最速手順）

### ステップ 1: Flutter SDK セットアップ
```bash
# Flutterのダウンロードが完了したら
cd ~
unzip flutter_macos_3.24.5-stable.zip
export PATH="$PATH:`pwd`/flutter/bin"
echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.zshrc
```

### ステップ 2: プロジェクト初期化
```bash
cd /Users/katoryo/Desktop/game_gpt
flutter create --platforms=android,ios --org com.katoryo --project-name my_flutter_game .
flutter pub get
```

### ステップ 3: アプリ署名の設定
```bash
# キーストア生成
keytool -genkey -v -keystore android/app/keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias key -storepass android -keypass android

# key.properties ファイル作成
cat > android/key.properties << EOF
storePassword=android
keyPassword=android
keyAlias=key
storeFile=keystore.jks
EOF
```

### ステップ 4: 即座にビルド・デプロイ
```bash
# デプロイスクリプト実行
chmod +x deploy_to_play_store.sh
ANDROID_KEYSTORE_PATH="android/app/keystore.jks" \
ANDROID_KEYSTORE_PASSWORD="android" \
ANDROID_KEY_ALIAS="key" \
ANDROID_KEY_PASSWORD="android" \
./deploy_to_play_store.sh
```

## 📱 Google Play Console 設定

### 前提条件
1. Google Play デベロッパーアカウント（$25の登録料が必要）
2. Google Playアプリ署名の有効化

### アプリ作成手順
1. [Google Play Console](https://play.google.com/console) にログイン
2. 「アプリを作成」をクリック
3. 以下の情報を入力：
   - **アプリ名**: My Flutter Game
   - **デフォルトの言語**: 日本語
   - **アプリまたはゲーム**: ゲーム
   - **無料または有料**: 無料

### 必要な素材
- **アプリアイコン**: 512x512 PNG
- **スクリーンショット**: 最低2枚（1080x1920）
- **アプリの説明**: 簡潔で魅力的な説明文
- **プライバシーポリシー**: 必須（簡易版でも可）

## 🤖 自動化設定

### GitHub Secrets 設定
```bash
# GitHubリポジトリの Settings > Secrets and variables > Actions で設定

ANDROID_KEYSTORE: (base64エンコードしたkeystore.jks)
ANDROID_STORE_PASSWORD: android
ANDROID_KEY_ALIAS: key
ANDROID_KEY_PASSWORD: android
GOOGLE_PLAY_SERVICE_ACCOUNT_JSON: (Google Play Console API JSON)
```

### 自動デプロイの有効化
1. コードをGitHubにプッシュ
2. タグを作成してプッシュ: `git tag v1.0.0 && git push origin v1.0.0`
3. GitHub Actionsが自動的にビルド・デプロイを実行

## ⚡ 最速アップロード戦略

### Phase 1: 緊急手動アップロード（推定時間: 2-3時間）
1. **Flutter環境構築**: 30分
2. **アプリ設定・ビルド**: 30分
3. **Play Console設定**: 60分
4. **審査提出**: 30分

### Phase 2: 自動化実装（推定時間: 1-2時間）
1. **GitHub Actions設定**: 30分
2. **Google Play API設定**: 60分
3. **テスト・デバッグ**: 30分

## 🔧 トラブルシューティング

### よくある問題と解決法

#### Flutter SDK インストール失敗
```bash
# Homebrewが失敗した場合の手動インストール
curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_3.24.5-stable.zip
unzip flutter_macos_3.24.5-stable.zip
export PATH="$PATH:`pwd`/flutter/bin"
flutter doctor
```

#### ビルドエラー
```bash
# キャッシュクリア
flutter clean
flutter pub get
flutter build appbundle --release
```

#### 署名エラー
```bash
# キーストアの再確認
keytool -list -v -keystore android/app/keystore.jks
```

## 📋 チェックリスト

### 公開前必須チェック
- [ ] アプリが正常に起動する
- [ ] クラッシュしない
- [ ] 必要な権限が設定済み
- [ ] プライバシーポリシーが準備済み
- [ ] 年齢制限が適切に設定
- [ ] Google Play ポリシーに準拠

### 自動化チェック
- [ ] GitHub Actions が正常に動作する
- [ ] 署名済みAPK/AABが生成される
- [ ] Google Play Console API が正常に動作する

## 🎯 次のステップ

1. **即座に実行**: Flutter SDK インストール完了後、上記のクイックスタート手順を実行
2. **並行作業**: Google Play デベロッパーアカウントの登録（未登録の場合）
3. **最適化**: 公開後の分析とアプリ改善

---

**推定総作業時間**: 3-5時間（手動）+ 1-2時間（自動化）
**最短公開時間**: Google Play審査時間（通常1-3日）を除き、当日中に提出可能