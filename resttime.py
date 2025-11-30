#!/usr/bin/env python3
import sys
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
if sys.platform == "linux":
    from Xlib import display, X
    from Xlib.protocol import event

try:
    import mpv
    _loadedMPV=True
except ImportError as e:
    _loadedMPV=False
    print(f"No se pudo cargar la librería mpv: {e}")

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

from datetime import datetime

class RestTime:
    def __init__(self):
        self.timer_activo = False
        self.timer_contador = 0
        self.window_id = None

        self._root = Tk()
        self._root.state(['iconic'])

        self._root.title('RestTime v1.01')

        self.create_layout()
        self.configura_layout()

        self.ajusta_ventana()
        self._root.state(['normal'])

        if sys.platform == "linux":
            self.d = display.Display()
            root = self.d.screen().root

            # Método _NET_ACTIVE_WINDOW para obtener el id de la ventana.
            self.log("Probando _NET_ACTIVE_WINDOW...")
            try:
                atom = self.d.intern_atom('_NET_ACTIVE_WINDOW')
                prop = root.get_full_property(atom, X.AnyPropertyType)
                self.window_id = prop.value[0]
                if prop and prop.value:
                    self.log(f"Encontrado ID de Ventana: {hex(self.window_id)}")
            except Exception as err:
                self.log(err)
        elif sys.platform == "win32":
            self.hwnd = ctypes.windll.user32.GetParent(self._root.winfo_id())
            self.log(f"Encontrado hwnd:{hex(self.hwnd)}")

    def create_layout(self):
        self._mainframe = ttk.Frame(self._root, padding='5 5 5 5')
        self._mainframe.grid(row=0, column=0, sticky=(E, W, N, S))

        self._tiempo_frame = ttk.Frame(self._mainframe, padding='0 0 0 0')
        self._tiempo_frame.grid(row=0, column=0, sticky=(E, W, N, S))

        self._horas1_sv = StringVar()
        self._horas1_sv.set(0)
        self._horas1 = ttk.Entry(self._tiempo_frame, textvariable=self._horas1_sv, width=1, font=('Arial', 150))
        self._horas1.grid(row=0, column=1, sticky=(S, N))
        vcmdh1 = (self._root.register(self.validar_entrada_0a9), '%P')
        self._horas1.config(validate="key", validatecommand=vcmdh1)
        self._scale_horas1 = ttk.Scale(self._tiempo_frame, orient=VERTICAL, command=self._horas1_update, from_=9, to=0)
        self._scale_horas1.grid(row=0, column=2, sticky=(S, N))

        self._horas2_sv = StringVar()
        self._horas2_sv.set(0)
        self._horas2 = ttk.Entry(self._tiempo_frame, textvariable=self._horas2_sv, width=1, font=('Arial', 150))
        self._horas2.grid(row=0, column=3, sticky=(S, N))
        vcmdh2 = (self._root.register(self.validar_entrada_0a9), '%P')
        self._horas2.config(validate="key", validatecommand=vcmdh2)
        self._scale_horas2 = ttk.Scale(self._tiempo_frame, orient=VERTICAL, command=self._horas2_update, from_=9, to=0)
        self._scale_horas2.grid(row=0, column=4, sticky=(S, N))

        self._colon_horas = ttk.Label(self._tiempo_frame, width=0, font=('Arial', 150), text=":")
        self._colon_horas.grid(row=0, column=5, sticky=(S, N))

        self._minutos1_sv = StringVar()
        self._minutos1_sv.set(0)
        self._minutos1 = ttk.Entry(self._tiempo_frame, textvariable=self._minutos1_sv, width=1, font=('Arial', 150))
        self._minutos1.grid(row=0, column=6, sticky=(S, N))
        vcmdm1 = (self._root.register(self.validar_entrada_0a5), '%P')
        self._minutos1.config(validate="key", validatecommand=vcmdm1)
        self._scale_minutos1 = ttk.Scale(self._tiempo_frame, orient=VERTICAL, command=self._minutos1_update, from_=5, to=0)
        self._scale_minutos1.grid(row=0, column=7, sticky=(S, N))

        self._minutos2_sv = StringVar()
        self._minutos2_sv.set(0)
        self._minutos2 = ttk.Entry(self._tiempo_frame, textvariable=self._minutos2_sv, width=1, font=('Arial', 150))
        self._minutos2.grid(row=0, column=8, sticky=(S, N))
        vcmdm2 = (self._root.register(self.validar_entrada_0a9), '%P')
        self._minutos2.config(validate="key", validatecommand=vcmdm2)
        self._scale_minutos2 = ttk.Scale(self._tiempo_frame, orient=VERTICAL, command=self._minutos2_update, from_=9, to=0)
        self._scale_minutos2.grid(row=0, column=9, sticky=(S, N))

        self._colon_minutos = ttk.Label(self._tiempo_frame, width=0, font=('Arial', 150), text=":")
        self._colon_minutos.grid(row=0, column=10, sticky=(S, N))

        self._segundos1_sv = StringVar()
        self._segundos1_sv.set(0)
        self._segundos1 = ttk.Entry(self._tiempo_frame, textvariable=self._segundos1_sv, width=1, font=('Arial', 150))
        self._segundos1.grid(row=0, column=11, sticky=(S, N))
        vcmds1 = (self._root.register(self.validar_entrada_0a5), '%P')
        self._segundos1.config(validate="key", validatecommand=vcmds1)
        self._scale_segundos1 = ttk.Scale(self._tiempo_frame, orient=VERTICAL, command=self._segundos1_update, from_=5, to=0)
        self._scale_segundos1.grid(row=0, column=12, sticky=(S, N))

        self._segundos2_sv = StringVar()
        self._segundos2_sv.set(0)
        self._segundos2 = ttk.Entry(self._tiempo_frame, textvariable=self._segundos2_sv, width=1, font=('Arial', 150))
        self._segundos2.grid(row=0, column=13, sticky=(S, N))
        vcmds2 = (self._root.register(self.validar_entrada_0a9), '%P')
        self._segundos2.config(validate="key", validatecommand=vcmds2)
        self._scale_segundos2 = ttk.Scale(self._tiempo_frame, orient=VERTICAL, command=self._segundos2_update, from_=9, to=0)
        self._scale_segundos2.grid(row=0, column=14, sticky=(S, N))

        self._start_btn = ttk.Button(self._tiempo_frame, text="Start", underline=0, command=self._start_timer, padding="5 5 5 5")
        self._root.bind('<Alt-i>', lambda event: self._start_timer())
        self._start_btn.grid(row=1, column=13, sticky=(E, W), padx=10, pady=10)
        self._start_btn.rowconfigure(1, weight=1)

        self._stop_btn = ttk.Button(self._tiempo_frame, text="Stop", underline=0, command=self._stop_timer, padding="5 5 5 5")
        self._root.bind('<Alt-i>', lambda event: self._stop_timer())
        self._stop_btn.grid(row=1, column=11, sticky=(E, W), padx=10, pady=10)
        self._stop_btn.rowconfigure(1, weight=1)

        self._log_frame = ttk.LabelFrame(self._mainframe, text="Log", padding="10")
        self._log_frame.grid(row=2, column=0, pady=10, sticky=(E, W, N, S))

        self._text_log = Text(self._log_frame, height=6, font=('Courier', 10))
        self._text_log.grid(row=0, column=0, pady=5, sticky=(E, W, N, S))
        self._scrollbar_tl = ttk.Scrollbar(self._log_frame, orient=VERTICAL, command=self._text_log.yview)
        self._scrollbar_tl.grid(row=0, column=1, pady=5, sticky=(N, S))
        self._text_log.configure(yscrollcommand=self._scrollbar_tl.set)

    def configura_layout(self):
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.rowconfigure(2, weight=1)
        self._tiempo_frame.columnconfigure(0, weight=1)
        self._tiempo_frame.columnconfigure(15, weight=1)
        self._log_frame.rowconfigure(0, weight=1)
        self._log_frame.columnconfigure(0, weight=1)
        self._text_log.rowconfigure(0, weight=1)
        self._text_log.columnconfigure(0, weight=1)
        self._scrollbar_tl.rowconfigure(2, weight=1)

    def validar_entrada_0a9(self, nuevo_texto):
        """Valida que la entrada sea un solo dígito numérico"""
        # Permitir campo vacío (para poder borrar).
        if nuevo_texto == "":
            return True

        # Solo permitir 1 carácter.
        if len(nuevo_texto) > 1:
            return False

        # Solo permitir dígitos.
        if nuevo_texto.isdigit():
            return True

        return False

    def validar_entrada_0a5(self, nuevo_texto):
        """Valida que la entrada sea un solo dígito numérico de 0 a 5"""
        # Permitir campo vacío (para poder borrar).
        if nuevo_texto == "":
            return True

        # Solo permitir 1 carácter.
        if len(nuevo_texto) > 1:
            return False

        # Solo permitir dígitos de 0 a 6.
        if nuevo_texto.isdigit() and int(nuevo_texto) < 6:
            return True

        return False

    def _start_timer(self):
        if not self.timer_activo:
            self.timer_contador = int(self._horas1_sv.get()) * 60 * 60 * 10 + int(self._horas2_sv.get()) * 60 * 60 +\
                int(self._minutos1_sv.get()) * 60 * 10 + int(self._minutos2_sv.get()) * 60 + int(self._segundos1_sv.get()) * 10 + int(self._segundos2_sv.get())
            if self.timer_contador > 0:
                self.log(f"Iniciando timer {self._horas1_sv.get()}{self._horas2_sv.get()}:{self._minutos1_sv.get()}{self._minutos2_sv.get()}:{self._segundos1_sv.get()}{self._segundos2_sv.get()}...")
                self._start_btn.state(["disabled"])
                self._horas1.state(["disabled"])
                self._horas2.state(["disabled"])
                self._minutos1.state(["disabled"])
                self._minutos2.state(["disabled"])
                self._segundos1.state(["disabled"])
                self._segundos2.state(["disabled"])
                self.timer_contador += 1
                self.timer_activo = True
                self.update_counter()
                self._root.iconify()
                # Necesita perder el foco en Windows para que funcione el aviso.
                if sys.platform == "win32":
                    hwnd_desktop = ctypes.windll.user32.GetDesktopWindow()
                    ctypes.windll.user32.SetForegroundWindow(hwnd_desktop)

    def _stop_timer(self):
        self.timer_activo = False
        self._root.title("** PARADO ***")
        self.log("*** PARADO ***")
        self._start_btn.state(["!disabled"])
        self._horas1.state(["!disabled"])
        self._horas2.state(["!disabled"])
        self._minutos1.state(["!disabled"])
        self._minutos2.state(["!disabled"])
        self._segundos1.state(["!disabled"])
        self._segundos2.state(["!disabled"])

    def update_counter(self):
        if self.timer_activo:
            self._root.after(1000, self.update_counter)
            self.timer_contador -= 1
            hor1 = int(self.timer_contador // 36000)
            hor2 = int((self.timer_contador - (hor1 * 36000)) // 3600)
            min1 = int((self.timer_contador - (hor1 * 36000) - (hor2 * 3600)) // 600)
            min2 = int((self.timer_contador - (hor1 * 36000) - (hor2 * 3600) - (min1 * 600)) // 60)
            seg1 = int((self.timer_contador - (hor1 * 36000) - (hor2 * 3600) - (min1 * 600) - (min2 * 60)) // 10)
            seg2 = int(self.timer_contador - (hor1 * 36000) - (hor2 * 3600) - (min1 * 600) - (min2 * 60) - (seg1 * 10))
            self._root.title(f"{hor1}{hor2}:{min1}{min2}:{seg1}{seg2} {self.timer_contador}s")
            self._horas1_sv.set(hor1)
            self._horas2_sv.set(hor2)
            self._minutos1_sv.set(min1)
            self._minutos2_sv.set(min2)
            self._segundos1_sv.set(seg1)
            self._segundos2_sv.set(seg2)

            if self.timer_contador < 1:
                self.log("*** FINALIZADO ***")
                self.timer_activo=False
                self._start_btn.state(["!disabled"])
                self._start_btn.state(["!disabled"])
                self._horas1.state(["!disabled"])
                self._horas2.state(["!disabled"])
                self._minutos1.state(["!disabled"])
                self._minutos2.state(["!disabled"])
                self._segundos1.state(["!disabled"])
                self._segundos2.state(["!disabled"])
                # Reproduce un sonido.
                if _loadedMPV:
                    self.reproduce_sonidos()

                if sys.platform == "linux":
                    self.muestra_parpadeo_linux()
                elif sys.platform == "win32":
                    self.muestra_parpadeo_windows()

    def muestra_parpadeo_windows(self):
        # Usar FlashWindowEx para parpadeo continuo
        self.flash_window(self.hwnd, -1)

    def flash_window(self, hwnd, count=10, timeout=0):
        """
        Hace parpadear la ventana en la barra de tareas
        """
        # FlashWindowEx function
        FLASHW_STOP = 0
        FLASHW_CAPTION = 1
        FLASHW_TRAY = 2
        FLASHW_ALL = 3
        FLASHW_TIMER = 4
        FLASHW_TIMERNOFG = 12

        class FLASHWINFO(ctypes.Structure):
            _fields_ = [
                ('cbSize', wintypes.UINT),
                ('hwnd', wintypes.HWND),
                ('dwFlags', wintypes.DWORD),
                ('uCount', wintypes.UINT),
                ('dwTimeout', wintypes.DWORD)
            ]

        flash_info = FLASHWINFO()
        flash_info.cbSize = ctypes.sizeof(flash_info)
        flash_info.hwnd = hwnd
        flash_info.dwFlags = FLASHW_ALL | FLASHW_TRAY | FLASHW_TIMERNOFG
        flash_info.uCount = count
        flash_info.dwTimeout = timeout

        result = ctypes.windll.user32.FlashWindowEx(ctypes.byref(flash_info))

    def muestra_parpadeo_linux(self):
        # Muestra el aviso en la ventana minimizada o sin foco.
        atom_demands_attention = self.d.intern_atom('_NET_WM_STATE_DEMANDS_ATTENTION')
        atom_wm_state = self.d.intern_atom('_NET_WM_STATE')
        event_data = event.ClientMessage(
            window=self.window_id,
            client_type=atom_wm_state,
            data=(32, [1, atom_demands_attention, 0, 0, 0])
        )
        root = self.d.screen().root
        root.send_event(event_data, event_mask=X.SubstructureNotifyMask | X.SubstructureRedirectMask)
        self.d.flush()

    def reproduce_sonidos(self):
        current_path=os.path.dirname(os.path.abspath(__file__))
        sonido1=os.path.join(current_path, 'Spo.wav')
        sonido2=os.path.join(current_path, 'IsTimeToRest.amr')
        player = mpv.MPV()
        if os.path.exists(sonido1):
            for i in range(5):
                player.play(sonido1)
                player.wait_for_playback()  # Espera a que termine
        else:
            print(f"No existe el fichero {sonido1}")
        if os.path.exists(sonido2):
            player.play(sonido2)
            player.wait_for_playback()
        else:
            print(f"No existe el fichero {sonido2}")
        player.terminate()

    def _horas1_update(self, valor):
        valor_entero = int(float(valor))
        self._horas1_sv.set(valor_entero)

    def _horas2_update(self, valor):
        valor_entero = int(float(valor))
        self._horas2_sv.set(valor_entero)

    def _minutos1_update(self, valor):
        valor_entero = int(float(valor))
        self._minutos1_sv.set(valor_entero)

    def _minutos2_update(self, valor):
        valor_entero = int(float(valor))
        self._minutos2_sv.set(valor_entero)

    def _segundos1_update(self, valor):
        valor_entero = int(float(valor))
        self._segundos1_sv.set(valor_entero)

    def _segundos2_update(self, valor):
        valor_entero = int(float(valor))
        self._segundos2_sv.set(valor_entero)

    def log(self, mensaje):
        ahora = datetime.now()
        formato_milesimas = ahora.strftime("%Y-%m-%d %H:%M:%S.%f")
        self._text_log.insert(END, f"[{formato_milesimas}] {mensaje}\n")
        self._text_log.see(END)
        self._root.update()

    def on_cerrar(self):
        if sys.platform == "linux":
            self.d.close()
        self._root.destroy()

    def ejecutar(self):
        self._root.protocol("WM_DELETE_WINDOW", self.on_cerrar)
        self._root.mainloop()

    def ajusta_ventana(self):
        self._root.update()
        ancho_ventana = self._root.winfo_width()
        alto_ventana = self._root.winfo_height()
        ancho_pantalla = self._root.winfo_screenwidth()
        alto_pantalla = self._root.winfo_screenheight()
        pos_x = (ancho_pantalla - ancho_ventana) // 2
        pos_y = (alto_pantalla - alto_ventana) // 2
        self._root.geometry(f"+{pos_x}+{pos_y}")

if __name__ == "__main__":
    app = RestTime()
    app.ejecutar()
