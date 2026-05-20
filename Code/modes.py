MODES = [
  {
    "name": "Windows",
    "icon": "WIN",
    "enc_label": "BRIGH",
    "enc_cw": {
      "action_type": "media",
      "action_value": "BRIGHTNESS_INCREMENT"
    },
    "enc_ccw": {
      "action_type": "media",
      "action_value": "BRIGHTNESS_DECREMENT"
    },
    "keys": [
      {
        "short_label": "DSK",
        "label": "Desktop Show",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "D"
        ]
      },
      {
        "short_label": "LOCK",
        "label": "Lock PC",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "L"
        ]
      },
      {
        "short_label": "SNAP",
        "label": "Screenshot Tool",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "SHIFT",
          "S"
        ]
      },
      {
        "short_label": "EMOJ",
        "label": "Emoji Panel",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "PERIOD"
        ]
      },
      {
        "short_label": "CLIP",
        "label": "Clipboard History",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "V"
        ]
      },
      {
        "short_label": "LEFT",
        "label": "Snap Window Left",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "LEFT_ARROW"
        ]
      },
      {
        "short_label": "TASK",
        "label": "Task View",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "TAB"
        ]
      },
      {
        "short_label": "RUN",
        "label": "Run Dialog",
        "action_type": "shortcut",
        "action_value": [
          "GUI",
          "R"
        ]
      },
      {
        "short_label": "MUTE",
        "label": "System Mute",
        "action_type": "media",
        "action_value": [
          "MUTE"
        ]
      }
    ]
  },
  {
    "name": "VS Code",
    "icon": "CODE",
    "enc_label": "INDNT",
    "enc_cw": {
      "action_type": "shortcut",
      "action_value": "RIGHT_BRACKET"
    },
    "enc_ccw": {
      "action_type": "shortcut",
      "action_value": "LEFT_BRACKET"
    },
    "keys": [
      {
        "short_label": "CMD",
        "label": "Command Palette",
        "action_type": "shortcut",
        "action_value": [
          "CONTROL",
          "SHIFT",
          "P"
        ]
      },
      {
        "short_label": "FILE",
        "label": "Quick File Search",
        "action_type": "shortcut",
        "action_value": [
          "CONTROL",
          "P"
        ]
      },
      {
        "short_label": "TERM",
        "label": "Toggle Terminal",
        "action_type": "shortcut",
        "action_value": [
          "CONTROL",
          "GRAVE"
        ]
      },
      {
        "short_label": "CMNT",
        "label": "Comment Line",
        "action_type": "shortcut",
        "action_value": [
          "CONTROL",
          "SLASH"
        ]
      },
      {
        "short_label": "RENM",
        "label": "Rename Symbol",
        "action_type": "shortcut",
        "action_value": [
          "F2"
        ]
      },
      {
        "short_label": "FMT",
        "label": "Format Document",
        "action_type": "shortcut",
        "action_value": [
          "SHIFT",
          "ALT",
          "F"
        ]
      },
      {
        "short_label": "MLTI",
        "label": "Multi Cursor",
        "action_type": "shortcut",
        "action_value": [
          "CONTROL",
          "ALT",
          "DOWN_ARROW"
        ]
      },
      {
        "short_label": "DEF",
        "label": "Go to Definition",
        "action_type": "shortcut",
        "action_value": [
          "F12"
        ]
      },
      {
        "short_label": "RUN",
        "label": "Run/Debug",
        "action_type": "shortcut",
        "action_value": [
          "F5"
        ]
      }
    ]
  },
  {
    "name": "Media",
    "icon": "MED",
    "enc_label": "VOL",
    "enc_cw": {
      "action_type": "media",
      "action_value": "VOLUME_INCREMENT"
    },
    "enc_ccw": {
      "action_type": "media",
      "action_value": "VOLUME_DECREMENT"
    },
    "keys": [
      {
        "short_label": "PREV",
        "label": "Previous Track",
        "action_type": "media",
        "action_value": [
          "SCAN_PREVIOUS_TRACK"
        ]
      },
      {
        "short_label": "PLAY",
        "label": "Play / Pause",
        "action_type": "media",
        "action_value": [
          "PLAY_PAUSE"
        ]
      },
      {
        "short_label": "NEXT",
        "label": "Next Track",
        "action_type": "media",
        "action_value": [
          "SCAN_NEXT_TRACK"
        ]
      },
      {
        "short_label": "MIC",
        "label": "Microphone Mute",
        "action_type": "none",
        "action_value": []
      },
      {
        "short_label": "MUTE",
        "label": "System Mute",
        "action_type": "media",
        "action_value": [
          "MUTE"
        ]
      },
      {
        "short_label": "CAM",
        "label": "Camera Toggle",
        "action_type": "none",
        "action_value": []
      },
      {
        "short_label": "MIX",
        "label": "Volume Mixer",
        "action_type": "none",
        "action_value": []
      },
      {
        "short_label": "MUSC",
        "label": "Open Music App",
        "action_type": "none",
        "action_value": []
      },
      {
        "short_label": "OVR",
        "label": "Media Overlay",
        "action_type": "none",
        "action_value": []
      }
    ]
  }
]
