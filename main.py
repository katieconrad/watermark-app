from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image, ImageDraw, ImageFont

# Create class to hold variables


class VarHolder:

    def __init__(self):
        self.img = 0
        self.wm_img = 0
        self.panel = 0
        self.width = 0
        self.height = 0


holder = VarHolder()

# Set constants for padding

XPAD = 5
YPAD = 5

# Create tkinter window and maximize it

window = Tk()
window.title("Watermark Your Photos!")
window.config(padx=10, pady=10)
window.attributes("-zoomed", True)

# Create and place frames for widgets and the picture

widget_frame = Frame()
widget_frame.config(padx=10, pady=10)
widget_frame.grid(column=0, row=0)

photo_frame = Frame()
photo_frame.config(padx=10, pady=10)
photo_frame.grid(column=1, row=0)


def open_file():
    """Asks user to select a file to open"""
    filename = fd.askopenfilename(
        title="Select a Photo",
        initialdir="/",
        filetypes=[("Image", "*.jpg"),
                   ("Image", "*.jpeg"),
                   ("Image", "*.png"),
                   ("Image", "*.gif")])

    return filename


def open_img():
    """Opens the selected file as an image"""

    # Get file and open image
    file = open_file()
    img = Image.open(file)

    new_img = resize(img)

    # Convert to PhotoImage and store in holder object
    holder.img = ImageTk.PhotoImage(new_img)

    # Display the image
    display_img(holder.img)


def resize(image):
    """Resizes image if too large for window"""

    ratio = image.size[1] / image.size[0]

    # Get window size
    win_width = window.winfo_width()
    win_height = window.winfo_height()

    # Compare image size to window size and resize as needed
    if image.size[0] > win_width:
        new_width = win_width - 1000
        new_height = round((win_width - 1000) * ratio)
        small_img = image.resize((new_width, new_height))
        if small_img.size[1] > win_height:
            new_width = round((win_height - 150) / ratio)
            new_height = win_height - 150
            small_img = image.resize((new_width, new_height))
    elif image.size[1] > win_height:
        new_width = round((win_height - 150) / ratio)
        new_height = win_height - 150
        small_img = image.resize((new_width, new_height))
    else:
        small_img = image

    return small_img


def display_img(img):
    """Displays an image in the GUI"""
    holder.panel = Label(photo_frame, image=img)
    holder.panel.grid(column=0, row=0, padx=XPAD, pady=YPAD)


def apply_wm():
    """Applies the watermark to the image"""

    # Get text from entry box
    text = wm_entry.get()

    # Get font style and size
    font_type = get_font()

    # Get font colour and opacity
    fill_colour = get_colour()

    # Convert PhotoImage back to Image
    img = ImageTk.getimage(holder.img)

    # Get image size
    holder.width = img.size[0]
    holder.height = img.size[1]

    # Get text coordinates and alignment
    text_coords, text_align = get_placement(holder.width, holder.height)

    # Make a blank image for the text, initialized to transparent text color
    txt_img = Image.new("RGBA", (img.size[0], img.size[1]), (255, 255, 255, 0))

    # Create a drawing context
    draw = ImageDraw.Draw(txt_img)

    # Draw the text
    draw.text(text_coords, text, anchor=text_align, font=font_type, fill=fill_colour)

    # Create the composite and convert to PhotoImage
    wm_img = Image.alpha_composite(img, txt_img)
    holder.wm_img = ImageTk.PhotoImage(wm_img)

    # Display the watermarked image
    display_img(holder.wm_img)


def get_font():
    """Gets font style and size from widgets"""
    size = size_slider.get()
    style = font_box.get()
    if style == "Arial":
        font_style = ImageFont.truetype("arial.ttf", size)
    elif style == "Times New Roman":
        font_style = ImageFont.truetype("times new roman.ttf", size)
    else:
        font_style = ImageFont.truetype("COMIC.TTF", size)
    return font_style


def get_colour():
    """Gets font colour and opacity from widgets"""
    opacity = opacity_slider.get()
    colour = colour_box.get()
    if colour == "Black":
        fill_tuple = (0, 0, 0, opacity)
    else:
        fill_tuple = (255, 255, 255, opacity)
    return fill_tuple


def get_placement(width, height):
    """Gets coordinates and alignment for placement of text"""

    # Get alignment and split it to separate vertical and horizontal alignment
    placement = align_box.get()
    align_list = str.split(placement)
    vertical = align_list[0]
    horizontal = align_list[1]

    # Set horizontal coordinates and alignment
    if horizontal == "Left":
        hcoord = 10
        align1 = "l"
    elif horizontal == "Right":
        hcoord = width - 10
        align1 = "r"
    elif horizontal == "Middle":
        hcoord = width / 2
        align1 = "m"

    # Set vertical coordinates and alignment
    if vertical == "Top":
        vcoord = 10
        align2 = "t"
    elif vertical == "Bottom":
        vcoord = height - 10
        align2 = "b"
    elif vertical == "Middle":
        vcoord = height / 2
        align2 = "m"

    # Combine values into proper format for coordinates and alignment
    coords = (hcoord, vcoord)
    align = align1 + align2
    return coords, align


def save_image():

    # Convert PhotoImage to Image
    image = ImageTk.getimage(holder.wm_img)
    rgb_img = image.convert("RGB")

    # Allow user to name and save file in desired directory
    file_name = fd.asksaveasfilename()
    rgb_img.save(f"{file_name}.jpg")
    messagebox.showinfo(message="Your image has been saved.")


def reset():
    """Resets watermark settings"""
    holder.panel.destroy()
    holder.img = 0
    holder.wm_img = 0
    wm_entry.delete(0, END)
    font_box.current(0)
    size_slider.set(64)
    colour_box.current(0)
    opacity_slider.set(128)


# Create the interface

# Button to select photo
select_photo_btn = Button(widget_frame, text="Select a Photo", command=open_img)
select_photo_btn.grid(column=0, row=0, padx=XPAD, pady=YPAD, columnspan=2)

# Entry for watermark text
wm_label = Label(widget_frame, text="Enter Watermark Text: ")
wm_label.grid(column=0, row=2, padx=XPAD, pady=YPAD)

wm_entry = Entry(widget_frame, width=21)
wm_entry.grid(column=1, row=2, padx=XPAD, pady=YPAD)

# Combobox for font style
font_label = Label(widget_frame, text="Select font: ")
font_label.grid(column=0, row=3)

font_var = StringVar()
font_box = ttk.Combobox(widget_frame, textvariable=font_var, width=20)
font_box["values"] = ("Arial", "Times New Roman", "Comic Sans")
font_box.current(0)
font_box.state(["readonly"])
font_box.grid(column=1, row=3)

# Slider for font size
size_label = Label(widget_frame, text="Select font size: ")
size_label.grid(column=0, row=4, padx=XPAD, pady=YPAD)

size_slider = Scale(widget_frame, orient="horizontal", length=315, from_=1, to=128)
size_slider.grid(column=1, row=4, padx=XPAD, pady=YPAD)
size_slider.set(64)

# Combobox for font colour
colour_label = Label(widget_frame, text="Select font colour: ")
colour_label.grid(column=0, row=5, padx=XPAD, pady=YPAD)

colour_var = StringVar()
colour_box = ttk.Combobox(widget_frame, textvariable=colour_var, width=20)
colour_box["values"] = ("Black", "White")
colour_box.current(0)
colour_box.state(["readonly"])
colour_box.grid(column=1, row=5, padx=XPAD, pady=YPAD)

# Slider for font opacity
opacity_label = Label(widget_frame, text="Select opacity: ")
opacity_label.grid(column=0, row=6, padx=XPAD, pady=YPAD)

opacity_slider = Scale(widget_frame, orient="horizontal", length=315, from_=1, to=255)
opacity_slider.grid(column=1, row=6, padx=XPAD, pady=YPAD)
opacity_slider.set(128)

# Combobox for text alignment
align_label = Label(widget_frame, text="Select placement: ")
align_label.grid(column=0, row=7, padx=XPAD, pady=YPAD)

align_var = StringVar()
align_box = ttk.Combobox(widget_frame, textvariable=align_var, width=20)
align_box["values"] = ("Top Left", "Top Middle", "Top Right", "Middle Left", "Middle Middle", "Middle Right",
                       "Bottom Left", "Bottom Middle", "Bottom Right")
align_box.current(0)
align_box.state(["readonly"])
align_box.grid(column=1, row=7, padx=XPAD, pady=YPAD)

# Button to apply watermark
wm_button = Button(widget_frame, text="Apply", command=apply_wm)
wm_button.grid(column=0, row=8, padx=XPAD, pady=YPAD, columnspan=2)

# Button to download watermarked image
save_button = Button(widget_frame, text="Save Image", command=save_image)
save_button.grid(column=0, row=9, padx=XPAD, pady=YPAD, columnspan=2)

# Button to reset watermark settings
reset_button = Button(widget_frame, text="Start Over", command=reset)
reset_button.grid(column=0, row=10, padx=XPAD, pady=YPAD, columnspan=2)

window.mainloop()
