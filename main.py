from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import os
import yt_dlp

class DownloaderApp(App):
    def build(self):
        self.title = "FB Video Downloader"
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.label_title = Label(
            text="FB Video Downloader", 
            font_size='22sp', 
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.label_title)
        
        self.url_input = TextInput(
            hint_text="Paste Link Facebook ទីនេះ...", 
            multiline=False, 
            size_hint=(1, 0.2),
            font_size='16sp'
        )
        layout.add_widget(self.url_input)
        
        self.btn_download = Button(
            text="Download វីដេអូ", 
            size_hint=(1, 0.2), 
            font_size='18sp',
            background_color=(0.1, 0.6, 0.9, 1)
        )
        self.btn_download.bind(on_press=self.start_download)
        layout.add_widget(self.btn_download)
        
        self.status_label = Label(
            text="រង់ចាំបញ្ចូល Link...", 
            font_size='16sp', 
            size_hint=(1, 0.4)
        )
        layout.add_widget(self.status_label)
        
        return layout

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "សូមបញ្ចូល Link ជាមុនសិន!"
            return
            
        self.btn_download.disabled = True
        self.status_label.text = "កំពុងទាញយក... សូមរង់ចាំ!"
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
            Clock.schedule_once(lambda dt: self._update_status("ទាញយកជោគជ័យ! ចូលមើលក្នុង Gallery។", True))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_status(f"មានបញ្ហា៖ {str(e)}", True))

    def _update_status(self, message, enable_btn):
        self.status_label.text = message
        self.btn_download.disabled = not enable_btn
        if enable_btn:
            self.url_input.text = ""

if __name__ == '__main__':
    DownloaderApp().run()
