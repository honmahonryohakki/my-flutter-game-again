import 'package:flame/game.dart';
import 'package:flame/flame.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MaterialApp(home: GameWidget<MyGame>.controlled(gameFactory: MyGame.new)));
}

class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // ゲーム初期化処理
    print("Game loaded!");
  }
}
