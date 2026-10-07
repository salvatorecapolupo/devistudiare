"""
DEVI STUDIARE
Screensaver fullscreen stile spazio / 2001.

Audio:
- soundtrack.ogg
- soundtrack.wav
- soundtrack.mp3
- soundtrack.mid / soundtrack.midi su Windows

Esci con:
- ESC
- qualsiasi tasto
- click
- movimento del mouse
"""

import os
import sys
import math
import random
import ctypes
import pygame


# ============================================================
# CONFIG
# ============================================================

TEXT = "DEVI STUDIARE"

NUM_STARS = 900
FPS = 60

BASE_SPEED = 0.10
WARP_MAX = 5.8

T_FADEIN = 2.0

T_WARP_UP_A = 2.0
T_WARP_UP_B = 10.0

T_WARP_DN_A = 18.0
T_WARP_DN_B = 28.0

T_TEXT = 16.0
T_TEXT_FADE = 2.0

BG = (1, 2, 8)

STAR_COLORS = (
    (255, 255, 255),
    (205, 225, 255),
    (230, 235, 255),
    (255, 242, 220),
)


# ============================================================
# AUDIO - PRE-INIT
# ============================================================

# IMPORTANTE:
# Configuriamo il mixer PRIMA di pygame.init().
pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=1024
)

pygame.init()
pygame.font.init()


# ============================================================
# PATH
# ============================================================

def runtime_dir():
    return os.path.dirname(
        os.path.abspath(__file__)
    )


def exe_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(
            os.path.abspath(sys.executable)
        )

    return runtime_dir()


def get_resource_path(filename):
    """
    Cerca il file:
    1. directory temporanea PyInstaller (--onefile)
    2. directory EXE
    3. directory script
    """

    paths = []

    # PyInstaller --onefile
    if hasattr(sys, "_MEIPASS"):
        paths.append(
            os.path.join(
                sys._MEIPASS,
                filename
            )
        )

    # Accanto all'EXE
    paths.append(
        os.path.join(
            exe_dir(),
            filename
        )
    )

    # Accanto allo script
    paths.append(
        os.path.join(
            runtime_dir(),
            filename
        )
    )

    checked = set()

    for path in paths:

        path = os.path.abspath(path)

        if path in checked:
            continue

        checked.add(path)

        if os.path.isfile(path):
            return path

    return None


def find_audio():

    # OGG per primo
    for name in (
        "soundtrack.ogg",
        "soundtrack.wav",
        "soundtrack.mp3",
        "soundtrack.mid",
        "soundtrack.midi",
    ):

        path = get_resource_path(name)

        if path:
            return path

    return None


# ============================================================
# AUDIO
# ============================================================

class AudioPlayer:

    def __init__(self):

        self.mode = None
        self.mci = None
        self.alias = "devistudiare_bgm"

    def start(self, path):

        if not path:
            return False

        ext = os.path.splitext(
            path
        )[1].lower()

        # MIDI su Windows -> MCI
        if (
            ext in (".mid", ".midi")
            and
            os.name == "nt"
        ):
            return self.start_midi(path)

        # OGG/WAV/MP3 -> pygame
        return self.start_pygame(path)

    # --------------------------------------------------------

    def start_pygame(self, path):

        try:

            # Se il mixer è già attivo, non lo reinizializziamo.
            if not pygame.mixer.get_init():

                pygame.mixer.init(
                    frequency=44100,
                    size=-16,
                    channels=2,
                    buffer=1024
                )

            pygame.mixer.music.load(
                path
            )

            pygame.mixer.music.set_volume(
                0.70
            )

            pygame.mixer.music.play(
                loops=-1
            )

            self.mode = "pygame"

            return True

        except Exception as e:

            print(
                "[AUDIO] Errore:",
                e
            )

            self.mode = None

            return False

    # --------------------------------------------------------

    def start_midi(self, path):

        try:

            self.mci = ctypes.WinDLL(
                "winmm"
            )

            send = self.mci.mciSendStringW

            send.argtypes = [
                ctypes.c_wchar_p,
                ctypes.c_wchar_p,
                ctypes.c_uint,
                ctypes.c_void_p,
            ]

            send.restype = ctypes.c_uint

            error = send(
                f'open "{path}" type sequencer alias {self.alias}',
                None,
                0,
                None
            )

            if error != 0:

                self.mci = None

                return False

            error = send(
                f"play {self.alias} repeat",
                None,
                0,
                None
            )

            if error != 0:

                send(
                    f"close {self.alias}",
                    None,
                    0,
                    None
                )

                self.mci = None

                return False

            self.mode = "mci"

            return True

        except Exception as e:

            print(
                "[MIDI] Errore:",
                e
            )

            self.mode = None
            self.mci = None

            return False

    # --------------------------------------------------------

    def stop(self):

        if self.mode == "pygame":

            try:

                pygame.mixer.music.fadeout(
                    500
                )

                pygame.time.wait(
                    550
                )

            except Exception:
                pass

            try:

                if pygame.mixer.get_init():
                    pygame.mixer.quit()

            except Exception:
                pass

        elif (
            self.mode == "mci"
            and
            self.mci
        ):

            try:

                self.mci.mciSendStringW(
                    f"stop {self.alias}",
                    None,
                    0,
                    None
                )

                self.mci.mciSendStringW(
                    f"close {self.alias}",
                    None,
                    0,
                    None
                )

            except Exception:
                pass

        self.mode = None
        self.mci = None


# ============================================================
# MATH
# ============================================================

def smoothstep(a, b, x):

    if b == a:
        return 1.0

    t = max(
        0.0,
        min(
            1.0,
            (x - a) / (b - a)
        )
    )

    return (
        t * t
        * (3.0 - 2.0 * t)
    )


def warp_speed(t):

    up = smoothstep(
        T_WARP_UP_A,
        T_WARP_UP_B,
        t
    )

    down = smoothstep(
        T_WARP_DN_A,
        T_WARP_DN_B,
        t
    )

    return (
        BASE_SPEED
        +
        (WARP_MAX - BASE_SPEED)
        * (up - down)
    )


# ============================================================
# FONT
# ============================================================

def find_font(size):

    names = (
        "segoeuil",
        "segoe ui light",
        "century gothic",
        "bahnschrift light",
        "arial",
        "dejavu sans",
        "liberation sans",
    )

    for name in names:

        try:

            path = pygame.font.match_font(
                name
            )

            if path:

                return pygame.font.Font(
                    path,
                    size
                )

        except Exception:
            pass

    return pygame.font.Font(
        None,
        size
    )


# ============================================================
# CENTER LIGHT
# ============================================================

def make_center_glow(w, h):

    surface = pygame.Surface(
        (w, h),
        pygame.SRCALPHA
    )

    cx = w * 0.5
    cy = h * 0.5

    radius = min(w, h) * 0.34

    for i in range(28, 0, -1):

        r = radius * (
            i / 28.0
        )

        alpha = int(
            2
            +
            9
            *
            (
                1
                -
                i / 28.0
            )
        )

        pygame.draw.circle(
            surface,
            (
                40,
                90,
                180,
                alpha
            ),
            (
                int(cx),
                int(cy)
            ),
            max(
                1,
                int(r)
            )
        )

    return surface


# ============================================================
# STARS
# ============================================================

class Star:

    __slots__ = (
        "x",
        "y",
        "z",
        "prev_z",
        "size_factor",
        "phase",
        "twinkle",
        "color",
    )

    def __init__(self):

        self.color = random.choice(
            STAR_COLORS
        )

        self.size_factor = random.uniform(
            0.65,
            1.45
        )

        self.phase = random.uniform(
            0,
            math.tau
        )

        self.twinkle = random.uniform(
            0.25,
            1.0
        )

        self.reset(
            far=True
        )

    def reset(self, far=False):

        self.x = random.uniform(
            -1.0,
            1.0
        )

        self.y = random.uniform(
            -1.0,
            1.0
        )

        self.z = (
            1.0
            if far
            else random.uniform(
                0.02,
                1.0
            )
        )

        self.prev_z = self.z

    def update(self, dz):

        self.prev_z = self.z

        self.z -= dz

        if self.z <= 0.018:

            self.reset(
                far=True
            )

    def draw(
        self,
        surface,
        speed,
        time_now,
        w,
        h
    ):

        cx = w * 0.5
        cy = h * 0.5

        k_now = (
            (w * 0.52)
            /
            max(
                self.z,
                0.001
            )
        )

        xn = (
            self.x * k_now
            + cx
        )

        yn = (
            self.y * k_now
            + cy
        )

        k_prev = (
            (w * 0.52)
            /
            max(
                self.prev_z,
                0.001
            )
        )

        xp = (
            self.x * k_prev
            + cx
        )

        yp = (
            self.y * k_prev
            + cy
        )

        visible_now = (
            0 <= xn < w
            and
            0 <= yn < h
        )

        visible_prev = (
            0 <= xp < w
            and
            0 <= yp < h
        )

        if not visible_now and not visible_prev:
            return

        depth = 1.0 - self.z

        brightness = (
            0.18
            +
            0.82
            * depth ** 0.65
        )

        twinkle = (
            1.0
            +
            math.sin(
                time_now
                *
                (
                    1.5
                    +
                    self.twinkle
                    * 2.2
                )
                +
                self.phase
            )
            * 0.08
        )

        brightness *= twinkle

        r, g, b = self.color

        color = (
            min(
                255,
                int(r * brightness)
            ),
            min(
                255,
                int(g * brightness)
            ),
            min(
                255,
                int(b * brightness)
            ),
        )

        # ----------------------------------------------------
        # SCIA
        # ----------------------------------------------------

        if speed > 0.85:

            trail = math.hypot(
                xn - xp,
                yn - yp
            )

            if trail > 2.0:

                width = max(
                    1,
                    int(
                        0.7
                        +
                        depth
                        * 2.0
                        * self.size_factor
                    )
                )

                pygame.draw.line(
                    surface,
                    color,
                    (
                        int(xp),
                        int(yp)
                    ),
                    (
                        int(xn),
                        int(yn)
                    ),
                    width
                )

                return

        # ----------------------------------------------------
        # PUNTO
        # ----------------------------------------------------

        radius = max(
            1,
            int(
                0.55
                +
                depth
                * 2.4
                * self.size_factor
            )
        )

        pygame.draw.circle(
            surface,
            color,
            (
                int(xn),
                int(yn)
            ),
            radius
        )


# ============================================================
# SHARP TEXT
# ============================================================

class SharpText:

    def __init__(
        self,
        text,
        font,
        y,
        screen_width
    ):

        self.text_surface = font.render(
            text,
            True,
            (
                245,
                248,
                255
            )
        )

        self.shadow = font.render(
            text,
            True,
            (
                0,
                0,
                0
            )
        )

        # CORRETTO:
        # prima usava una variabile globale W inesistente.
        self.x = (
            screen_width
            -
            self.text_surface.get_width()
        ) // 2

        self.y = y

    def draw(
        self,
        surface,
        alpha
    ):

        if alpha <= 0:
            return

        alpha = max(
            0,
            min(
                255,
                int(alpha)
            )
        )

        # Ombra 1 px
        shadow = self.shadow.copy()

        shadow.set_alpha(
            min(
                130,
                alpha
            )
        )

        surface.blit(
            shadow,
            (
                self.x + 1,
                self.y + 1
            )
        )

        # TESTO PERFETTAMENTE NITIDO
        text = self.text_surface.copy()

        text.set_alpha(
            alpha
        )

        surface.blit(
            text,
            (
                self.x,
                self.y
            )
        )


# ============================================================
# MAIN
# ============================================================

def main():

    info = pygame.display.Info()

    W = info.current_w
    H = info.current_h

    screen = pygame.display.set_mode(
        (W, H),
        pygame.FULLSCREEN
        |
        pygame.SCALED
    )

    pygame.display.set_caption(
        "Screensaver"
    )

    pygame.mouse.set_visible(
        False
    )

    clock = pygame.time.Clock()

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    center_glow = make_center_glow(
        W,
        H
    )

    # --------------------------------------------------------
    # FONT
    # --------------------------------------------------------

    font_size = int(
        H * 0.115
    )

    font = find_font(
        font_size
    )

    max_width = int(
        W * 0.82
    )

    # CORRETTO: font.size(TEXT)[0]
    while (
        font.size(TEXT)[0]
        >
        max_width
        and
        font_size > 20
    ):

        font_size -= 2

        font = find_font(
            font_size
        )

    text_y = int(
        H * 0.5
        -
        font.get_height()
        * 0.5
    )

    text = SharpText(
        TEXT,
        font,
        text_y,
        W
    )

    # --------------------------------------------------------
    # STARS
    # --------------------------------------------------------

    stars = [
        Star()
        for _ in range(
            NUM_STARS
        )
    ]

    # --------------------------------------------------------
    # AUDIO
    # --------------------------------------------------------

    audio = AudioPlayer()

    audio_path = find_audio()

    if audio_path:
        print(
            "[AUDIO]",
            audio_path
        )

        audio.start(
            audio_path
        )

    else:
        print(
            "[AUDIO] soundtrack non trovato"
        )

    # --------------------------------------------------------
    # LOOP
    # --------------------------------------------------------

    start = pygame.time.get_ticks()

    running = True
    mouse_armed = False

    # Svuota eventuali movimenti iniziali
    pygame.mouse.get_rel()

    while running:

        dt = (
            clock.tick(FPS)
            /
            1000.0
        )

        now = (
            pygame.time.get_ticks()
            -
            start
        ) / 1000.0

        if now > 1.0:
            mouse_armed = True

        # ----------------------------------------------------
        # EVENTI
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif event.type == pygame.KEYDOWN:

                running = False

            elif (
                event.type
                ==
                pygame.MOUSEBUTTONDOWN
            ):

                running = False

            elif (
                event.type
                ==
                pygame.MOUSEMOTION
                and
                mouse_armed
            ):

                if (
                    abs(event.rel[0]) > 4
                    or
                    abs(event.rel[1]) > 4
                ):

                    running = False

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        speed = warp_speed(
            now
        )

        dz = speed * dt

        for star in stars:

            star.update(
                dz
            )

        # ----------------------------------------------------
        # DRAW
        # ----------------------------------------------------

        screen.fill(
            BG
        )

        screen.blit(
            center_glow,
            (0, 0)
        )

        for star in stars:

            star.draw(
                screen,
                speed,
                now,
                W,
                H
            )

        # ----------------------------------------------------
        # TESTO
        # ----------------------------------------------------

        if now >= T_TEXT:

            text_alpha = min(
                255,
                int(
                    255
                    *
                    smoothstep(
                        T_TEXT,
                        T_TEXT
                        +
                        T_TEXT_FADE,
                        now
                    )
                )
            )

            text.draw(
                screen,
                text_alpha
            )

        # ----------------------------------------------------
        # FADE-IN
        # ----------------------------------------------------

        if now < T_FADEIN:

            alpha = int(
                255
                *
                (
                    1.0
                    -
                    now
                    /
                    T_FADEIN
                )
            )

            black = pygame.Surface(
                (W, H),
                pygame.SRCALPHA
            )

            black.fill(
                (
                    0,
                    0,
                    0,
                    alpha
                )
            )

            screen.blit(
                black,
                (0, 0)
            )

        pygame.display.flip()

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    audio.stop()

    pygame.quit()

    sys.exit()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
