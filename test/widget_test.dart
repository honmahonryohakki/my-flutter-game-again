import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:my_flutter_game/main.dart';

void main() {
  testWidgets('Game loads successfully', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(MaterialApp(home: GameWidget(game: MyGame())));

    // Verify that the game initializes without errors
    expect(find.byType(GameWidget), findsOneWidget);
  });
}