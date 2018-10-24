import gi, asyncio
from telethon import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

client = TelegramClient('telegramgtk+', 138604, '4c57c7c2e94b8116f007dbd39767173a')
numberinputbox = None
codeinputbox = None
current_user = None

def login():
	loop = asyncio.get_event_loop()
	try: 
		loop.run_until_complete(client.connect())
		if not loop.run_until_complete(client.is_user_authorized()):
			dialog = LoginWindowStep1(self)
			response = dialog.run()
			phonenumber = numberinputbox.get_text()
			loop.run_until_complete(client.send_code_request(phonenumber))
			dialog2 = LoginWindowStep2(self)
			response = dialog2.run()
			code = codeinputbox.get_text()
			global current_user
			current_user = loop.run_until_complete(client.sign_in(phonenumber, code))
	finally:
		print("Logged in successfully!")

class MainWindow(Gtk.Window):
	def draw_pixbuf(self, widget, event):
		path = '\\testwp.jpg'
		pixbuf = Gtk.Gdk.pixbuf_new_from_file(path)
		widget.window.drawpixbuf(widget.style.bg_gc[Gtk.STATE_NORMAL], pixbug, 0, 0, 0, 0)


	def __init__(self):
		Gtk.Window.__init__(self, title="Telegram GTK", default_width=800, default_height=600)
		
class ChatHeader(Gtk.ListBoxRow):


	def open_chat(self, widget):
		print("clicked on " + self.data)

	def __init__(self, data):
		super(Gtk.ListBoxRow, self).__init__()
		self.data = data
		lb = Gtk.Label(data)
		self.add(lb)
		lb.set_hexpand(False)
		lb.set_margin_start(0)
		lb.set_xalign(Gtk.Align.START)
		lb.set_direction(Gtk.TextDirection.RTL)
		self.connect("focus", open_chat)

class LoginWindowStep1(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Authenticate", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(200,150)
		mainlabel = Gtk.Label("Time to log in! Input your number, prefix included, you'll receive a code to enter in the next step.")
		global numberinputbox
		numberinputbox = Gtk.Entry()
		box = self.get_content_area()
		box.add(mainlabel)
		box.add(numberinputbox)
		self.show_all()

class LoginWindowStep2(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Authenticate2", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(200,150)
		mainlabel = Gtk.Label("Enter the code you received in the SMS or by telegram message.")
		global codeinputbox
		codeinputbox = Gtk.Entry()
		box = self.get_content_area()
		box.add(mainlabel)
		box.add(codeinputbox)
		self.show_all()

login()

builder = Gtk.Builder()
builder.add_from_file("testlayout001.glade")
main_window = builder.get_object("main_window")

main_window.connect("destroy", Gtk.main_quit)

loop = asyncio.get_event_loop()
result = loop.run_until_complete(client.get_dialogs())
chats_listbox = builder.get_object("chats_listbox")
print(chats_listbox)
for di in result:
	chats_listbox.add(ChatHeader(di.name))

main_window.show_all()
Gtk.main()