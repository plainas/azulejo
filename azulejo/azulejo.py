import time
import keybinder
import configuration
import wm
import gtk, wnck

window_manager = wm.WindowManager()

#(windows_deq[0]).activate(int(time.time())) #not sure why it doesn't work. if uncommented causes other windows beyond the rotated ones to hide behind current ones even after pressing ctrl+tab


callable_actions = dict(\
    resize_single_window = window_manager.resize_single_window, \
    resize_windows = window_manager.resize_windows, \
    rotate_windows = window_manager.rotate_windows
)


def dispatcher(dis_param):
    print dis_param
    func = dis_param[0]
    param = dis_param[1]
    wnck.screen_get_default().force_update() #doesn't apear to do much
    func(param)    

def run():
    for action in configuration.conf_data:
        keybind = action['keybind']
        function_name = action['function']
        function = callable_actions[function_name]
        parameters = action['parameters']
        dispacher_parameters = [function, parameters]
        keybinder.bind(keybind, dispatcher ,dispacher_parameters)        

    gtk.main()
