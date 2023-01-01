import tcod as libtcod
from random import choice

from game_messages import MessageLog, Message
from input_handlers import handle_keys

class PanelInfo:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.panel = False
		self.log = MessageLog(x, width, height)

	def render(self, con, screen_width, screen_height):
		libtcod.console_set_default_background(self.panel, libtcod.black)
		libtcod.console_clear(self.panel)
		self.log.render(self.panel)
		libtcod.console_blit(self.panel, 0, 0, screen_width, self.height, 0, 0, self.y)

def main():
	screen_width = 80 # /4 = 20
	screen_height = 50 # /4 ~= 12

	# setup panel params
	panels = {}
	panels['messages'] = PanelInfo(2, 2, screen_width // 2, screen_height // 2)

	# set up console
	libtcod.console_set_custom_font('arial10x10.png', 
		libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(screen_width, screen_height, 
		'libtcod tutorial revised', False, 
		libtcod.RENDERER_SDL2, vsync=True)

	# set up all panels
	con = libtcod.console.Console(screen_width, screen_height)
	for panel in panels:
		panels[panel].panel = libtcod.console.Console(
			panels[panel].width, 
			panels[panel].height
		)

	# input variables
	key = libtcod.Key()
	mouse = libtcod.Mouse()

	while not libtcod.console_is_window_closed():
		# poll input
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

		# parse input
		action = handle_keys(key)

		exit = action.get('exit')
		fullscreen = action.get('fullscreen')
		move = action.get('move')
		confirm = action.get('confirm')
		cancel = action.get('cancel')

		if exit:
			return True

		if fullscreen:
			libtcod.console_set_fullscreen(
				not libtcod.console_is_fullscreen())

		if move:
			panels['messages'].log.add('moved!')

		if confirm:
			panels['messages'].log.add('confirmed!')

		if cancel:
			panels['messages'].log.add('canceled!')

		# draw screen
		for panel in panels:
			panels[panel].render(con, screen_width, screen_height)

		libtcod.console_flush()

if __name__ == '__main__':
	main()