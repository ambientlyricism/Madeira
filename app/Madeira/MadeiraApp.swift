import SwiftUI
import UIKit

@main
struct MadeiraApp: App {
    final class ViewController: UIViewController {
        var GamepadBridge = GamepadBridge?
        override var prefersPointerLocked: Bool {
            return true
        }
        init() {
            // GamepadBridge.shared.start()
            GamepadBridge = GamepadBridge()
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
