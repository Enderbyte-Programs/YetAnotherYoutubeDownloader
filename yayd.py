try:
    import pyi_splash
except:
    __compiled = False
else:
    __compiled = True
    pyi_splash.update_text("Enderbyte Programs")
import pytube
from tkinter import IntVar, StringVar, ttk,messagebox,Tk
from tkinter.constants import *
from tkinter import filedialog
import os
import subprocess
import sys
import sv_ttk

try:
    rsz = subprocess.run(["ffmpeg","--help"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if rsz.returncode != 0:
        HFMMPG = False
    else:
        HFMMPG = True
except:
    HFMMPG = False
try:
    print(HFMMPG)
    """
    installfm = False
    if not HFMMPG:
        if __compiled:
            pyi_splash.close()
        if messagebox.askyesno("Question","FFmpeg is not installed. Would you like to install it now?"):# uncomment when ffmpeg implemented
            installfm = True
    ISOP = False
    """

    root = Tk()
    def saq():
        try:
            global ISOP
            if not ISOP:
                os.system("taskkill /f /pid "+str(os.getpid()))#Forcibly stopping all threads
                sys.exit()
            else:
                if messagebox.askyesno("YAYD","Are you sure you want to quit? An operation is still running. Quitting now will corrupt the downloads."):
                    os.system("taskkill /f /pid "+str(os.getpid()))#Forcibly stopping all threads
                    sys.exit()
        except:
            sys.exit()
    root.wm_protocol("WM_DELETE_WINDOW",saq)
    root.title("Youtube Downloader")
    sv_ttk.set_theme("dark")
    if __compiled:
        root.wm_iconbitmap("yayd.exe")
    else:
        try:
            root.wm_iconbitmap("ep.ico")
        except:
            pass
    root.geometry("500x500")
    ent = ttk.Entry(root,width=50)
    def dnl(audio=False):
        global root
        global ent
        global t0
        global b0
        global opmen
        global rb0v
        global ISOP
        ISOP = True
        dat = ent.get()
        def progress_function(stream, chunk, bytes_remaining):
            global pbar
            global t0
            size = stream.filesize
            print(size)
            print(bytes_remaining)
            pbar["mode"] = "determinate"
            pbar["maximum"] = size
            pbar["value"] = size - bytes_remaining
            t0["text"] = f"Downloading... {round((size - bytes_remaining)/size*100)}%"
            root.update()
            root.update_idletasks()
        b0["state"] = "disabled"
        b1["state"] = "disabled"
        opmen["state"] = "disabled"
        global pbar
        pbar = ttk.Progressbar(root,mode="indeterminate",length=500)
        pbar.pack(fill=X)
        t0 = ttk.Label(root,text="Preparing...")
        t0.pack()
        root.update()
        root.update_idletasks()
        try:
            y = pytube.YouTube(dat,on_progress_callback=progress_function)
        except:
            messagebox.showerror("YAYD","Invalid URL")
            t0.destroy()
            pbar.destroy()
            b0["state"] = "normal"
            b1["state"] = "normal"
            opmen["state"] = "normal"
            ISOP = False
            return
        print(rb0v.get())
        if not audio and int(rb0v.get()) != 1:
            stream = y.streams.get_highest_resolution()
        elif not audio and int(rb0v.get()) == 1:
            print("dlr")
            stream = y.streams.get_lowest_resolution()
        elif audio:
            stream = y.streams.get_audio_only()
        if not audio:
            file = filedialog.asksaveasfilename(filetypes=[(".mp4 Video","*.mp4")])
        else:
            file = filedialog.asksaveasfilename(filetypes=[(".mp3 Audio","*.mp3")])
        print(file)
        if file is None or file == "":
            t0.destroy()
            pbar.destroy()
            b0["state"] = "normal"
            b1["state"] = "normal"
            opmen["state"] = "normal"
            ISOP = False
            return
        try:
            os.remove(file)
        except:
            pass
        stream.download(filename=file)
        messagebox.showinfo("YAYD",f"Your video \"{y.title}\" has finished downloading!")
        pbar.destroy()
        t0.destroy()
        b0["state"] = "normal"
        b1["state"] = "normal"
        opmen["state"] = "normal"
        ISOP = False
    
    mltext = ttk.Label(root,text="Url of video")
    mltext.pack()
    b0 = ttk.Button(root,text="Download Video",command=dnl)
    b1 = ttk.Button(root,text="Download Audio",command=lambda: dnl(True))
    ttk.Button(root,text="Quit",command=saq).pack(side=BOTTOM,pady=5)
    ent.pack(pady=5,fill=X)
    b0.pack(pady=5)
    b1.pack(pady=5)
    olist = ["Video","Video","Playlist","Channel"]
    olist = [" "*10+i+" "*10 for i in olist]
    vl = StringVar(root)
    rb0v = IntVar(root)
    rb0 = ttk.Checkbutton(root,variable=rb0v,onvalue=1,offvalue=0,text="Prefer smaller file size")
    rb0.pack()
    rb1v = IntVar(root,value=3)
    rb1 = ttk.Checkbutton(root,variable=rb1v,onvalue=1,offvalue=0,text="Concatenate files")
    rb2v = IntVar(root,value=1)
    rb2 = ttk.Checkbutton(root,variable=rb2v,onvalue=1,offvalue=0,text="Remove extra files")
    rb3 = ttk.Checkbutton(root,variable=rb1v,onvalue=2,offvalue=0,text="Create clip compilation")#NOTE shared variable to ensure only one is checked
    rb4 = ttk.Checkbutton(root,variable=rb1v,onvalue=3,offvalue=0,text="Download with video name")
    rb1["state"] = "disabled"
    rb3["state"] = "disabled"#REMOVE WHEN FEATURE IMPLEMENTED
    def __odo(event):
        global b1
        global b0
        global mltext
        dat = vl.get()
        dat = dat.replace(" ","")
        if dat == "Playlist":
            b1["text"] = "Download all audio"
            b0["text"] = "Download all video"
            mltext["text"] = "Playlist URL"
            b0.config(command=lambda: dnlp(False,False))
            b1.config(command=lambda: dnlp(False,True))
            rb1.pack()
            rb2.pack()
            rb3.pack()
            rb4.pack()
        elif dat == "Channel":
            b1["text"] = "Download all audio"
            b0["text"] = "Download all video"
            mltext["text"] = "Channel URL"
            b0.config(command=lambda: dnlp(True,False))
            b1.config(command=lambda: dnlp(True,True))
            rb1.pack()
            rb2.pack()
            rb3.pack()
            rb4.pack()
        else:
            b1["text"] = "Download audio"
            b0["text"] = "Download video"
            mltext["text"] = "Channel URL"
            rb1.pack_forget()
            rb2.pack_forget()
            rb3.pack_forget()
            rb4.pack_forget()
        
    opmen = ttk.OptionMenu(root,vl,*olist,command=__odo)
    opmen.pack(side=BOTTOM,pady=5)
    def dnlp(channel=False,audio=False,preferfname=False):
        global root
        global ent
        global t0
        global b0
        global opmen
        global rb0v
        global rb1v
        global rb2v
        global ISOP
        ISOP = True
        dat = ent.get()
        __plen = 3
        if rb2v.get() == 1:
            __plen += 1
        if rb1v.get() == 1:
            __plen += 2
        elif rb1v.get() == 2:
            __plen += 3
        elif rb1v.get() == 3:
            preferfname = True
        def progress_function(stream, chunk, bytes_remaining):
            global pbar
            global t0
            size = stream.filesize
            print(size)
            print(bytes_remaining)
            pbar["mode"] = "determinate"
            pbar["maximum"] = size
            pbar["value"] = size - bytes_remaining
            t0["text"] = f"Downloading... {round((size - bytes_remaining)/size*100)}%"
            root.update()
            root.update_idletasks()
        b0["state"] = "disabled"
        b1["state"] = "disabled"
        opmen["state"] = "disabled"
        global pbar
        pbarm = ttk.Progressbar(root,mode="determinate",length=500,maximum=__plen)
        pbarm.pack(fill=X)
        t1 = ttk.Label(root,text="Preparing...")
        t1.pack()
        pbard = ttk.Progressbar(root,mode="indeterminate",length=500)
        pbard.pack(fill=X)
        t2 = ttk.Label(root,text="Preparing...")
        t2.pack()
        pbar = ttk.Progressbar(root,mode="indeterminate",length=500)
        pbar.pack(fill=X)
        t0 = ttk.Label(root,text="Preparing...")
        t0.pack()
        root.update()
        root.update_idletasks()
        if not channel:
            try:
                y = pytube.Playlist(dat)
            except:
                messagebox.showerror("YAYD","Invalid URL")
                t0.destroy()
                pbar.destroy()
                pbarm.destroy()
                pbard.destroy()
                t1.destroy()
                t2.destroy()
                b0["state"] = "normal"
                b1["state"] = "normal"
                opmen["state"] = "normal"
                ISOP = False
                return
        else:
            try:
                y = pytube.Channel(dat)
            except:
                messagebox.showerror("YAYD","Invalid URL")
                t0.destroy()
                pbar.destroy()
                pbarm.destroy()
                pbard.destroy()
                t1.destroy()
                t2.destroy()
                b0["state"] = "normal"
                b1["state"] = "normal"
                opmen["state"] = "normal"
                ISOP = False
                return
        print(rb0v.get())
        if not audio and int(rb0v.get()) != 1:
            savesize = False
        elif not audio and int(rb0v.get()) == 1:
            print("dlr")
            savesize = True
        elif audio:
            ua = True

        file = filedialog.askdirectory()
        print(file)
        if file is None or file == "":
            t0.destroy()
            pbar.destroy()
            pbarm.destroy()
            pbard.destroy()
            t1.destroy()
            t2.destroy()
            b0["state"] = "normal"
            b1["state"] = "normal"
            opmen["state"] = "normal"
            ISOP = False
            return
        if os.path.isfile("output.mp4") or os.path.isfile("vid_0.mp4") or os.path.isfile("vid_0s.mp4"):
            if not messagebox.askyesno("Some files needed files already exist. May we overwrite them?"):
                t0.destroy()
                pbar.destroy()
                pbarm.destroy()
                pbard.destroy()
                t1.destroy()
                t2.destroy()
                b0["state"] = "normal"
                b1["state"] = "normal"
                opmen["state"] = "normal"
                ISOP = False
                return 
        pbarm["value"] += 1
        t1["text"] = "Downloading"
        pbard["mode"] = "determinate"
        pbard["maximum"] = len(y.video_urls)
        vinc = 0
        for video in y.video_urls:
            pbard["value"] += 1
            v = pytube.YouTube(video,on_progress_callback=progress_function)
            if savesize and not audio:
                stream = v.streams.get_lowest_resolution()
            elif not savesize and not audio:
                stream = v.streams.get_highest_resolution()
            elif audio:
                stream = v.streams.get_audio_only()
            t2["text"] = v.title
            if not preferfname:
                if os.path.isfile(file+f"\\vid_{vinc}.mp4"):
                    os.remove(file+f"\\vid_{vinc}.mp4")
                stream.download(filename=file+f"\\vid_{vinc}.mp4")
                vinc += 1
            else:
                try:
                    if os.path.isfile(file+f"\\{v.title}.mp4"):
                        os.remove(file+f"\\{v.title}.mp4")
                    stream.download(filename=file+f"\\{v.title}.mp4")
                except Exception as r:
                    print(r)
                    if os.path.isfile(file+f"\\vid_{vinc}.mp4"):
                        os.remove(file+f"\\vid_{vinc}.mp4")
                    stream.download(filename=file+f"\\vid_{vinc}.mp4")
                vinc += 1
        
        if rb2v == 1:
            pbarm["value"] += 1
            t1["text"] = "Cleaning up"
            root.update()
            root.update_idletasks()
            if rb1v != 0:
                pass#TODO add cleanup for ffmpeg stuff
        pbarm["value"] = pbarm["maximum"]
        t1["text"] = "All Done!"
        root.update()
        root.update_idletasks()
        if not channel:
            messagebox.showinfo("YAYD",f"Your Playlist \"{y.title}\" has finished downloading!")
        else:
            messagebox.showinfo("YAYD",f"The contents of channel \"{y.channel_name}\" have finished downloading")
        t0.destroy()
        pbar.destroy()
        pbarm.destroy()
        pbard.destroy()
        t1.destroy()
        t2.destroy()
        b0["state"] = "normal"
        b1["state"] = "normal"
        opmen["state"] = "normal"
        ISOP = False
    if __compiled:
        pyi_splash.close()
    root.mainloop()
except Exception as e:
    messagebox.showerror("Error",e)