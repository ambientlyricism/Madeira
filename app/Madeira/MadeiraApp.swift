import SwiftUI
// import UIKit

@main
// final class ViewController: UIViewController {
//   var GamepadBridge: GamepadBridge? 
//   override var prefersPointerLocked: Bool {
//	   return true
//   }
//   override func viewDidLoad() {
//	   super.viewDidLoad()
//   	   GamepadBridge = GamepadBridge()
//   }
// }
// struct MadeiraViewController: UIViewControllerRepresentable {
//	func makeUIViewController(context: Context) -> MetalViewController {
//        return MetalViewController()
//    }
// }
// final class MainSceneDelegate: UIResponder, UIWindowSceneDelegate {
//    var view: UIView?
// }
    
struct MadeiraApp: App {
		// GamepadBridge = GamepadBridge()
		// GamepadBridge()
        // required init?(coder: NSCoder) {
		//   fatalError("init(coder:) has not been implemented")
	    // }
    init() {
		// MadeiraViewController.shared.lockPointer()
		// GamepadBridge.shared.start()
	}
    var body: some Scene {
		WindowGroup {
			// PointerView()
			MadeiraViewController()
			// ContentView()
   		}
	}
}
