import customtkinter
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from screen_brightness_control import get_brightness, set_brightness

class SystemControlsApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('System Controls')

        # Volume Slider
        self.volume_label = customtkinter.CTkLabel(self, text='Volume:')
        self.volume_label.pack(pady=10)
        self.volume_slider = customtkinter.CTkSlider(self, from_=0, to=100, orientation='horizontal', command=self.set_volume)
        self.volume_slider.pack(pady=10)

        # Brightness Slider
        self.brightness_label = customtkinter.CTkLabel(self, text='Brightness')
        self.brightness_label.pack(pady=10)
        self.brightness_slider = customtkinter.CTkSlider(self, from_=0, to=100, number_of_steps=10, orientation='horizontal', command=self.set_brightness)
        self.brightness_slider.pack(pady=10)

        # Getting default playback device for volume control
        devices = AudioUtilities.GetSpeakers()
        self.volume_control = cast(devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume)
        )

        # Getting brightness control interface
        self.brightness_control = get_brightness(display=0)

    def set_volume(self, value):
        volume = int(value)
        # Setting systme volume using pycaw
        self.volume_control.SetMasterVolumeLevelScalar(float(volume / 100), None)

    def set_brightness(self, value):
        brightness = int(value)
        # Setting screen brightness using screen-brightness-control
        set_brightness(display=0, value=brightness)


if __name__ == '__main__':
    app = SystemControlsApp()
    app.mainloop()
