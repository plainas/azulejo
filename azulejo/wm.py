import wnck, gtk


class Window:
	def __init__(self, x,y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = heigt
		

class WindowManager:
	def get_screen_geometry():
		return gtk.gdk.get_default_root_window().property_get('_NET_WORKAREA')[2][:4]	


	def get_all_windows():
		def f_normal_window(window):
		if window.get_window_type() == wnck.WindowType.__enum_values__[0]:
			return True
		return False

		s = wnck.screen_get_default()

		while gtk.events_pending():
		gtk.main_iteration()

		windows = s.get_windows_stacked()
		filtered_windows = filter(f_normal_window,windows)
		filtered_windows.reverse()

		return filtered_windows


	#TODO: rename to resize_top_window
	def resize_single_window(geometries):
		def similar_geometries(ga,gb):
		for i in range(4):
			if abs(ga[i] - gb[i]) >= window_geometry_error_margin:
				return False
		return True
	 
		window = wnck.screen_get_default().get_active_window()	
		window_original_geometry = window.get_geometry()

		#not an arrangement, but a list of geometires for that matter
		geometries_numeric = parse_arrangement(geometries)
		geometry_list_args = [0,255]
		
		i=1
		geometry_to_use_index=0	
		for geometry_numeric in geometries_numeric:
		if similar_geometries(geometry_numeric, window_original_geometry):
			geometry_to_use_index = i % len(geometries_numeric)
			break
		i+=1 

		geometry_list_args.extend(map (int,geometries_numeric[geometry_to_use_index]))
		window.unmaximize()
		window.set_geometry(*geometry_list_args)

