from tkinter import *
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time

colour='#5cdb95'

root = Tk()
root.geometry('500x300')
root.resizable(0,0)
# root.iconbitmap('icon.ico')
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
# Label(root, text="Put the link here", font='Helvetica 14 bold', bg=colour).place(x=150, y=55)

def temp_text(e):
   link_enter.delete(0,"end")

link_enter = Entry(root, width=70, textvariable=link)
link_enter.insert(0, "Put the link Here")
link_enter.place(x=30, y=85)
link_enter.bind("<FocusIn>",temp_text)
display_size= Label(root, text="")
message = Label(root, text= "", font="arial 15")

def download():
    url = YouTube(str(link.get()))
    
    if(res.get()!="Select"):
        video = url.streams.get_by_itag(itag[res.get()])
        video.download() 
        message.config(text="Downloaded")
        message.place(relx=0.5, y=200, anchor=CENTER)
    
    elif(sub_sel.get()!="Select"):
        caption=url.captions[sub_code[sub_sel.get()]]
        caption.download(url.title,True)
        message.config(text="Downloaded")
        message.place(relx=0.5, y=200, anchor=CENTER)
    
    else:
        message.config(text="Please select a resolution/subtitle first")
        message.place(relx=0.5, y=200, anchor=CENTER)
    
def f_size(*args):
    display_size.config(text = str(round(res_size[res.get()]/pow(1024,2) , 2)) + " MB" , font="arial 8")
    display_size.place(x=200, y=110) 
    message.place_forget()
    # display_size= Label(root, text= str(round(res_size[res.get()]/pow(1024,2) , 2)) + " MB" , font="arial 8").place(x=160, y=110) 
    
res.trace("w", f_size)
    
def get_res():
    res_temp=[]
    bitrate_temp=[]
    url = YouTube(str(link.get()))
    message.place_forget()
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
    
    img_url=url.thumbnail_url
    response=requests.get(img_url)

    global img
    img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((120,80),Image.ANTIALIAS))
    tb=Label(root, image=img).place(relx=0.5, y=175, anchor=CENTER)
    
    Label(root, text=url.title, font='times 12 bold', bg=colour, fg='#05386b').place(relx=0.5, y=225, anchor=CENTER)
    drop = OptionMenu( root , res , *diplay_list ).place(x=30, y=105)
    

def get_sub():
    sub_list=[]
    url = YouTube(str(link.get()))
    sub=url.captions
    
    for caption in sub:
        sub_list.append(caption.name)
        sub_code.update({caption.name:caption.code})
    
    
    
    
    if(len(sub_list)==0):
        message.config(text="No subtitle found!")
        message.place(relx=0.5, y=200, anchor=CENTER)
    else:
        img_url=url.thumbnail_url
        response=requests.get(img_url)

        global img
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((120,80),Image.ANTIALIAS))
        tb=Label(root, image=img).place(relx=0.5, y=175, anchor=CENTER)

        Label(root, text=url.title, font='times 12 bold', bg=colour, fg='#05386b').place(relx=0.5, y=225, anchor=CENTER)
        OptionMenu( root , sub_sel , *sub_list ).place(x=30, y=105)
    
Button(root, text='Download', font='san-serif 15 bold', bg='#05386b', fg='white', padx=2,command=download).place(x=15, y=240)
Button(root, text='Get Resolutions', font='san-serif 15 bold', bg='#05386b', fg='white', padx=2,command=get_res).place(x=150, y=240)
Button(root, text='Get Subtitles', font='san-serif 15 bold', bg='#05386b', fg='white', padx=2,command=get_sub).place(x=350, y=240)
    

# res_temp=[]    
# url = YouTube(str("https://www.youtube.com/watch?v=BD_Euf_CBbs"))
# for i in url.streams:
#     if(i.is_progressive):
        # print(i)
# c=url.captions['en']
# # c
# c.download('',True)
# caption=''
# for ca in c:
#     print(ca.name)
# print(caption)
# print(c.xml_captions)
# print(c.get_by_language_code(caption))
# c.xml_captions
# url.thumbnail_url.split('?')[0]
# for stream in url.streams:
#     if(stream.resolution!=None):
#         x=int(stream.resolution.replace('p',''))
#         if(x not in res_temp):
#             res_temp.append(x)
#             itag.update({str(x)+'p':stream.itag})
# res_temp.sort()
# for i in url.streams.filter(only_audio=True):
#     print(i)
    
# for t_res in res_temp:
#     x=str(t_res)+'p'
#     res_list.append(x)
# # itag[res_list[5]]
# res_list

root.mainloop()