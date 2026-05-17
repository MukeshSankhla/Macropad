import usb_hid
import board, busio, digitalio, rotaryio, keypad, time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import displayio, terminalio, i2cdisplaybus
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect

# ── Release displays ───────────────────────────────────
displayio.release_displays()

# ── OLED I²C ──────────────────────────────────────────
i2c   = busio.I2C(board.GP5, board.GP4)
dbus  = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(dbus, width=128, height=64)
mouse = Mouse(usb_hid.devices)

W, H  = 128, 64
WHITE = 0xFFFFFF
BLACK = 0x000000
FONT  = terminalio.FONT

# ── HID ───────────────────────────────────────────────
kbd = Keyboard(usb_hid.devices)
cc  = ConsumerControl(usb_hid.devices)
KC  = Keycode

# ── Encoder ───────────────────────────────────────────
enc         = rotaryio.IncrementalEncoder(board.GP0, board.GP1)
enc_btn     = digitalio.DigitalInOut(board.GP8)
enc_btn.switch_to_input(pull=digitalio.Pull.UP)

# ── Keypad 3×3 ────────────────────────────────────────
keys = keypad.KeyMatrix(
    row_pins   =(board.GP19, board.GP26, board.GP27),
    column_pins=(board.GP9,  board.GP16, board.GP18),
    columns_to_anodes=False,
)

# ─────────────────────────────────────────────────────
# HID HELPERS
# ─────────────────────────────────────────────────────
def tap(*codes):
    kbd.press(*codes)
    kbd.release_all()

def cc_tap(code):
    cc.send(code)

# ─────────────────────────────────────────────────────
# MODES  (name, icon 4ch, enc_label, enc_cw, enc_ccw, keys[9])
# ─────────────────────────────────────────────────────
MODES = [
    # 0 ── Windows
    {
        "name":      "Windows",
        "icon":      "WIN",
        "enc_label": "VOLUME",
        "enc_cw":  lambda: cc_tap(ConsumerControlCode.VOLUME_INCREMENT),
        "enc_ccw": lambda: cc_tap(ConsumerControlCode.VOLUME_DECREMENT),
        "keys": [
            ("DSK", "Desktop",  lambda: tap(KC.GUI, KC.D)),
            ("LCK", "Lock PC",  lambda: tap(KC.GUI, KC.L)),
            ("SNP", "Snip",     lambda: tap(KC.GUI, KC.SHIFT, KC.S)),
            ("AF4", "Close",    lambda: tap(KC.ALT, KC.F4)),
            ("UND", "Undo",     lambda: tap(KC.CONTROL, KC.Z)),
            ("RDO", "Redo",     lambda: tap(KC.CONTROL, KC.Y)),
            ("TSK", "Task Mgr", lambda: tap(KC.CONTROL, KC.SHIFT, KC.ESCAPE)),
            ("RUN", "Run",      lambda: tap(KC.GUI, KC.R)),
            ("SET", "Settings", lambda: tap(KC.GUI, KC.I)),
        ],
    },
    # 1 ── VS Code
    {
        "name":      "VS Code",
        "icon":      "VSC",
        "enc_label": "INDENT",
        "enc_cw":  lambda: tap(KC.CONTROL, KC.RIGHT_BRACKET),
        "enc_ccw": lambda: tap(KC.CONTROL, KC.LEFT_BRACKET),
        "keys": [
            ("TRM", "Terminal", lambda: tap(KC.CONTROL, KC.GRAVE)),
            ("PAL", "Palette",  lambda: tap(KC.CONTROL, KC.SHIFT, KC.P)),
            ("CMT", "Comment",  lambda: tap(KC.CONTROL, KC.SLASH)),
            ("FMT", "Format",   lambda: tap(KC.ALT, KC.SHIFT, KC.F)),
            ("UND", "Undo",     lambda: tap(KC.CONTROL, KC.Z)),
            ("RDO", "Redo",     lambda: tap(KC.CONTROL, KC.Y)),
            ("SPL", "Split",    lambda: tap(KC.CONTROL, KC.BACKSLASH)),
            ("ZEN", "Zen",      lambda: tap(KC.CONTROL, KC.K, KC.Z)),
            ("EXP", "Explorer", lambda: tap(KC.CONTROL, KC.SHIFT, KC.E)),
        ],
    },

    # 2 ── Fusion 360
    {
        "name":      "Fusion360",
        "icon":      "F360",
        "enc_label": "ZOOM",
        "enc_cw":  lambda: mouse.move(wheel=3),   # scroll up  = zoom in
        "enc_ccw": lambda: mouse.move(wheel=-3),  # scroll down = zoom out
        "keys": [
            ("SKT", "Sketch",  lambda: tap(KC.S)),
            ("EXT", "Extrude", lambda: tap(KC.E)),
            ("FIL", "Fillet",  lambda: tap(KC.F)),
            ("UND", "Undo",    lambda: tap(KC.CONTROL, KC.Z)),
            ("RDO", "Redo",    lambda: tap(KC.CONTROL, KC.Y)),
            ("MSR", "Measure", lambda: tap(KC.I)),
            ("FIT", "Fit View",lambda: tap(KC.F6)),
            ("SEC", "Section", lambda: tap(KC.ALT, KC.SHIFT, KC.S)),
            ("RND", "Render",  lambda: tap(KC.CONTROL, KC.SHIFT, KC.R)),
        ],
    },
    # 3 ── DaVinci Resolve
    {
        "name":      "DaVinci",
        "icon":      "DAV",
        "enc_label": "SCRUB",
        "enc_cw":  lambda: tap(KC.RIGHT_ARROW),
        "enc_ccw": lambda: tap(KC.LEFT_ARROW),
        "keys": [
            ("PLY", "Play",    lambda: tap(KC.SPACE)),
            ("RZR", "Razor",   lambda: tap(KC.B)),
            ("MKI", "Mark In", lambda: tap(KC.I)),
            ("MKO", "Mark Out",lambda: tap(KC.O)),
            ("UND", "Undo",    lambda: tap(KC.CONTROL, KC.Z)),
            ("RDO", "Redo",    lambda: tap(KC.CONTROL, KC.SHIFT, KC.Z)),
            ("FUL", "FullScr", lambda: tap(KC.P)),
            ("EXP", "Export",  lambda: tap(KC.CONTROL, KC.E)),
            ("CLR", "Color",   lambda: tap(KC.SHIFT, KC.SIX)),
        ],
    },
    # 4 ── Media  (double-click encoder btn to toggle)
    {
        "name":      "Media",
        "icon":      "MED",
        "enc_label": "VOLUME",
        "enc_cw":  lambda: cc_tap(ConsumerControlCode.VOLUME_INCREMENT),
        "enc_ccw": lambda: cc_tap(ConsumerControlCode.VOLUME_DECREMENT),
        "keys": [
            ("PRV", "Prev",    lambda: cc_tap(ConsumerControlCode.SCAN_PREVIOUS_TRACK)),
            ("PLY", "Play",    lambda: cc_tap(ConsumerControlCode.PLAY_PAUSE)),
            ("NXT", "Next",    lambda: cc_tap(ConsumerControlCode.SCAN_NEXT_TRACK)),
            ("MUT", "Mute",    lambda: cc_tap(ConsumerControlCode.MUTE)),
            ("VD-", "Vol Dn",  lambda: cc_tap(ConsumerControlCode.VOLUME_DECREMENT)),
            ("VD+", "Vol Up",  lambda: cc_tap(ConsumerControlCode.VOLUME_INCREMENT)),
            ("BRD", "Brght-",  lambda: cc_tap(ConsumerControlCode.BRIGHTNESS_DECREMENT)),
            ("BRU", "Brght+",  lambda: cc_tap(ConsumerControlCode.BRIGHTNESS_INCREMENT)),
            ("STP", "Stop",    lambda: cc_tap(ConsumerControlCode.STOP)),
        ],
    },
]

NUM_MODES = len(MODES)
MEDIA_IDX = 4   # index of Media mode

# ─────────────────────────────────────────────────────
# LOW-LEVEL BITMAP DRAW HELPERS
# (pure displayio — no external shape library needed)
# ─────────────────────────────────────────────────────
def make_bitmap(w, h, color, bg=BLACK):
    bmp = displayio.Bitmap(w, h, 2)
    pal = displayio.Palette(2)
    pal[0] = bg
    pal[1] = color
    for i in range(w * h):
        bmp[i] = 1
    return bmp, pal

def filled_rect(g, x, y, w, h, color=WHITE):
    bmp, pal = make_bitmap(w, h, color)
    g.append(displayio.TileGrid(bmp, pixel_shader=pal, x=x, y=y))

def h_line(g, x, y, length, color=WHITE):
    filled_rect(g, x, y, length, 1, color)

def v_line(g, x, y, length, color=WHITE):
    filled_rect(g, x, y, 1, length, color)

def border_rect(g, x, y, w, h, color=WHITE):
    h_line(g, x,       y,       w, color)
    h_line(g, x,       y+h-1,   w, color)
    v_line(g, x,       y,       h, color)
    v_line(g, x+w-1,   y,       h, color)

def lbl(g, txt, x, y, color=WHITE, scale=1):
    l = label.Label(FONT, text=str(txt), color=color, scale=scale)
    l.x = x; l.y = y
    g.append(l)
    return l

def centered_lbl(g, txt, y, color=WHITE, scale=1):
    x = max(0, (W - len(str(txt)) * 6 * scale) // 2)
    return lbl(g, txt, x, y, color, scale)

# ─────────────────────────────────────────────────────
# DRAW: TITLE BAR  (inverted, full width)
# ─────────────────────────────────────────────────────
def title_bar(g, left_txt, right_txt=""):
    filled_rect(g, 0, 0, W, 11, WHITE)
    l = label.Label(FONT, text=left_txt, color=BLACK)
    l.x = 2; l.y = 5
    g.append(l)
    if right_txt:
        r = label.Label(FONT, text=right_txt, color=BLACK)
        r.x = W - len(right_txt) * 6 - 2
        r.y = 5
        g.append(r)

# ─────────────────────────────────────────────────────
# DRAW: 3×3 KEY GRID
# Each cell: 40×16px  grid starts at y=13
#  ┌───┬───┬───┐
#  │ 1 │ 2 │ 3 │  row0  y=13
#  ├───┼───┼───┤
#  │ 4 │ 5 │ 6 │  row1  y=29
#  ├───┼───┼───┤
#  │ 7 │ 8 │ 9 │  row2  y=45
#  └───┴───┴───┘
# ─────────────────────────────────────────────────────
CELL_W  = 42
CELL_H  = 16
GRID_X  = 0
GRID_Y  = 12
# Right strip (8px) shows encoder info
STRIP_X = 120

def draw_grid_lines(g):
    # Outer border
    border_rect(g, GRID_X, GRID_Y, STRIP_X, H - GRID_Y)
    # Internal vertical lines
    v_line(g, GRID_X + CELL_W,     GRID_Y, H - GRID_Y)
    v_line(g, GRID_X + CELL_W * 2, GRID_Y, H - GRID_Y)
    # Internal horizontal lines
    h_line(g, GRID_X, GRID_Y + CELL_H,     STRIP_X)
    h_line(g, GRID_X, GRID_Y + CELL_H * 2, STRIP_X)
    # Right strip separator
    v_line(g, STRIP_X, GRID_Y, H - GRID_Y)

def cell_xy(idx):
    """Top-left pixel of key cell interior (1px inset from border)."""
    row = idx // 3
    col = idx % 3
    x = GRID_X + col * CELL_W + 1
    y = GRID_Y + row * CELL_H + 1
    return x, y

def draw_key_labels(g, mode_idx):
    for i, (short, _, _) in enumerate(MODES[mode_idx]["keys"]):
        cx, cy = cell_xy(i)
        # Key number (tiny, top-left of cell)
        num_lbl = label.Label(FONT, text=str(i+1), color=WHITE)
        num_lbl.x = cx + 2
        num_lbl.y = cy + 8
        g.append(num_lbl)
        # Short label (right of number)
        sl = label.Label(FONT, text=short, color=WHITE)
        sl.x = cx + 12
        sl.y = cy + 8
        g.append(sl)

# ─────────────────────────────────────────────────────
# DRAW: RIGHT ENCODER STRIP  (8px wide, rotated feel)
# Shows encoder function label vertically
# ─────────────────────────────────────────────────────
def draw_enc_strip(g, enc_label):
    # Strip background (inverted on active)
    filled_rect(g, STRIP_X + 1, GRID_Y, W - STRIP_X - 1, H - GRID_Y, WHITE)
    # Label chars stacked vertically
    chars = enc_label[:4]
    for i, ch in enumerate(chars):
        cl = label.Label(FONT, text=ch, color=BLACK)
        cl.x = STRIP_X + 2
        cl.y = GRID_Y + 6 + i * 10
        g.append(cl)

# ─────────────────────────────────────────────────────
# MAIN SCREEN
# ─────────────────────────────────────────────────────
def draw_main(mode_idx):
    g = displayio.Group()
    m = MODES[mode_idx]
    title_bar(g, m["name"], m["icon"])
    draw_grid_lines(g)
    draw_key_labels(g, mode_idx)
    draw_enc_strip(g, m["enc_label"])
    display.root_group = g

# ─────────────────────────────────────────────────────
# DRAW: MODE SELECT  — 4 visible items + scroll bar
# ─────────────────────────────────────────────────────
PAGE_SIZE = 4          # items visible at once
ROW_H     = 12         # px per row
MENU_Y    = 12         # y where list starts (below title bar)

def draw_mode_select(sel):
    g = displayio.Group()
    title_bar(g, "MODE SELECT", "ENC")

    # Which page window to show — keep selected item visible
    page_start = (sel // PAGE_SIZE) * PAGE_SIZE
    visible    = MODES[page_start : page_start + PAGE_SIZE]

    for i, m in enumerate(visible):
        mode_idx = page_start + i
        y        = MENU_Y + i * ROW_H

        if mode_idx == sel:
            # Highlighted row — white fill, black text
            filled_rect(g, 0, y, W - 8, ROW_H, WHITE)

            arrow = label.Label(FONT, text=">", color=BLACK)
            arrow.x = 2; arrow.y = y + 6
            g.append(arrow)

            nm = label.Label(FONT, text=m["name"], color=BLACK)
            nm.x = 12; nm.y = y + 6
            g.append(nm)

            ef = label.Label(FONT, text=m["enc_label"], color=BLACK)
            ef.x = W - 8 - len(m["enc_label"]) * 6 - 2
            ef.y = y + 6
            g.append(ef)
        else:
            nm = label.Label(FONT, text=m["name"], color=WHITE)
            nm.x = 12; nm.y = y + 6
            g.append(nm)

            ef = label.Label(FONT, text=m["enc_label"], color=WHITE)
            ef.x = W - 8 - len(m["enc_label"]) * 6 - 2
            ef.y = y + 6
            g.append(ef)

    # ── Scroll bar (right 6px strip) ─────────────────
    bar_area_h  = PAGE_SIZE * ROW_H          # total scrollable area height in px
    bar_h       = max(4, bar_area_h * PAGE_SIZE // NUM_MODES)
    bar_y       = MENU_Y + (sel * bar_area_h // NUM_MODES)

    # Track
    v_line(g, W - 4, MENU_Y, bar_area_h, WHITE)

    # Thumb
    filled_rect(g, W - 6, bar_y, 5, bar_h, WHITE)

    # Page indicator dots at bottom
    dot_y = MENU_Y + PAGE_SIZE * ROW_H + 3
    pages = (NUM_MODES + PAGE_SIZE - 1) // PAGE_SIZE
    cur_page = sel // PAGE_SIZE
    for p in range(pages):
        dot_x = (W // 2) - (pages * 6 // 2) + p * 6
        if p == cur_page:
            filled_rect(g, dot_x, dot_y, 4, 4, WHITE)   # filled = current page
        else:
            border_rect(g, dot_x, dot_y, 4, 4, WHITE)   # outline = other pages

    display.root_group = g

# ─────────────────────────────────────────────────────
# MEDIA MODE POPUP  (shown when entering/in media mode)
# ─────────────────────────────────────────────────────
def draw_media_popup():
    g = displayio.Group()
    title_bar(g, "** MEDIA **", "MED")
    draw_grid_lines(g)
    draw_key_labels(g, MEDIA_IDX)
    draw_enc_strip(g, "VOL")
    display.root_group = g

# ─────────────────────────────────────────────────────
# BOOT ANIMATION
# ─────────────────────────────────────────────────────
def boot_animation():
    # — Scene 1: big centered name ———————————————————
    g = displayio.Group()
    filled_rect(g, 0, 0, W, H, WHITE)

    # MACRO text
    mt = label.Label(FONT, text="MACROPAD", color=BLACK, scale=2)
    mt.x = 20; mt.y = 26
    g.append(mt)

    # Divider line under text
    h_line(g, 10, 38, W-20, BLACK)

    # Subtitle
    sl = label.Label(FONT, text="Makerbrains.com", color=BLACK)
    sl.x = (W - 15*6)//2; sl.y = 46
    g.append(sl)

    display.root_group = g
    time.sleep(2)

    # — Scene 2: slide out upward ————————————————————
    for offset in range(0, H + 1, 4):
        g2 = displayio.Group()
        if offset < H:
            # Draw existing screen shifted up (simulate by clipping top)
            filled_rect(g2, 0, 0, W, H - offset, WHITE)
            # Re-draw text shifted
            mt2 = label.Label(FONT, text="MACROPAD", color=BLACK, scale=2)
            mt2.x = 20; mt2.y = 26 - offset
            g2.append(mt2)
            
        display.root_group = g2
        time.sleep(0.01)

    # — Scene 3: mode icons slide in one by one ———————
    icons = [m["icon"] for m in MODES]
    for ic in icons:
        g3 = displayio.Group()
        # Black bg with white bordered box
        border_rect(g3, 34, 16, 60, 32)
        il = label.Label(FONT, text=ic, color=WHITE, scale=2)
        il.x = 34 + (60 - len(ic)*12)//2
        il.y = 32
        g3.append(il)
        display.root_group = g3
        time.sleep(0.15)

    time.sleep(0.1)

    # — Scene 4: ready pulse ——————————————————————————
    for _ in range(2):
        g4 = displayio.Group()
        filled_rect(g4, 0, 0, W, H, WHITE)
        rl = label.Label(FONT, text="READY", color=BLACK, scale=2)
        rl.x = (W - 5*12)//2; rl.y = H//2
        g4.append(rl)
        display.root_group = g4
        time.sleep(0.12)
        display.root_group = displayio.Group()
        time.sleep(0.10)

# ─────────────────────────────────────────────────────
# ENCODER BUTTON — double-click detection
# ─────────────────────────────────────────────────────
DOUBLE_CLICK_MS = 400   # window in milliseconds

btn_last        = True
btn_press_time  = 0
btn_click_count = 0
btn_pending     = False  # waiting to see if 2nd click comes

# ─────────────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────────────
current_mode = 0
mode_select  = False
select_idx   = 0
last_enc_pos = enc.position
prev_mode    = 0          # remember last non-media mode

# ─────────────────────────────────────────────────────
# RUN BOOT + SHOW FIRST SCREEN
# ─────────────────────────────────────────────────────
boot_animation()
draw_main(current_mode)

# ─────────────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────────────
while True:
    now = time.monotonic_ns() // 1_000_000   # ms

    # ── Encoder button edge detect ──────────────────
    btn_now = enc_btn.value   # True = not pressed
    falling = btn_last and not btn_now

    if falling:
        btn_click_count += 1
        btn_press_time   = now
        btn_pending      = True

    btn_last = btn_now

    # ── Resolve single vs double click ───────────────
    if btn_pending and (now - btn_press_time) > DOUBLE_CLICK_MS:
        btn_pending = False
        clicks = btn_click_count
        btn_click_count = 0

        if clicks >= 2:
            # ── DOUBLE CLICK → toggle Media mode ────
            if current_mode == MEDIA_IDX:
                current_mode = prev_mode
                mode_select  = False
                draw_main(current_mode)
            else:
                prev_mode    = current_mode
                current_mode = MEDIA_IDX
                mode_select  = False
                draw_media_popup()

        else:
            # ── SINGLE CLICK ────────────────────────
            if mode_select:
                current_mode = select_idx
                mode_select  = False
                draw_main(current_mode)
            else:
                mode_select = True
                select_idx  = current_mode
                draw_mode_select(select_idx)

    # ── Encoder rotation ─────────────────────────────
    pos = enc.position
    if pos != last_enc_pos:
        delta        = pos - last_enc_pos
        last_enc_pos = pos

        if mode_select:
            select_idx = (select_idx + (1 if delta > 0 else -1)) % NUM_MODES
            draw_mode_select(select_idx)
        else:
            m = MODES[current_mode]
            steps = abs(delta)
            fn    = m["enc_cw"] if delta > 0 else m["enc_ccw"]
            for _ in range(steps):
                fn()

    # ── Keypad ───────────────────────────────────────
    event = keys.events.get()
    if event and event.pressed:
        k = event.key_number
        if mode_select:
            if k < NUM_MODES:
                current_mode = k
                mode_select  = False
                draw_main(current_mode)
        else:
            _, _, action = MODES[current_mode]["keys"][k]
            action()

    time.sleep(0.004)
