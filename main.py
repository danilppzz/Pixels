#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import colorsys

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixels")
        self.root.iconbitmap("icon.ico")
        self.root.geometry("600x400")

        self.image_path = None
        self.original_image = None
        self.modified_image = None

        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.load_image)
        self.file_menu.add_command(label="Save", command=self.download_image)
        self.file_menu.add_command(label="Save As", command=self.save_as_image)

        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Change Color", command=self.select_color)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.label_image = tk.Label(root)
        self.label_image.pack(side="left", padx=10, pady=10)

        self.sidebar = tk.Frame(root, width=200)
        self.sidebar.pack(side="right", fill="y")

        self.brightness_label = tk.Label(self.sidebar, text="Brightness")
        self.brightness_label.pack(pady=5)
        self.brightness_slider = tk.Scale(self.sidebar, from_=0.0, to=2.0, orient="horizontal", resolution=0.1, command=self.adjust_brightness)
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack(pady=5)

        self.contrast_label = tk.Label(self.sidebar, text="Contrast")
        self.contrast_label.pack(pady=5)
        self.contrast_slider = tk.Scale(self.sidebar, from_=0.0, to=2.0, orient="horizontal", resolution=0.1, command=self.adjust_contrast)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(pady=5)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.original_image = Image.open(self.image_path).convert("RGBA")
            self.modified_image = self.original_image
            self.show_image(self.original_image)

    def show_image(self, image):
        min_width, min_height = 380, 380

        original_width, original_height = image.size

        if image.mode == 'RGBA':
            background_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
            background_image.paste(image, (0, 0), image)
            image = background_image

        if original_width < min_width or original_height < min_height:
            scale_factor = max(min_width // original_width, min_height // original_height)
            image_preview = image.resize((original_width * scale_factor, original_height * scale_factor),
                                         Image.Resampling.NEAREST)
        else:
            image_preview = image.resize((min_width, min_height), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(image_preview)
        self.label_image.config(image=img_tk)
        self.label_image.image = img_tk

    def adjust_brightness(self, value):
        if self.original_image:
            self.current_brightness = float(value)
            self.apply_adjustments()

    def adjust_contrast(self, value):
        if self.original_image:
            self.current_contrast = float(value)
            self.apply_adjustments()

    def select_color(self):
        if self.original_image is None:
            return

        selected_color = colorchooser.askcolor()[0]
        if selected_color:
            new_hue = self.rgb_to_hue(selected_color)
            self.current_hue = new_hue
            self.apply_adjustments()

    def apply_adjustments(self):
        modified_image = self.original_image

        if hasattr(self, 'current_hue'):
            modified_image = self.change_hue(modified_image, self.current_hue)

        if hasattr(self, 'current_brightness'):
            enhancer = ImageEnhance.Brightness(modified_image)
            modified_image = enhancer.enhance(self.current_brightness)

        if hasattr(self, 'current_contrast'):
            enhancer = ImageEnhance.Contrast(modified_image)
            modified_image = enhancer.enhance(self.current_contrast)

        self.modified_image = modified_image
        self.show_image(self.modified_image)

    def change_hue(self, image, new_hue):
        img_np = np.array(image.convert('RGBA')) / 255.0
        new_img_np = np.zeros_like(img_np)

        for i in range(img_np.shape[0]):
            for j in range(img_np.shape[1]):
                r, g, b, a = img_np[i, j]
                if a > 0:
                    h, s, v = colorsys.rgb_to_hsv(r, g, b)
                    new_rgb = colorsys.hsv_to_rgb(new_hue, s, v)
                    new_img_np[i, j] = (*new_rgb, a)

        new_image = Image.fromarray((new_img_np * 255).astype(np.uint8), 'RGBA')
        return new_image

    def rgb_to_hue(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        h, _, _ = colorsys.rgb_to_hsv(r, g, b)
        return h

    def download_image(self):
        if self.modified_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                self.modified_image.save(save_path)

    def save_as_image(self):
        if self.modified_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                self.modified_image.save(save_path)

    def show_about(self):
        messagebox.showinfo("About", "This is a simple image editor with basic features like brightness, contrast adjustment, and more.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
