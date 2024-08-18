import customtkinter
from customtkinter import filedialog
from pathlib import Path
from PIL import Image
from time import sleep
import ffmpeg
import os, sys


# Function to load images on exe file (More compatibility with the auto-py-to-exe)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Function to open file selector dialog
def selectFile(app):
    file_selector = filedialog.askopenfilename()
    app.entry.delete(0, customtkinter.END)  # Clear the entry
    app.entry.insert(0, file_selector)  # Display selected file in the entry
    app.selected_file = file_selector  # Store the selected file path in the app instance
    app.label.configure(text="Press the button to start")


# Convert selected video to PSP format
def convertVideo(app):

    app.label.configure(text="File is being converted...")

    sleep(2)

    input_video = app.selected_file
    output_video = os.path.splitext(input_video)[0] + "_psp.mp4"
    
    (
        ffmpeg
        .input(input_video)
        .filter("fps", fps=29.97, round="up")
        .filter("scale", 320, 240)
        .output(
            output_video,
            vcodec="mpeg4",
            video_bitrate="672k",
            acodec="aac",
            ar="24000",
            audio_bitrate="128k",
            movflags="faststart",
            strict="experimental",
            map="0:a"
        )
        .run()
    )

    app.label.configure(text="Conversion done!")
    print(f"Converted file saved as: {output_video}")


# CustomTkinter GUI
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("450x320")
        self.title("PSP Video Converter")
        self.iconbitmap(resource_path("assets/icon.ico"))

        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="", width=300)
        self.entry.grid(row=0, column=0, padx=30, pady=50)

        image_button = customtkinter.CTkImage(Image.open(resource_path("assets/folder.png")))

        self.file_button = customtkinter.CTkButton(master=self, text="", width=50, image=image_button, fg_color="#2E4057", command=lambda: selectFile(self))
        self.file_button.grid(row=0, column=1, pady=50)

        self.label = customtkinter.CTkLabel(master=self, text="Select a file to convert", font=("Arial", 18, "bold"))
        self.label.grid(row=1, column=0, columnspan=2, sticky="n")

        self.start_button = customtkinter.CTkButton(master=self, text="Convert", font=("Arial", 30), width=200, height=100, fg_color="#2E4057", command=lambda: convertVideo(self))
        self.start_button.grid(row=1, column=0, columnspan=2, pady=50, sticky="n")

        self.selected_file = ""
        

customtkinter.set_appearance_mode("dark")
app = App()
app.mainloop()
