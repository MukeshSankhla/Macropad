import storage
import usb_hid

# Remount FIRST before anything else
# storage.remount("/", readonly=False)

# Then enable HID
usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.CONSUMER_CONTROL)
)