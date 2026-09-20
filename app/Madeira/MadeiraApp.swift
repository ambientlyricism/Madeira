import SwiftUI
import UIKit

@main
struct MadeiraApp: App {
    final class ViewController: UIViewController {
        override var prefersPointerLocked: Bool {
            return true
        }
    }
    init() {
        GamepadBridge.shared.start()
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
