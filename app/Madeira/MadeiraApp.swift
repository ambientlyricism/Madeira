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
		// var GamepadBridge: GamepadBridge?
		// GamepadBridge()
        // required init?(coder: NSCoder) {
		//   fatalError("init(coder:) has not been implemented")
	    // }
    // init() {
		// MadeiraViewController.shared.lockPointer()
		// GamepadBridge.shared.start()
		// GamepadBridge = Madeira.GamepadBridge()
	// }
	// @State private var isPresenting = true
    var body: some Scene {
		WindowGroup {
			// PointerView()
			if DisplaySettings.shared.immersive {
				MadeiraUIViewController()
					.ignoresSafeArea()
			}
			else{
				ContentView()
			// .fullScreenCover(isPresented: $isPresenting, content: { MadeiraViewController() })
			}
   		}
        // .background(Color.black)
	}
}
