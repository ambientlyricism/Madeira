import SwiftUI
import UIKit

@main
struct MadeiraApp: App {
		// GamepadBridge = GamepadBridge()
		// GamepadBridge()
        // required init?(coder: NSCoder) {
		//   fatalError("init(coder:) has not been implemented")
	    // }
    init() {
		GamepadBridge.GCViewController()
	}
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
