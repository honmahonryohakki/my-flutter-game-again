import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:my_flutter_game/main.dart';

void main() {
  testWidgets('Game loads successfully', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(MyApp());

    // Verify that the game screen loads
    expect(find.text('My Flutter Game'), findsOneWidget);
    expect(find.text('Score:'), findsOneWidget);
    expect(find.text('0'), findsOneWidget);
    expect(find.text('Tap to Score!'), findsOneWidget);
  });

  testWidgets('Tap increments score', (WidgetTester tester) async {
    await tester.pumpWidget(MyApp());

    // Find the button and tap it
    await tester.tap(find.text('Tap to Score!'));
    await tester.pump();

    // Verify score increased
    expect(find.text('1'), findsOneWidget);
  });
}
