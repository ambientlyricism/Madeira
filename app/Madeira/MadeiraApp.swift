import SwiftUI
import UIKit
import SceneKit

@main
struct MadeiraApp: App {
    final class ViewController: UIViewController {
        var GamepadBridge: GamepadBridge?
        override var prefersPointerLocked: Bool {
            return true
        }
		self.GamepadBridge = GamepadBridge()
		// GamepadBridge()
        // init() {

        // }
        // required init?(coder: NSCoder) {
		//   fatalError("init(coder:) has not been implemented")
	    // }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
