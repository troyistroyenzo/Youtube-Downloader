from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube  # pip install pytube3
import time

Folder_Name = ""
fileSizeInBytes = 0
MaxFileSize = 0

# test = https://www.youtube.com/watch?v=PPaLdl8q4Gg

# file location


def openLocation():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    if(len(Folder_Name) > 1):
        locationError.config(text=Folder_Name, fg="white",
                             font=("Futura", 12, "bold"))
    else:
        locationError.config(text="Please Choose Folder!!", fg="red")

# Start viewing stream data


def start():
    GB = 100
    download = 0
    speed = 1
    while(download < GB):
        time.sleep(0.05)
        progressBar['value'] += (speed/GB)*100
        download += speed
        percent.set(str(int((download/GB)*100))+"%")
        #text.set(str(download)+"/"+str(GB)+" GB completed")
        root.update_idletasks()


#  Download video
def DownloadVideo():
    global MaxFileSize, fileSizeInBytes
    convertedChoice = ytdChoices.get()
    url = ytdEntry.get()
    start()
    if(len(url) > 1):
        ytdError.config(text="")
        yt = YouTube(url)

        if(convertedChoice == choices[0]):
            select = yt.streams.filter(progressive=True).first()

        elif(convertedChoice == choices[1]):
            select = yt.streams.filter(
                progressive=True, file_extension='mp4').last()

        elif(convertedChoice == choices[2]):
            select = yt.streams.filter(only_audio=True).first()

        fileSizeInBytes = select.filesize
        MaxFileSize = fileSizeInBytes/1024000
        MB = str(MaxFileSize) + " MB"
        print("File Size = {:00.00f} MB".format(MaxFileSize))
        # download function
        select.download(Folder_Name)
        complete()

    else:
        ytdError.config(text="Paste Link again!!", fg="red")

# Update Progress


def progress(stream=None, chunk=None, file_handle=None, remaining=None):
    # Gets the percentage of the file that has been downloaded.
    #nextLevel = Toplevel(root)
    percent = (100 * (fileSizeInBytes - remaining)) / fileSizeInBytes
    print("{:00.0f}% downloaded".format(percent))
    progressBar.config(text="Downloading...")

# Update To Completed


def complete():
    progressLabel.config(text=("Download Complete"))


# Root Settings
root = Tk()
root.title("PyTube - Media Downloader")
root.geometry("500x750")
root.columnconfigure(0, weight=1)
root.resizable(False, False)
root.configure(background="#002366")

percent = StringVar()
text = StringVar()

# NameLabel
ytdLabel = Label(root, text="Pytube Downloader",
                 background="#002366", fg="white", font=("Futura", 25, "bold"))
ytdLabel.grid(pady=10)

# Link Label
ytdLabel = Label(root, text="Enter Link",
                 background="#002366", fg="white", font=("Futura", 15, "bold"))
ytdLabel.grid(padx=20, pady=10, sticky=W)

# Entries
ytdEntryVar = StringVar()
ytdEntry = Entry(root, width=60, textvariable=ytdEntryVar)
ytdEntry.grid(padx=20, sticky=W, pady=10)


# Error
ytdError = Label(root, fg="red",
                 background="#002366", font=("Futura", 10))
ytdError.grid(pady=20, padx=20, sticky=W)

# Ask To Save
saveLabel = Label(root, text="Choose File Location",
                  background="#002366", fg="white", font=("Futura", 15, "bold"))
saveLabel.grid(padx=20, pady=7, sticky=W)

# Save
saveEntry = Button(root, width=10, bg="#008080", fg="white",
                   text="Choose Path", command=openLocation)
saveEntry.grid(pady=20, padx=20, sticky=W)

# Error Message
locationError = Label(root,
                      fg="red", background="#002366", font=("Futura", 10))
locationError.grid(pady=1, padx=20)

# Download Quality
ytdQuality = Label(root, text="Select Quality",
                   background="#002366", fg="white", font=("Futura", 15, "bold"))
ytdQuality.grid(pady=10, padx=20, sticky=W)

# Combo Box
choices = ["High Quality",  "Low Quality", "Audio Only", ]
ytdChoices = ttk.Combobox(root, values=choices)
ytdChoices.grid(pady=20, padx=20, sticky=W)

# Download Button
downloadBtn = Button(root, text="Download", width=10,
                     bg="#008080", fg="white", command=DownloadVideo)
downloadBtn.grid(pady=20, padx=20, sticky=W)

# Progressbar
progressBar = ttk.Progressbar(root, orient="horizontal",
                              length=200, mode='indeterminate')
progressBar.grid(pady=(1, 0), padx=0.1)
progressLabel = Label(root,
                      background="#002366", fg="white", font=("Futura", 15, "bold"))
progressLabel.grid(pady=10, padx=20, sticky=W)

# Developer Label
developerlabel = Label(root, text="TROY ENZO | 2021",
                       background="#002366", fg="white", font=("Futura", 7))
developerlabel.grid(pady=40)

root.mainloop()
