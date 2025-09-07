#!/usr/bin/env python3
"""
Local AAB Builder for Flutter (macOS/Linux)

What this script does:
- Verifies/installs Flutter SDK (stable) to ~/flutter if missing
- Verifies Java 17
- Verifies/installs Android SDK cmdline-tools to $ANDROID_HOME
- Installs required Android packages (platform-tools, platforms;android-34, build-tools;34.0.0)
- Sets up Android signing (creates keystore + key.properties if missing)
- Runs: flutter clean && flutter pub get && flutter build appbundle --release

Usage (non-interactive example):
  python3 scripts/local_aab_builder.py \
    --store-pass android --key-pass android --key-alias key

Notes:
- This script performs downloads from Google (Flutter/Android SDK). Run it on your own machine.
- It will never commit your keystore or key.properties.
"""

from __future__ import annotations

import os
import sys
import platform
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path
from urllib.request import urlretrieve
from getpass import getpass


FLUTTER_VERSION = "3.24.5"
ANDROID_CMDLINE_VER = "11076708"  # Google published build id


def run(cmd: list[str], env: dict | None = None, cwd: str | None = None) -> None:
    print("$", " ".join(cmd))
    subprocess.check_call(cmd, env=env, cwd=cwd)


def ensure_java17() -> None:
    try:
        out = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT).decode()
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit(
            "Java (JDK) not found. Install Temurin 17: macOS → brew install --cask temurin@17"
        )
    if "version \"17" not in out:
        print(out)
        raise SystemExit("Java 17 required. Please install JDK 17 and retry.")


def ensure_flutter(tmp_dir: Path) -> Path:
    exe = shutil.which("flutter")
    if exe:
        print(f"Found Flutter: {exe}")
        return Path(exe).parent.parent  # .../flutter/bin/flutter -> .../flutter

    home = Path.home()
    flutter_root = home / "flutter"
    if flutter_root.exists():
        print(f"Using existing Flutter at {flutter_root}")
        return flutter_root

    system = platform.system().lower()
    print("Flutter not found. Downloading stable...")
    if system == "darwin":
        url = f"https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_{FLUTTER_VERSION}-stable.zip"
        dest = tmp_dir / "flutter.zip"
        urlretrieve(url, dest)
        with zipfile.ZipFile(dest) as zf:
            zf.extractall(home)
    elif system == "linux":
        url = f"https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_{FLUTTER_VERSION}-stable.tar.xz"
        dest = tmp_dir / "flutter.tar.xz"
        urlretrieve(url, dest)
        with tarfile.open(dest) as tf:
            tf.extractall(home)
    else:
        raise SystemExit("Unsupported OS. Use macOS or Linux.")

    print("Flutter installed at:", flutter_root)
    print("Be sure your PATH includes:", flutter_root / "bin")
    return flutter_root


def ensure_android_sdk(tmp_dir: Path) -> Path:
    system = platform.system().lower()
    if system == "darwin":
        default_home = Path.home() / "Library/Android/sdk"
        clt_url = f"https://dl.google.com/android/repository/commandlinetools-mac-{ANDROID_CMDLINE_VER}_latest.zip"
    elif system == "linux":
        default_home = Path.home() / "Android/Sdk"
        clt_url = f"https://dl.google.com/android/repository/commandlinetools-linux-{ANDROID_CMDLINE_VER}_latest.zip"
    else:
        raise SystemExit("Unsupported OS for Android SDK. Use macOS or Linux.")

    android_home = Path(os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or default_home)
    tools_bin = android_home / "cmdline-tools" / "latest" / "bin"
    if not tools_bin.exists():
        print(f"Android cmdline-tools not found. Installing into {android_home}...")
        android_home.mkdir(parents=True, exist_ok=True)
        zip_path = tmp_dir / "cmdline-tools.zip"
        urlretrieve(clt_url, zip_path)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp_dir / "clt")
        # Move into .../cmdline-tools/latest
        # downloaded content includes a 'cmdline-tools' dir
        extracted_root = next((tmp_dir / "clt").iterdir())
        dest = android_home / "cmdline-tools" / "latest"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(extracted_root), str(dest))

    # Install required packages
    sdkmanager = str(tools_bin / "sdkmanager")
    env = os.environ.copy()
    env.setdefault("ANDROID_HOME", str(android_home))
    env.setdefault("ANDROID_SDK_ROOT", str(android_home))

    try:
        run([sdkmanager, "--version"], env=env)
    except Exception as e:
        raise SystemExit(f"sdkmanager failed: {e}")

    pkgs = [
        "platform-tools",
        "platforms;android-35",
        "build-tools;35.0.0",
    ]
    run([sdkmanager, "--install", *pkgs], env=env)

    # Accept licenses
    try:
        p = subprocess.Popen([sdkmanager, "--licenses"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        if p.stdin:
            p.stdin.write(b"y\n" * 50)
            p.stdin.flush()
        p.communicate()
    except Exception:
        pass

    return android_home


def ensure_signing(project_root: Path, store_pass: str | None, key_pass: str | None, key_alias: str | None) -> None:
    app_dir = project_root / "android" / "app"
    keystore = app_dir / "keystore.jks"
    key_props = project_root / "android" / "key.properties"

    if not store_pass:
        store_pass = getpass("Keystore password (storePassword): ")
    if not key_pass:
        key_pass = getpass("Key password (keyPassword): ")
    if not key_alias:
        key_alias = input("Key alias (default 'key'): ") or "key"

    if not keystore.exists():
        print("Generating keystore at", keystore)
        app_dir.mkdir(parents=True, exist_ok=True)
        run([
            "keytool", "-genkey", "-v",
            "-keystore", str(keystore),
            "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
            "-alias", key_alias,
            "-storepass", store_pass,
            "-keypass", key_pass,
            "-dname", "CN=Upload,O=MyOrg,C=JP",
        ])

    if not key_props.exists():
        print("Writing", key_props)
        key_props.write_text(
            """
storePassword={store}
keyPassword={key}
keyAlias={alias}
storeFile=keystore.jks
""".strip().format(store=store_pass, key=key_pass, alias=key_alias)
            + "\n"
        )


def build_aab(project_root: Path, flutter_root: Path | None) -> None:
    env = os.environ.copy()
    if flutter_root is not None:
        env["PATH"] = f"{flutter_root / 'bin'}:{env['PATH']}"

    run(["flutter", "doctor", "-v"], env=env, cwd=str(project_root))
    run(["flutter", "clean"], env=env, cwd=str(project_root))
    run(["flutter", "pub", "get"], env=env, cwd=str(project_root))
    run(["flutter", "build", "appbundle", "--release"], env=env, cwd=str(project_root))
    out = project_root / "build/app/outputs/bundle/release/app-release.aab"
    if out.exists():
        print("AAB built:", out)
    else:
        raise SystemExit("AAB not found. Build failed.")


def main(argv: list[str]) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Local Flutter AAB builder")
    parser.add_argument("--store-pass")
    parser.add_argument("--key-pass")
    parser.add_argument("--key-alias")
    parser.add_argument("--skip-install", action="store_true", help="Skip installing Flutter/Android SDK")
    args = parser.parse_args(argv)

    project_root = Path(__file__).resolve().parents[1]
    tmp_dir = project_root / ".tmp_local_build"
    tmp_dir.mkdir(exist_ok=True)

    ensure_java17()

    flutter_root = None
    android_home = None
    if not args.skip_install:
        flutter_root = ensure_flutter(tmp_dir)
        android_home = ensure_android_sdk(tmp_dir)
        print("ANDROID_HOME:", android_home)
    else:
        print("Skipping SDK installs as requested. Make sure flutter and sdkmanager are in PATH.")

    ensure_signing(project_root, args.store_pass, args.key_pass, args.key_alias)
    build_aab(project_root, flutter_root)

    # Cleanup temp folder (best-effort)
    try:
        shutil.rmtree(tmp_dir)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)
