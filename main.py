import gi, asyncio
from telethon import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

client = TelegramClient('telegramgtk+', 138604, '4c57c7c2e94b8116f007dbd39767173a')
#client.start()  --  replaced with custom login
numberinputbox = None
codeinputbox = None
current_user = None

class MainWindow(Gtk.Window):
	def login(self):
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

	def __init__(self):
		Gtk.Window.__init__(self, title="Telegram GTK", default_width=800, default_height=600)
		#chats_listbox = Gtk.ListBox()

		self.login()

		vbox = Gtk.VBox()
		swin = Gtk.ScrolledWindow()

		loop = asyncio.get_event_loop()
		result = loop.run_until_complete(client.get_dialogs())
		for di in result:
		#	chats_listbox.add(ChatHeader(di.name))
			vbox.pack_start(ChatHeader(di.name), 1, 1, 0)

		swin.add_with_viewport(vbox)
		#print(dir(chats_listbox))

		#main_grid = Gtk.Grid()
		#self.add(main_grid)
		#main_grid.attach(chats_listbox, 1, 1, 1, 1)

		#content_grid = Gtk.Grid()
		#main_grid.attach(content_grid, 2, 1, 2, 1)

		self.add(swin)
		self.set_size_request(600,400)

class ChatHeader(Gtk.ListBoxRow):
	def __init__(self, data):
		super(Gtk.ListBoxRow, self).__init__()
		self.data = data
		self.add (Gtk.Label(data))

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

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()

