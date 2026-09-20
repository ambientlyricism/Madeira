import SwiftUI
import UIKit

@main
struct MadeiraApp: App {
		// GamepadBridge = GamepadBridge()
		// GamepadBridge()
        init() {
			GamepadBridge.shared.start()
        }
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
