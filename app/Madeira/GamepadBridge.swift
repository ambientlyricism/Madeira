import Foundation
import GameController
import CoreHaptics
// import UIKit
// import SwiftUI

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
   init() {
      start()
   }
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
        NotificationCenter.default.addObserver(self, selector: #selector(self.handleKeyboardDidConnect),
                                               name: NSNotification.Name.GCKeyboardDidConnect, object: nil)
   }
    var delta: CGPoint = CGPoint.zero
    var keyboard: GCKeyboard? = nil
    var key: Int32 = 0
    
   @objc
   func handleKeyboardDidConnect(_ notification: Notification) {
      guard let keyboard = notification.object as? GCKeyboard else {
         return
      }
      keyboard.keyboardInput?.keyChangedHandler = {
            ( _ keyboard, _ button: GCDeviceButtonInput, _ value: GCKeyCode, _ pressed: Bool) -> Void in
               // guard pressed else {
               //   return
               // }
               MetalHostingController.shared.lockPointer()
               MetalViewController.shared.lockPointer()
               let code = Int(value.rawValue)
               let key = MadeiraKeys.virtualKey(hid: code) ?? Int32(0)
               winios_post_key(key, pressed ? 1 : 0)
      }
         
   }
    
    @objc
    func handleMouseDidConnect(_ notification: Notification) {
        if #available(iOS 14.0, OSX 10.16, *) {
            guard let mouse = notification.object as? GCMouse else {
                return
            }
            MetalHostingController.shared.lockPointer()
            MetalViewController.shared.lockPointer()
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
    var MouseMoving = false
    var MouseClicking = false
    
    func registerMouse(_ mouseDevice: GCMouse) {
        self.MouseMoving = false
        self.MouseClicking = false
        if #available(iOS 14.0, OSX 10.16, *) {
            guard let mouseInput = mouseDevice.mouseInput else {
                return
            }
            
            mouseInput.mouseMovedHandler = {(_ mouse: GCMouseInput, _ deltaX: Float, _ deltaY: Float) -> Void in
                self.dx = self.dx+Int32(deltaX)
                self.dy = self.dy-Int32(deltaY)
                self.delta = CGPoint(x: CGFloat(deltaX), y: CGFloat(deltaY))
                MetalHostingController.shared.lockPointer()
                MetalViewController.shared.lockPointer()
                if deltaX != 0 || deltaY != 0 {
                   self.MouseMoving = true
                }
                else {
                   self.MouseMoving = false
                }
                winios_pointer(self.dx, self.dy, 0x0001 | 0x8000, 0)
            }
            mouseInput.scroll.valueChangedHandler = {
                (_ cursor: GCControllerDirectionPad, _ scrollX: Float, _ scrollY: Float) -> Void in
                // self.sy = self.sy+Int32(scrollY)
                MetalHostingController.shared.lockPointer()
                MetalViewController.shared.lockPointer()
                winios_pointer(0, 0, 0x0800, UInt32(bitPattern: Int32(scrollY)))
            }
            mouseInput.leftButton.valueChangedHandler = {
                (_ button: GCControllerButtonInput, _ value: Float, _ pressed: Bool) -> Void in
               MetalHostingController.shared.lockPointer()
               MetalViewController.shared.lockPointer()
               if pressed {
                  winios_pointer(0, 0, 0x0002, 0)
                  self.MouseClicking = true
               }
               else {
                  winios_pointer(0, 0, 0x0004, 0)
                  self.MouseClicking = false
               }
            }
            mouseInput.rightButton?.valueChangedHandler = {
                (_ button: GCControllerButtonInput, _ value: Float, _ pressed: Bool) -> Void in
               MetalHostingController.shared.lockPointer()
               MetalViewController.shared.lockPointer()
               if pressed {
                  winios_pointer(0, 0, 0x0008, 0)
                  self.MouseClicking = true
               }
               else {
                  winios_pointer(0, 0, 0x0010, 0)
                  self.MouseClicking = false
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
       return self.MouseMoving || self.MouseClicking
       // return self.MouseClicking
    }
}

// Hardware keyboard state, separate from the XInput controller bridge.
struct MadeiraKeys {
    static func virtualKey(hid: Int) -> Int32? {
        if (4...29).contains(hid) { return Int32(0x41 + hid - 4) }
        if (30...38).contains(hid) { return Int32(0x31 + hid - 30) }
        if (89...97).contains(hid) { return Int32(0x61 + hid - 89) }
        if (104...115).contains(hid) { return Int32(0x7c + hid - 104) }
        if (58...69).contains(hid) { return Int32(0x70 + hid - 58) }
        let keys: [Int: Int32] = [39:0x30,40:0x0d,41:0x1b,42:0x08,43:0x09,44:0x20,
            45:0xbd,46:0xbb,47:0xdb,48:0xdd,49:0xdc,51:0xba,52:0xde,53:0xc0,
            54:0xbc,55:0xbe,56:0xbf,57:0x14,73:0x2d,74:0x24,75:0x21,76:0x2e,
            77:0x23,78:0x22,79:0x27,80:0x25,81:0x28,82:0x26,
            70:0x2c,71:0x91,72:0x13,83:0x90,84:0x6f,85:0x6a,86:0x6d,
            87:0x6b,88:0x0d,98:0x60,99:0x6e,100:0xe2,101:0x5d,
            224:0xa2,225:0xa0,226:0xa4,227:0x5b,228:0xa3,229:0xa1,230:0xa5,231:0x5c]
        return keys[hid]
    }

    static func virtualKey(character: Character) -> (key: Int32, shift: Bool)? {
        guard let ascii = character.asciiValue else { return nil }
        if (65...90).contains(ascii) { return (Int32(ascii), true) }
        if (97...122).contains(ascii) { return (Int32(ascii - 32), false) }
        if (48...57).contains(ascii) { return (Int32(ascii), false) }
        if ascii == 10 || ascii == 13 { return (0x0d, false) }
        if ascii == 9 { return (0x09, false) }
        if ascii == 32 { return (0x20, false) }
        let symbols: [Character: (Int32, Bool)] = [
            "!": (0x31, true), "@": (0x32, true), "#": (0x33, true), "$": (0x34, true),
            "%": (0x35, true), "^": (0x36, true), "&": (0x37, true), "*": (0x38, true),
            "(": (0x39, true), ")": (0x30, true), "-": (0xbd, false), "_": (0xbd, true),
            "=": (0xbb, false), "+": (0xbb, true), "[": (0xdb, false), "{": (0xdb, true),
            "]": (0xdd, false), "}": (0xdd, true), "\\": (0xdc, false), "|": (0xdc, true),
            ";": (0xba, false), ":": (0xba, true), "'": (0xde, false), "\"": (0xde, true),
            ",": (0xbc, false), "<": (0xbc, true), ".": (0xbe, false), ">": (0xbe, true),
            "/": (0xbf, false), "?": (0xbf, true), "`": (0xc0, false), "~": (0xc0, true)
        ]
        return symbols[character]
    }

    private var sources: [String: Set<Int32>] = [:]
    mutating func update(name: String, value: Double) -> [(Int32, Bool)] {
        let before = Set(sources.values.flatMap { $0 })
        let key = name.lowercased()
        var held = Set<Int32>()
        if value > 0 {
            let bindings: [String: Int32] = [
                "arrowup": 0x26, "arrowdown": 0x28, "arrowleft": 0x25, "arrowright": 0x27,
                "up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
                "space": 0x20, "enter": 0x0d, "return": 0x0d, "escape": 0x1b]
            if let vk = bindings[key] { held.insert(vk) }
            else if key.count == 1, let character = key.first,
                    let mapping = Self.virtualKey(character: character), !mapping.shift {
                held.insert(mapping.key)
            }
        }
        sources[key] = held.isEmpty ? nil : held
        let after = Set(sources.values.flatMap { $0 })
        return before.subtracting(after).sorted().map { ($0, false) }
            + after.subtracting(before).sorted().map { ($0, true) }
    }
    mutating func releaseAll() -> [Int32] {
        let keys = Set(sources.values.flatMap { $0 }).sorted()
        sources.removeAll()
        return keys
    }
}
