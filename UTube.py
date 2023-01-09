from tkinter import *
from tkinter import messagebox
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time

colour='#5cdb95'

root = Tk()
root.geometry('500x300')
root.resizable(0,0)

try:
    root.iconbitmap('icon.ico')
except:
    pass

root.title('Youtube Downloader SE Project')
root.configure(background=colour)

Label(root, text="SE Project - Youtube Video Downloader", font='times 17 bold', bg=colour, fg='#05386b').place(x=40,y=20)


link = StringVar()
res = StringVar()
sub_sel = StringVar()
res.set("Select")
sub_sel.set("Select")

itag={}
res_size={}
sub_code={}
u_link=""

def temp_text(e):
   link_enter.delete(0,"end")

link_enter = Entry(root, width=70, textvariable=link)
link_enter.insert(0, "Put the link Here")
link_enter.place(x=30, y=85)
link_enter.bind("<FocusIn>",temp_text)
display_size= Label(root, text="")
message = Label(root, text= "", font="arial 15")
tb = Label(root)
tit=Label(root, font='times 12 bold', bg=colour, fg='#05386b')
dropr = OptionMenu( root , res , None )
drops = OptionMenu( root , sub_sel , None )
clear_butt= Button(root, text='Clear', font='san-serif 15 bold', bg='#05386b', fg='white', padx=2)

def clear():
    global u_link
    res.set("Select")
    sub_sel.set("Select")
    itag={}
    res_size={}
    sub_code={}
    u_link=""
    link_enter.place(x=30, y=85)
    tb.place_forget()
    tit.place_forget()
    display_size.place_forget()
    clear_butt.place_forget()
    dropr.place_forget()
    drops.place_forget()
    
    
clear_butt.config(command=clear)

def download():
    global u_link
    if(u_link==""):
        u_link=str(link.get())
    
    link_enter.delete(0,"end")
    try:
        url = YouTube(u_link)

        if(res.get()!="Select"):
            video = url.streams.get_by_itag(itag[res.get()])
            video.download() 
            messagebox.showinfo("Done", "Downloaded")

        elif(sub_sel.get()!="Select"):
            caption=url.captions[sub_code[sub_sel.get()]]
            caption.download(url.title,True)
            messagebox.showinfo("Done", "Downloaded")

        else:
            messagebox.showerror("Error", "Please select a resolution/subtitle first")
    
    except:
        messagebox.showerror("Error", "Please enter a valid YouTube link")
        clear()

        
def f_size(*args):
    if(res.get()!="Select"):
        display_size.config(text = str(round(res_size[res.get()]/pow(1024,2) , 2)) + " MB" , font="arial 8")
        display_size.place(x=200, y=110) 
        message.place_forget()
    
res.trace("w", f_size)
    
def get_res():
    res_temp=[]
    bitrate_temp=[]
    global u_link
    if(u_link==""):
        u_link=str(link.get())
    
    link_enter.delete(0,"end")
    try:
        url = YouTube(u_link)
        link_enter.place_forget()
        clear_butt.place(relx=0.5, y=70, anchor=CENTER)
        message.place_forget()
        drops.place_forget()
        for stream in url.streams.filter(only_video=False):
            if(stream.resolution!=None):
                x=int(stream.resolution.replace('p',''))
                if(x<721 and stream.is_adaptive):
                    continue;
                if(x not in res_temp):
                    res_temp.append(x)
                    if(x<721):
                        itag.update({str(x)+'p':stream.itag})
                        res_size.update({str(x)+'p':stream.filesize})
                    else:
                        itag.update({str(x)+"p (No Audio)":stream.itag})
                        res_size.update({str(x)+"p (No Audio)":stream.filesize})

        for stream in url.streams.filter(only_audio=True):
            x=int(stream.abr.replace('kbps',''))
            if(x not in bitrate_temp):
                bitrate_temp.append(x)
                itag.update({str(x)+'kbps (Only Audio)':stream.itag})
                res_size.update({str(x)+'kbps (Only Audio)':stream.filesize})


        res_temp.sort()
        bitrate_temp.sort()
        res_list=[]
        bitrate_list=[]

        for t_res in res_temp:
            if(t_res<721):
                x=str(t_res)+'p'
                res_list.append(x)
            else:
                x=str(t_res)+"p (No Audio)"
                res_list.append(x)

        for t_abr in bitrate_temp:
            x=str(t_abr)+'kbps (Only Audio)'
            bitrate_list.append(x)

        diplay_list=[]

        diplay_list.extend(res_list)
        diplay_list.extend(bitrate_list)

        menu = dropr["menu"]
        menu.delete(0, "end")
        for string in diplay_list:
            menu.add_command(label=string, command=lambda value=string: res.set(value))
        res.set("Select")
        dropr.place(x=30, y=105)

        img_url=url.thumbnail_url
        response=requests.get(img_url)

        global img
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((120,80),Image.ANTIALIAS))
        tb.config(image=img)
        tb.place(relx=0.5, y=175, anchor=CENTER)

        tit.config(text=url.title)
        tit.place(relx=0.5, y=225, anchor=CENTER)
        
    except:
        messagebox.showerror("Error", "Please enter a valid YouTube link")
        clear()

def get_sub():
    display_size.place_forget()
    
    
    global u_link
    if(u_link==""):
        u_link=str(link.get())
    
    link_enter.delete(0,"end")
    sub_list=[]
    try:
        url = YouTube(u_link)
        link_enter.place_forget()
        clear_butt.place(relx=0.5, y=70, anchor=CENTER)
        dropr.place_forget()
        sub=url.captions

        for caption in sub:
            sub_list.append(caption.name)
            sub_code.update({caption.name:caption.code})

        img_url=url.thumbnail_url
        response=requests.get(img_url)
        global img
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((120,80),Image.ANTIALIAS))
        tb.config(image=img)
        tb.place(relx=0.5, y=175, anchor=CENTER)

        tit.config(text=url.title)
        tit.place(relx=0.5, y=225, anchor=CENTER)


        if(len(sub_list)==0):
            messagebox.showerror("Error", "No Subtitle Found")
        else:
            menu = drops["menu"]
            menu.delete(0, "end")
            for string in sub_list:
                menu.add_command(label=string, command=lambda value=string: sub_sel.set(value))
            sub_sel.set("Select")
            drops.place(x=30, y=105)
    except:
        messagebox.showerror("Error", "Please enter a valid YouTube link")
        clear()
Button(root, text='Download', font='san-serif 15 bold', bg='#05386b', fg='white', padx=2,command=download).place(x=15, y=240)
Button(root, text='Get Resolutions', font='san-serif 15 bold', bg='#05386b', fg='white', padx=2,command=get_res).place(x=150, y=240)
Button(root, text='Get Subtitles', font='san-serif 15 bold', bg='#05386b', fg='white', padx=2,command=get_sub).place(x=350, y=240)

root.mainloop()