try:
 # for Python3
 from tkinter import *
except ImportError:
 # for Python2
 from Tkinter import *

try:
    from PIL import ImageTk
    from PIL import Image
    import googlemaps
    from staticmap import StaticMap, CircleMarker
except ImportError:
    exit()


class GroundStationApp:
    def __init__(self, master):
        self.master = master
        self.render_image()
        self.initialize_image()
        self.create_altitude_widget()
        self.create_speed_widget()
        self.map_coordinates = (39.9526, 75.1652)
        self.load_image()

    def initialize_image(self):
        self.current_image_path = "monkey.jpg"
        self.img = Image.open(self.current_image_path)
        self.photo_img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.master, image=self.photo_img)
        self.panel.grid(row=1, column=0, columnspan=2)

    def create_altitude_widget(self):
        self.altitude_widget = Label(self.master, text="Altitude")
        self.altitude_widget.config(font=("Arial", 24))
        self.altitude_widget.grid(row=0, column=0)

    def create_speed_widget(self):
        self.altitude_widget = Label(self.master, text="Speed")
        self.altitude_widget.config(font=("Arial", 24))
        self.altitude_widget.grid(row=0, column=1)

    def load_image(self):
        self.map = None
        #This static map library will load map positions
        #self.map = StaticMap(width, height, padding_x, padding_y, url_template, tile_size)

    # This method renders the images
    def render_image(self):
        self.static_map = StaticMap(width=300, height=300, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
        self.drone_marker = CircleMarker((39.952583, -75.165222), '#0036FF', 12)
        self.static_map.add_marker(self.drone_marker)
        image = self.static_map.render()
        image.save('map.png')

    def run(self):
        self.master.mainloop()


# The main method which runs the code for testing purposes
def main():
    root = Tk()
    app = GroundStationApp(root)
    app.run()


if __name__ == "__main__":
    main()