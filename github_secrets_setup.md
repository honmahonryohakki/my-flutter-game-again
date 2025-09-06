# GitHub Secrets 設定ガイド

プッシュが完了したら、以下のSecrets を設定する必要があります：

## 設定場所
1. GitHub リポジトリページに移動
2. **Settings** タブをクリック  
3. 左サイドバーの **Secrets and variables** → **Actions**
4. **New repository secret** をクリック

## 必要なSecrets

### 1. ANDROID_KEYSTORE (Base64エンコード済みキーストア)
```bash
# 後でキーストアファイルをBase64エンコードして設定
# 一時的にダミー値でOK
Name: ANDROID_KEYSTORE
Value: [後で設定]
```

### 2. ANDROID_STORE_PASSWORD
```
Name: ANDROID_STORE_PASSWORD  
Value: android
```

### 3. ANDROID_KEY_ALIAS
```
Name: ANDROID_KEY_ALIAS
Value: key
```

### 4. ANDROID_KEY_PASSWORD
```
Name: ANDROID_KEY_PASSWORD
Value: android
```

### 5. GOOGLE_PLAY_SERVICE_ACCOUNT_JSON (オプション)
```
Name: GOOGLE_PLAY_SERVICE_ACCOUNT_JSON
Value: [Google Play Console API JSON - 後で設定可能]
```

## 注意
- キーストアは GitHub Actions で自動生成されるため、最初はダミー値でOK
- Google Play API は後で設定可能（手動アップロードも可能）