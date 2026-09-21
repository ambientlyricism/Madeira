import Foundation
import GameController
import CoreHaptics
import UIKit
import SwiftUI

/// Feeds GameController.framework pads to Wine's XInput.
///
/// There is no HID stack under Wine on iOS, so xinput1_3 runs in "host
/// mode" and reads the pad table in xinput_host_ios.c. This class fills that
/// table: every connected GCExtendedGamepad (DualSense, DualShock 4, Xbox,
/// MFi — iOS normalises them all to Xbox-positional names) gets an XInput
/// slot, and the touch overlay's pad buttons are merged into slot 0.
///
/// Everything runs on the main queue: GC handlers, touch gestures and the
/// rumble poll timer.
// struct GCViewController: UIViewControllerRepresentable {
//   var ViewController: ViewController?
//   ViewController = ViewController() 
// }
// final class ViewController: UIHostingController {
//	static let shared = ViewController()
//	var GamepadBridge: GamepadBridge?
//	var shouldLockPointer: Bool = true
//	override var prefersPointerLocked: Bool {
//		return self.shouldLockPointer
//	}
//	func lockPointer() {
//		self.shouldLockPointer = true
//		setNeedsUpdateOfPrefersPointerLocked()
//		GamepadBridge = Madeira.GamepadBridge()
//	}
// }
final class GamepadBridge {
   static let shared = GamepadBridge()
   func start() {
        if #available(iOS 14.0, OSX 10.16, *) {
            NotificationCenter.default.addObserver(self, selector: #selector(self.handleMouseDidConnect),
                                                   name: NSNotification.Name.GCMouseDidBecomeCurrent, object: nil)
            NotificationCenter.default.addObserver(self, selector: #selector(self.handleMouseDidDisconnect),
                                                   name: NSNotification.Name.GCMouseDidStopBeingCurrent, object: nil)
            if let mouse = GCMouse.mice().first {
                registerMouse(mouse)
                MetalViewController.shared.lockPointer()
            }
        }
        // NotificationCenter.default.addObserver(self, selector: #selector(self.handleKeyboardDidConnect),
        //                                       name: NSNotification.Name.GCKeyboardDidConnect, object: nil)
   }
    
   // @objc
   // func handleKeyboardDidConnect(_ notification: Notification) {
   //     guard let keyboard = notification.object as? GCKeyboard else {
   //         return
   //     }
   // }

    var delta: CGPoint = CGPoint.zero
    var keyboard: GCKeyboard? = nil
    
    @objc
    func handleMouseDidConnect(_ notification: Notification) {
        if #available(iOS 14.0, OSX 10.16, *) {
            guard let mouse = notification.object as? GCMouse else {
                return
            }
            
            unregisterMouse()
            registerMouse(mouse)
            
        }
    }
    
    @objc
    func handleMouseDidDisconnect(_ notification: Notification) {
        unregisterMouse()
    }
    
    func unregisterMouse() {
        delta = CGPoint.zero
        
    }
    var dx : Int32 = 0
    var dy : Int32 = 0
    var sy : Int32 = 0
    
    func registerMouse(_ mouseDevice: GCMouse) {
        if #available(iOS 14.0, OSX 10.16, *) {
            guard let mouseInput = mouseDevice.mouseInput else {
                return
            }
            
            mouseInput.mouseMovedHandler = {(_ mouse: GCMouseInput, _ deltaX: Float, _ deltaY: Float) -> Void in
                self.dx = self.dx+Int32(deltaX)
                self.dy = self.dy-Int32(deltaY)
                self.delta = CGPoint(x: CGFloat(deltaX), y: CGFloat(deltaY))
                winios_pointer(self.dx, self.dy, 0x0001 | 0x8000, 0)
            }
            mouseInput.scroll.valueChangedHandler = {
                (_ cursor: GCControllerDirectionPad, _ scrollX: Float, _ scrollY: Float) -> Void in
                // self.sy = self.sy+Int32(scrollY)
                winios_pointer(0, 0, 0x0800, UInt32(bitPattern: Int32(scrollY)))
            }
            mouseInput.leftButton.valueChangedHandler = {
                (_ button: GCControllerButtonInput, _ value: Float, _ pressed: Bool) -> Void in
               if pressed {
                  winios_pointer(0, 0, 0x0002, 0)
               }
               else {
                  winios_pointer(0, 0, 0x0004, 0)
               }
            }
            mouseInput.rightButton?.valueChangedHandler = {
                (_ button: GCControllerButtonInput, _ value: Float, _ pressed: Bool) -> Void in
               if pressed {
                  winios_pointer(0, 0, 0x0008, 0)
               }
               else {
                  winios_pointer(0, 0, 0x0010, 0)
               }
            }
        }
    }
    func GCMouseInputX() -> CGFloat {
       return self.delta.x
    }
    func GCMouseInputY() -> CGFloat {
       return self.delta.y
    }
    func MouseActive() -> Bool {
       return self.delta.x != 0 || self.delta.y != 0
    }
    
}
