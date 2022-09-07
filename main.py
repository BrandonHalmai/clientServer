# Below are the external libraries that we'll be using to create our PythonClient server. The socket library is
# used for networking; such as establishing, maintaining and terminating a connection. Kivy is used for designing
# interface and the window itself. Sys is used to access or manipulate the interpreter; in this application
# we'll be using the 'exit()' method to quit out of our application. Lastly the webbrowser library allows us to
# view web-based documents to users.

import socket
import kivy
import sys
import webbrowser

# Here were setting a fixed value of '1.11.1' to indicate a version that is required to run this application.
kivy.require('1.11.1')
# Much like the importation of our libraries, were importing certain methods as we don't need all of them. This will
# reduce the amount fo resources to run.
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.graphics import *


# Here we are defining a class as 'FloatLayout' with the parameter 'FloatLayout'. This will determine the window size,
# status text and ip address to the functions that will allow us to connect to the server, drop files, get help and
# terminate the application.
class FloatLayout(FloatLayout):
    Window.size = (360, 200)  # These static values correspond to the window size.
    status_text = StringProperty()  # Both status_text and ip_address values correspond to a string value as it's
    # subject to change.
    ip_address = StringProperty()  

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 0, 0, 0.5, mode="rgba")
            self.rect = Rectangle(pos=(310, 0), size=(50, 50))
            Color(255, 255, 255, 1, mode="rgba")
            Line(points=(320, 5, 335, 45, 350, 5, 315, 30, 355, 30, 320, 5))

    def connect_to_server(self, instance, value):
        self.status_text = ('Not connected')
        HOST = self.ip.text
        PORT = 6789
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((HOST, PORT))
            self.status_text = ('Connection Test Successful \nDrag and Drop Files to Send')
            print(s)
            # Drag and Drop
            Window.bind(on_drop_file=self._on_file_drop)

            if (value != ''):
                sent = str(s.send(value.encode()))
                if sent == 0:
                    self.status_text = ('Failure: 0 Characters Sent')
                else:
                    print(sent + ' Characters Sent Successfully')
                    print(value)
                    self.status_text = (sent + ' Characters sent successfully')
                print(s)
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            print(s)
        except socket.timeout as e:
            self.status_text = ('Connection Test Failure: \n' + str(e))
        except socket.error as e:
            self.status_text = ('Connection Test Failure: \n' + str(e))
        return

    def _on_file_drop(self, window, file_path, x, y):
        print(file_path)
        data = open(file_path, 'r').read()
        self.connect_to_server('', data)
        return

    def help(self):
        webbrowser.open('help.html', new=2, autoraise=True)

    def exit(self):
        sys.exit()


class MyApp(App):
    def build(self):
        self.title = 'Python Client'
        return FloatLayout()


if __name__ == '__main__':
    MyApp().run()
