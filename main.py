from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
import threading
import os
import yt_dlp

# កំណត់ពណ៌ផ្ទៃខាងក្រោយ Dark Mode ទំនើប (#111827)
Window.clearcolor = (0.07, 0.09, 0.15, 1)

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        with self.canvas.before:
            Color(0.15, 0.45, 0.95, 1)  # ពណ៌ខៀវ Royal Blue ភ្លឺស្អាត
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class DownloaderApp(App):
    def build(self):
        self.title = "Video Saver"
        
        root = BoxLayout(orientation='vertical', padding=, spacing=15)
        
        # ចំណងជើងធំ
        title = Label(
            text="Video Saver",
            font_size='26sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height='45dp'
        )
        root.add_widget(title)
        
        # ចំណងជើងរង
        subtitle = Label(
            text="Fast & HD Video Downloader",
            font_size='14sp',
            color=(0.6, 0.65, 0.75, 1),
            size_hint_y=None,
            height='25dp'
        )
        root.add_widget(subtitle)
        
        root.add_widget(Widget(size_hint_y=None, height='25dp'))
        
        # ប្រអប់បញ្ចូល Link រចនាយ៉ាងស្អាត
        self.url_input = TextInput(
            hint_text="Paste Facebook video link here...",
            multiline=False,
            size_hint_y=None,
            height='55dp',
            font_size='15sp',
            padding=,
            background_color=(0.14, 0.18, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.6, 1, 1)
        )
        root.add_widget(self.url_input)
        
        root.add_widget(Widget(size_hint_y=None, height='10dp'))
        
        # ប៊ូតុង DOWNLOAD NOW កោងមូល
        self.btn_download = RoundedButton(
            text="DOWNLOAD NOW",
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height='55dp',
            color=(1, 1, 1, 1)
        )
        self.btn_download.bind(on_press=self.start_download)
        root.add_widget(self.btn_download)
        
        root.add_widget(Widget(size_hint_y=None, height='20dp'))
        
        # អក្សរបង្ហាញស្ថានភាព
        self.status_label = Label(
            text="Ready to download",
            font_size='15sp',
            color=(0.4, 0.85, 0.5, 1),
            size_hint_y=None,
            height='35dp'
        )
        root.add_widget(self.status_label)
        
        root.add_widget(Widget())
        
        return root

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.color = (1, 0.35, 0.35, 1)
            self.status_label.text = "Please paste a video link first!"
            return
            
        self.btn_download.disabled = True
        self.status_label.color = (0.95, 0.75, 0.25, 1)
        self.status_label.text = "Downloading... Please wait"
        threading.Thread(target=self._download_worker, args=(url,)).start()

    def _download_worker(self, url):
        download_dir = "/storage/emulated/0/Download"
        os.makedirs(download_dir, exist_ok=True)
        
        ydl_opts = {
            "outtmpl": os.path.join(download_dir, "FB_%(id)s.%(ext)s"),
            "format": "best",
            "windowsfilenames": True,
            "ignoreerrors": True,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            os.system(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d "file://{download_dir}" > /dev/null 2>&1')
            Clock.schedule_once(lambda dt: self._update_status("Download Complete! Check Gallery.", True, (0.3, 0.9, 0.4, 1)))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_status("Download Failed! Try another link.", True, (1, 0.3, 0.3, 1)))

    def _update_status(self, message, enable_btn, color):
        self.status_label.text = message
        self.status_label.color = color
        self.btn_download.disabled = not enable_btn
        if enable_btn:
            self.url_input.text = ""

if __name__ == '__main__':
    DownloaderApp().run()
