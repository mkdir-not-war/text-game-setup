import tcod as libtcod
import textwrap

class Message:
	def __init__(self, text, color):
		self.text = text
		self.color = color

class MessageLog:
	def __init__(self, x, width, height):
		self.messages = []
		self.x = x
		self.width = width
		self.height = height

	def add(self, msgstr, color=libtcod.white):
		message = Message(msgstr, color)
		new_msg_lines = textwrap.wrap(message.text, self.width)

		for line in new_msg_lines:
			if len(self.messages) == self.height:
				del self.messages[0]

			self.messages.append(Message(line, message.color))

	def clear(self):
		self.messages = []

	def render(self, panel, y_start=2):
		y = y_start
		for message in self.messages:
			libtcod.console_set_default_foreground(panel, message.color)
			libtcod.console_print_ex(panel, self.x, y, 
				libtcod.BKGND_NONE, libtcod.LEFT, message.text)
			y += 1