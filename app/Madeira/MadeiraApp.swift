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
		var GamepadBridge: GamepadBridge?
		// GamepadBridge()
        // required init?(coder: NSCoder) {
		//   fatalError("init(coder:) has not been implemented")
	    // }
    init() {
		// MadeiraViewController.shared.lockPointer()
		// GamepadBridge.shared.start()
		GamepadBridge = Madeira.GamepadBridge()
	}
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

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        let configuration = UISceneConfiguration(name: nil, sessionRole: connectingSceneSession.role)
        configuration.delegateClass = SceneDelegate.self
        return configuration
    }
}

class SceneDelegate: NSObject, UIWindowSceneDelegate, ObservableObject { // Make SceneDelegate conform ObservableObject
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        self.window = (scene as? UIWindowScene)?.keyWindow
		// self.window?.rootViewController = UIViewController
    }
}
/*:
struct YourView: View {
    // SceneDelegate is automatically set if it conforms to `ObservableObject`
    @EnvironmentObject var sceneDelegate: SceneDelegate
    var windowScene: UIWindowScene? {
        sceneDelegate.window?.windowScene
    }
}
*/
