import SwiftUI
import UIKit

@main
final class ViewController: UIViewController {
   var GamepadBridge: GamepadBridge? 
   override var prefersPointerLocked: Bool {
	   return true
   }
   GamepadBridge = GamepadBridge()
}
struct MadeiraApp: App {
		// GamepadBridge = GamepadBridge()
		// GamepadBridge()
        // required init?(coder: NSCoder) {
		//   fatalError("init(coder:) has not been implemented")
	    // }
    init() {
		GamepadBridge.shared.start()
	}
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
