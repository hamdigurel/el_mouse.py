# Gesture Mouse — Control Your Mouse with Hand Gestures

Control your computer's mouse with your hand through a webcam. Uses **MediaPipe Hands** to track 21 hand landmarks in real time and maps gestures to mouse actions.

## Gestures

| Gesture | Action |
|---|---|
| Move your index finger | Moves the cursor |
| Thumbs up | Left click |
| Fist | Copy (Ctrl + C) |

A short cooldown prevents the same action from firing several times in a row.

## Installation

```bash
pip install opencv-python mediapipe pyautogui
```

## Usage

```bash
python el_mouse.py
```

Keep one hand in front of the webcam. The image is mirrored so movements feel natural. Press **ESC** to exit.

## Tech stack

Python · MediaPipe · OpenCV · PyAutoGUI
