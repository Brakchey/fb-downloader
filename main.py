from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import threading
import os
import yt_dlp

class DownloaderApp(App):
    def build(self):
        self.title = "Video Saver"
        
        root = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        # ចំណងជើង
        self.title_label = Label(
            text="[b]Video Saver[/b]",
            markup=True,
            font_size='26sp',
            size_hint=(1, 0.15),
            color=(0.2, 0.6, 1, 1)
        )
        root.add_widget(self.title_label)
        
        self.subtitle = Label(
            text="Fast Video Downloader",
            font_size='14sp',
            size_hint=(1, 0.08),
            color=(0.7, 0.7, 0.7, 1)
        )
        root.add_widget(self.subtitle)
        
        # ប្រអប់ Paste Link
        self.url_input = TextInput(
            hint_text="Paste video link here...",
            multiline=False,
            size_hint=(1, 0.15),
            font_size='16sp',
            padding=
        )
        root.add_widget(self.url_input)
        
        # ប៊ូតុង Download
        self.btn_download = Button(
            text="DOWNLOAD VIDEO",
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.15),
            background_color=(0.1, 0.5, 0.9, 1)
        )
        self.btn_download.bind(on_press=self.start_download)
        root.add_widget(self.btn_download)
        
        # លេខភាគរយរត់ពី 1% ដល់ 100%
        self.percent_label = Label(
            text="0%",
            font_size='22sp',
            bold=True,
            size_hint=(1, 0.12),
            color=(0.2, 0.8, 0.4, 1)
        )
        root.add_widget(self.percent_label)
        
        # របារ Progress Bar
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(1, 0.1)
        )
        root.add_widget(self.progress_bar)
        
        # អក្សរបង្ហាញស្ថានភាព
        self.status_label = Label(
            text="Ready to download",
            font_size='14sp',
            size_hint=(1, 0.25),
            color=(0.8, 0.8, 0.8, 1)
        )
        root.add_widget(self.status_label)
        
        return root

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "Please paste a video link first!"
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
            
        self.btn_download.disabled = True
        self.progress_bar.value = 0
        self.percent_label.text = "0%"
        self.status_label.text = "Starting download..."
        self.status_label.color = (1, 0.8, 0.2, 1)
        threading.Thread(target=self._download_worker, args=(url,)).start()

    def _progress_hook(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes') or 0
            if total > 0:
                percent = int((downloaded / total) * 100)
                Clock.schedule_once(lambda dt: self._update_percent(percent, "Downloading..."))
        elif d.get('status') == 'finished':
            Clock.schedule_once(lambda dt: self._update_percent(100, "Saving to gallery..."))

    def _update_percent(self, percent, msg):
        self.progress_bar.value = percent
        self.percent_label.text = f"{percent}%"
        self.status_label.text = msg

    def _download_worker(self, url):
        download_dir = "/storage/emulated/0/Download"
        os.makedirs(download_dir, exist_ok=True)
        
        ydl_opts = {
            "outtmpl": os.path.join(download_dir, "FB_%(id)s.%(ext)s"),
            "format": "best",
            "windowsfilenames": True,
            "ignoreerrors": True,
            "progress_hooks": [self._progress_hook],
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            os.system(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d 'file://{download_dir}' > /dev/null 2>&1")
            Clock.schedule_once(lambda dt: self._finish("Download Complete! Check Gallery.", True, (0.2, 0.9, 0.3, 1)))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._finish(f"Download Failed: {str(e)}", True, (1, 0.3, 0.3, 1)))

    def _finish(self, message, enable_btn, color):
        self.status_label.text = message
        self.status_label.color = color
        self.btn_download.disabled = not enable_btn
        if enable_btn:
            self.url_input.text = ""

if __name__ == '__main__':
    DownloaderApp().run()            value=0,
            size_hint_y=None,
            height='20dp'
        )
        root.add_widget(self.progress_bar)
        
        # Status Label
        self.status_label = Label(
            text="Ready to download",
            font_size='14sp',
            color=(0.6, 0.7, 0.8, 1),
            size_hint_y=None,
            height='30dp'
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
        self.progress_bar.value = 0
        self.percent_label.text = "0%"
        self.status_label.color = (0.95, 0.75, 0.25, 1)
        self.status_label.text = "Starting download..."
        threading.Thread(target=self._download_worker, args=(url,)).start()

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes') or 0
            if total > 0:
                percent = int((downloaded / total) * 100)
                Clock.schedule_once(lambda dt: self._update_percent(percent, "Downloading..."))
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self._update_percent(100, "Saving to gallery..."))

    def _update_percent(self, percent, msg):
        self.progress_bar.value = percent
        self.percent_label.text = f"{percent}%"
        self.status_label.text = msg

    def _download_worker(self, url):
        download_dir = "/storage/emulated/0/Download"
        os.makedirs(download_dir, exist_ok=True)
        
        ydl_opts = {
            "outtmpl": os.path.join(download_dir, "FB_%(id)s.%(ext)s"),
            "format": "best",
            "windowsfilenames": True,
            "ignoreerrors": True,
            "progress_hooks": [self._progress_hook],
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            os.system(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d 'file://{download_dir}' > /dev/null 2>&1")
            Clock.schedule_once(lambda dt: self._finish_download("Download Complete! Check Gallery.", True, (0.3, 0.9, 0.4, 1)))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._finish_download("Download Failed! Try another link.", True, (1, 0.3, 0.3, 1)))

    def _finish_download(self, message, enable_btn, color):
        self.status_label.text = message
        self.status_label.color = color
        self.btn_download.disabled = not enable_btn
        if enable_btn:
            self.url_input.text = ""

if __name__ == '__main__':
    DownloaderApp().run()
