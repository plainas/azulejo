import wnck, gtk
from collections import deque

class Window:
     def __init__(self, x,y, width, height):
          self.x = x
          self.y = y
          self.width = width
          self.height = heigt
          

class WindowManager:

     def __init__(self):
          self.maximized_window_geometry = self.get_screen_geometry()
          self.upper_corner = self.maximized_window_geometry[:2]
          self.screen_width = self.maximized_window_geometry[2]
          self.screen_height = self.maximized_window_geometry[3]

          #because window resizing is not acurate we need a quick dirty workaround
          self.window_geometry_error_margin=30

          #variable to hold the amount of windows since the last arrangement
          self.arrangement_size = 0



     def get_screen_geometry(self):
          return gtk.gdk.get_default_root_window().property_get('_NET_WORKAREA')[2][:4]



     def parse_simple_math_expressions(self,expression):
          expression = str(expression)
          expression = expression.replace('w',str(self.screen_width))
          expression = expression.replace('h',str(self.screen_height))
          return eval(expression)


     def parse_geometry(self,geometry):
          return map(self.parse_simple_math_expressions,geometry)


     def parse_arrangement(self,arrangement):
          return map(self.parse_geometry, arrangement)


     def get_all_windows(self):
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
     def resize_single_window(self,geometries):
          def similar_geometries(ga,gb):
              for i in range(4):
                  if abs(ga[i] - gb[i]) >= self.window_geometry_error_margin:
                      return False
              return True
      
          window = wnck.screen_get_default().get_active_window()     
          window_original_geometry = window.get_geometry()

          #not an arrangement, but a list of geometires for that matter
          geometries_numeric = self.parse_arrangement(geometries)
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


     def resize_windows(self,arrangement):
          global arrangement_size
          arrangement_numeric = self.parse_arrangement(arrangement)
          #print arrangement_numeric
          all_windows = self.get_all_windows()
          amount_of_windows = len(all_windows)
        
          if amount_of_windows < len(arrangement_numeric):
               arrangement_numeric = arrangement_numeric[:amount_of_windows]

          i = 0
          arrangement_size = len(arrangement_numeric) #global scope variable, also used to rotate windows
          while i < arrangement_size:
               geometry_list_args = [0,255]
               index = arrangement_size - (i+1) #we must start in the end in order to keep window order correct
               geometry_list_args.extend(map (int,arrangement_numeric[index]))
               all_windows[index].unmaximize()
               all_windows[index].set_geometry(*geometry_list_args)
               i+=1

     def rotate_windows(self, dummy):
          global arrangement_size
          windows = self.get_all_windows()
          amount_of_windows = len(windows)

          if amount_of_windows > arrangement_size:
               windows = windows[:arrangement_size]

          geos = []
          for window in windows:
               window_geo = window.get_geometry()
               window_geo = window_geo[:4]
               geos.append(window_geo)

          #do the actual rotations, lets use deque as it's dramatically more efficient than a trivial shift implementation
          windows_deq = deque(windows)
          windows_deq.rotate(1)

          rotation_len = len(windows_deq)
          i = 0
          while i < rotation_len:
               geometry_list_args = [0,255]
               index = rotation_len - (i+1) #again, start by the tail
               geometry_list_args.extend(map (int,geos[index]))
               windows_deq[index].unmaximize()
               windows_deq[index].set_geometry(*geometry_list_args)
               i+=1
