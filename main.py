from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

csv_file = ""

def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(title="Select the exported csv file", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        csv_file = f"\"{file_path}\""
        print(f"Selected File: {csv_file}")
        listbox.insert(2, f"Selected File: {csv_file}")

def calc(movie_url):
    try:
        response = requests.get(movie_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = str(soup.find_all(class_="text-link text-footer"))   

        tokens = text.split(" ")
        time_token = tokens[2]
        digit_buffer = ""
        for character in time_token:
            if character.isnumeric():
                digit_buffer += character

        return int(digit_buffer)
    
    except:
        return 0

def calculate_watch_time(file_address):
    df = pd.read_csv(file_address)
    f = open("export.txt", "w")
    error_log = open("errors.log","w")
    counter = 0
    total_minutes = 0

    for url in df['Letterboxd URI']:
        time.sleep(2)
        movie_time = calc(url)
        total_minutes += movie_time
        print(df['Name'][counter] + " : " + str(movie_time) + " minutes")

        if movie_time == 0:
            error_string = "Error in : " + df['Name'][counter] + " - " + url + "\n"
            error_log.write(error_string)
            listbox.insert(counter + 2, error_string)
        else:
            output_string = df['Name'][counter] + " : " + str(movie_time) + " minutes\n"
            f.write(output_string)
            listbox.insert(counter + 2,  output_string)

        counter += 1

    f.write(f"\nTotal movie watchtime in minutes : {total_minutes}\n")
    f.write(f"Total movie watchtime in hours : {total_minutes / 60}\n")
    listbox2.insert(2, f"Total movie watchtime in minutes : {total_minutes}\n")
    listbox2.insert(3, f"Total movie watchtime in hours : {total_minutes / 60}\n")

    f.close()
    error_log.close()
    messagebox.showinfo("Success", "Done Processing") 

def executor():
    print("file path : " + file_path)
    calculate_watch_time(file_path)


def main():
    screen = Tk()
    screen.geometry("784x600")
    screen.title("Leterboxd Time Calculator")
    screen.resizable(False,False)
    screen.configure(bg="#ffffff")
    #screen.iconbitmap(r'./image.ico')

    Label(text="LetterBoxd Watch Time Calculator",fg="black",font=("Comic Sans MS",24)).place(x=125,y=35)
    Label(text="Input File : ",fg="black",font=("Comic Sans MS",16)).place(x=250,y=150)
    Button(text="Browse",height="2",width="23",bg="#000000",fg="white",bd=0,command=open_file_dialog).place(x=405,y=150)
    global listbox
    listbox = Listbox(screen, height="20",width="60")
    listbox.insert(1, 'Process Log:')
    listbox.place(x = 14, y = 205)
    global listbox2
    listbox2 = Listbox(screen,height="20",width="60")
    listbox2.insert(1, 'Overall Stats:')
    listbox2.place(x = 405, y = 205)

    Button(text="Calculate",height="2",width="18",bg="#000000",fg="white",bd=0,command=executor).place(x=325,y=548)

    screen.mainloop()


main()