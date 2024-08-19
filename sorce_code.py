# imports
import requests
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import io
import threading
import time
import random

# api url
base_url = 'https://pokeapi.co/api/v2/'

# window
theme = 'united'
window = ttk.Window(themename=theme)
window.geometry('510x300')
window.title('Pokemon Viewer by jamu441')

# variables
name_variable = ttk.StringVar()
name_variable.set('Name')
id_variable = ttk.StringVar()
id_variable.set('ID')
tips_var = ttk.StringVar()
default = ttk.StringVar()
default.set('Bulbasaur')

# widgets
top_frame = ttk.LabelFrame(master=window, style='primary', text='Enter Pokemon')
top_frame.pack(side='top', ipadx=500, padx=5, pady=5)

bottom_frame = ttk.LabelFrame(master=window, style='warning', text='Pokemon Data')
bottom_frame.pack(ipadx=500, ipady=200, padx=5, pady=5)

bottom_frame1 = ttk.LabelFrame(master=window, style='success', text='Pokemon Stats')
bottom_frame1.place(x=365, y=90)

bottom_frame2 = ttk.LabelFrame(master=window, style='warning', text='Pokemon Abilities')
bottom_frame2.place(x=165, y=90)

bottom_frame3 = ttk.LabelFrame(master=window, style='info', text='Pokemon Type')
bottom_frame3.place(x=165, y=170)

bottom_frame4 = ttk.LabelFrame(master=window, style='danger', text='Misc')
bottom_frame4.place(x=277, y=170)

bottom_frame5 = ttk.LabelFrame(master=window, style='warning', text='Appearance')
bottom_frame5.place(x=15, y=240)

bottom_frame6 = ttk.LabelFrame(master=window, style='info', text='Extra')
bottom_frame6.place(x=165, y=253)

info_label = ttk.Label(master=bottom_frame6, textvariable=tips_var)
info_label.grid(row=0, column=0)

photo_frame1 = ttk.Frame(master=window)
photo_frame1.place(x=25, y=130)

photo_frame2 = ttk.Frame(master=window)
photo_frame2.place(x=25, y=130)

image_data = Image.open('pokeball.png')
imagetk = ImageTk.PhotoImage(image_data)

photo_label = ttk.Label(master=window, image=imagetk)
photo_label.place(x=460, y=253)

photo_label.image = imagetk

pokemon_entry = ttk.Entry(master=top_frame, style='primary', font='Arial 14 bold', justify='center', foreground='#e95420', textvariable=default)
pokemon_entry.grid(row=0, column=0, padx=10, pady=5, ipadx=65)


def change_theme(event):
    window.style.theme_use('cyborg')
    pokemon_entry.configure(foreground='white')

def change_theme2(event):
    window.style.theme_use('united')
    pokemon_entry.configure(foreground='#e95420')

photo_label.bind('<Button-1>', change_theme)
photo_label.bind('<Button-3>', change_theme2)

name_label = ttk.Label(master=bottom_frame, textvariable=name_variable, font='Arial 16 bold')
name_label.grid(row=0, column=0, padx=5)

id_label = ttk.Label(master=bottom_frame, textvariable=id_variable, font='Arial 10')
id_label.grid(row=0, column=1)


# extras tips
def tip_switch():
    while True:
        tips = ['Made using https://pokeapi.co/', "You can also type ID's!", "Gotta Catch 'Em All!", "GET OUT", 'Hope you enjoy!', 'Made by jamu441', 'Click the Pokéball for Dark mode!']
        display_tip = random.choice(tips)
        if display_tip != tips_var:
            tips_var.set(display_tip)
            time.sleep(8)


t = threading.Thread(target=tip_switch)
t.start()


# get api dictionary
def pokemon_info(name):
    url = f'{base_url}pokemon/{name}'
    response = requests.get(url)
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        messagebox.showinfo('Error', f'Failed to get data error code {response.status_code}')


# Search dictionary for selected Pokémon
def search_pokemon():
    # setup
    amount = 0
    pokemon_name = pokemon_entry.get().lower()
    default.set(pokemon_name.capitalize())
    pokemon_dict = pokemon_info(pokemon_name)

    # delete all created widgets
    for widget in bottom_frame1.winfo_children():
        widget.destroy()
    for widget in bottom_frame2.winfo_children():
        widget.destroy()
    for widget in bottom_frame3.winfo_children():
        widget.destroy()
    for widget in bottom_frame4.winfo_children():
        widget.destroy()
    for widget in bottom_frame5.winfo_children():
        widget.destroy()
    for widget in photo_frame1.winfo_children():
        widget.destroy()
    for widget in photo_frame2.winfo_children():
        widget.destroy()

    # if data exists search for selected Pokémon data
    if pokemon_dict:
        name = pokemon_dict['name']
        poke_id = str(pokemon_dict['id'])
        id_variable.set('#'+poke_id)
        name_variable.set(name.capitalize())

        def toggle_normal():
            # display sprite of selected Pokémon
            for widget in photo_frame2.winfo_children():
                widget.destroy()
            for widget in photo_frame1.winfo_children():
                widget.destroy()
            photo_frame2.place_forget()
            photo_frame1.place(x=25, y=130)

            url = pokemon_dict['sprites']['front_default']
            response = requests.get(url)
            image_data = response.content

            image = Image.open(io.BytesIO(image_data))
            imagetk = ImageTk.PhotoImage(image)

            image_label = ttk.Label(master=photo_frame1, image=imagetk)
            image_label.Image = imagetk
            image_label.pack()
        toggle_normal()
        def toggle_shiny():
            # displays shiny sprite of selected Pokémon
            for widget in photo_frame2.winfo_children():
                widget.destroy()
            for widget in photo_frame1.winfo_children():
                widget.destroy()
            photo_frame1.place_forget()
            photo_frame2.place(x=25, y=130)

            shiny_url = pokemon_dict['sprites']['front_shiny']
            shiny_response = requests.get(shiny_url)
            shiny_image_data = shiny_response.content

            shiny_image = Image.open(io.BytesIO(shiny_image_data))
            shiny_imagetk = ImageTk.PhotoImage(shiny_image)

            shiny_image_label = ttk.Label(master=photo_frame2, image=shiny_imagetk)
            shiny_image_label.Image = shiny_imagetk
            shiny_image_label.pack()

        shiny_button = ttk.Button(master=bottom_frame5, text='Shiny', style='Warning, outline', command=toggle_shiny)
        shiny_button.grid(row=0, column=0, padx=2)

        normal_button = ttk.Button(master=bottom_frame5, text='Normal', style='Secondary, outline', command=toggle_normal)
        normal_button.grid(row=0, column=1, padx=2, pady=2)

        # Find and display Pokémon stats
        for key in pokemon_dict['stats']:
            amount += 1
            name = key['stat']['name']
            label = ttk.Label(master=bottom_frame1, text=name.capitalize()+' - '+str(key['base_stat']), font='Arial 9')
            label.grid(row=amount, column=2)

        # Find and display Pokémon abilities
        for key in pokemon_dict['abilities']:
            amount += 1
            name = key['ability']['name']
            label = ttk.Label(master=bottom_frame2, text='Ability '+name.capitalize() + ' - Hidden ' + str(key['is_hidden']), font='Arial 9')
            label.grid(row=amount, column=2)

        # Find and display Pokémon types
        for key in pokemon_dict['types']:
            amount += 1
            name = key['type']['name']
            label = ttk.Label(master=bottom_frame3, text='Type '+name.capitalize(), font='Arial 9')
            label.grid(row=amount, column=2)

        # Find misc info about the Pokémon
        label1 = ttk.Label(master=bottom_frame4, text='EXP - '+str(pokemon_dict['base_experience']), font='Arial 9')
        label1.grid(row=0, column=0)
        label2 = ttk.Label(master=bottom_frame4, text='Height - ' + str(pokemon_dict['height']), font='Arial 9')
        label2.grid(row=1, column=0)
        label3 = ttk.Label(master=bottom_frame4, text='Weight - ' + str(pokemon_dict['weight']), font='Arial 9')
        label3.grid(row=2, column=0)


# search button widget
find_button = ttk.Button(master=top_frame, text='Search', command=search_pokemon)
find_button.grid(row=0, column=1, ipadx=20, padx=3)


if window.winfo_exists():
    search_pokemon()
else:
    pass
# run
window.mainloop()
