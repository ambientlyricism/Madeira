import SwiftUI

@main
struct MadeiraApp: App {
    var GamepadBridge: GamepadBridge?
    init() {
		GamepadBridge = Madeira.GamepadBridge()
	}
    var body: some Scene {
        WindowGroup {
            ContentView()
                .modifier(ClaimGamepadEvents())
                .onAppear { GamepadInput.shared.start() }
        }
    }
}
