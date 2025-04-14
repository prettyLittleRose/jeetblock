import sys
import json
import asyncio

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from qasync import QEventLoop

from telethon import TelegramClient, events, functions
from telethon.tl.types import PeerUser

from framework.ui import *

conf = json.load(open('./settings.json', 'r', encoding='utf-8'))
ui = MainWindow()

class Worker(QThread):
    terminal_signal = pyqtSignal(str)
    increment_signal = pyqtSignal(str)

    def __init__(self, client: TelegramClient):
        super().__init__()
        self.client = client

    async def handle_message(self, event):
        message = event.message
        if not event.is_private:
            return
        
        result = await self.client(functions.messages.GetPeerSettingsRequest(
            peer = PeerUser(event.sender_id)
        ))

        if not hasattr(result.settings, 'phone_country'):
            self.terminal_signal.emit(
                f"""[<span style="color: yellow;">FAILED</span>] There was no 'phone_country' attribute in the 'GetPeerSettingsRequest' class. This is likely because the version of Telethon you're using is outdated. Please update your client by uninstalling telethon, and running:<br><br>pip install git+https://github.com/LonamiWebs/Telethon.git@67765f84a58598cee3fa52abeea9a1f76c993fdd<br>"""
            )
            return
        
        if not result.settings.phone_country in settings.get_countries():
            return
        
        self.terminal_signal.emit(
            f"""[<span style="color: lightblue;">OUTPUT</span>] <b>Threat Detected</b> (UID: {event.sender_id}, Country: {result.settings.phone_country})"""
        )
        
        should_block = settings.get_block_user()
        should_delete = settings.get_delete_chat()
        should_log = settings.get_log_user_info()

        if should_log:
            try:
                self.terminal_signal.emit(
                    f'<br>Username: {event.sender.username}<br>Nickname: {event.sender.first_name + ("" if not event.sender.last_name else " " + event.sender.last_name)}<br>Has Premium: {event.sender.premium != None}<br>Has Profile Picture: {event.sender.photo != None}<br>'
                )
            except:
                pass
           
        if should_block:
            await self.client(functions.contacts.BlockRequest(id = event.sender_id))
            self.increment_signal.emit('Blocked')
            self.terminal_signal.emit(
                f"""[<span style="color: lightblue;">OUTPUT</span>] Blocked User"""
            )
        
        if should_delete:
            await self.client(functions.messages.DeleteHistoryRequest(peer = PeerUser(event.sender_id), max_id = 0, revoke = True))
            self.increment_signal.emit('Deleted')
            self.terminal_signal.emit(
                f"""[<span style="color: lightblue;">OUTPUT</span>] Deleted Chat"""
            )

    def run(self):
        self.client.add_event_handler(self.handle_message, events.NewMessage)

async def start():
    client = TelegramClient('Me', conf['api_id'], conf['api_hash'])
    await client.start()

    worker = Worker(client)
    worker.terminal_signal.connect(ui.log_to_terminal)
    worker.increment_signal.connect(ui.increment_counter)
    worker.start()

    await client.run_until_disconnected()
    return worker

def close_event_handler(worker):
    if worker and worker.isRunning():
        worker.quit()
        worker.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    ui.show()

    worker = None
    try:
        worker = loop.run_until_complete(start())
    except Exception as E:
        ui.log_to_terminal(f'[<span style="color: red;">FAILURE</span>] {str(E)}')

    app.aboutToQuit.connect(lambda: close_event_handler(worker))
    with loop:
        loop.run_forever()
