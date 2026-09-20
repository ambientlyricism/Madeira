import SwiftUI
import UIKit

@main
struct MadeiraApp: App {
    final class ViewController: UIViewController {
        var GamepadBridge: GameController?
        override var prefersPointerLocked: Bool {
            return true
        }
        init() {
            // GamepadBridge.shared.start()
            self.GamepadBridge = GamepadBridge()
        }
        required init?(coder: NSCoder) {
		    fatalError("init(coder:) has not been implemented")
	    }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
