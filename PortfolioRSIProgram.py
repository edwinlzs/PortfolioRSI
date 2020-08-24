import tkinter as tk
from FunctionDefinitions.run_portfolio_rsi_program import run_portfolio_rsi_program

# create window that houses GUI widgets
window = tk.Tk()

# label widgets for GUI
frm_lbl_filename = tk.Frame()
lbl_filename = tk.Label(
    text="Name of Excel file to extract tickers from:",
    master=frm_lbl_filename
    )

frm_lbl_years = tk.Frame()
lbl_years = tk.Label(
    text="Years of data:",
    master=frm_lbl_years
    )

# user entry field widgets for GUI
frm_ent_filename = tk.Frame()
ent_filename = tk.Entry(master=frm_ent_filename)

frm_ent_years = tk.Frame()
ent_years = tk.Entry(master=frm_ent_years)


# button widgets for GUI
frm_btn_run = tk.Frame(
    master=window,
    relief="raised",
    borderwidth=3
    )
btn_run = tk.Button(
    text="Run extraction",
    bg="black",
    fg="white",
    master=frm_btn_run
    )

# pack widgets to make them visible
# pack in the order of display

frm_lbl_filename.grid(row=1,column=0,padx=3,pady=10)
lbl_filename.pack()

frm_ent_filename.grid(row=1,column=1,padx=7,pady=10)
ent_filename.pack()

frm_lbl_years.grid(row=2,column=0,padx=3,pady=10,sticky='e')
lbl_years.pack()

frm_ent_years.grid(row=2,column=1,padx=7,pady=10)
ent_years.pack()

frm_btn_run.grid(row=3,column=1,columnspan=2)
btn_run.grid(row=3,column=1,sticky="nsew")


# prepare events
events_list = []

# create run button press event handler
def btn_run_click(event):
    # submit
    # print("the button was clicked")
    filename = ent_filename.get()
    years = int(ent_years.get())
    run_portfolio_rsi_program(filename, years)
    

# Bind button press event to btn_run_press()
btn_run.bind("<Button-1>", btn_run_click)
    
# run Tkinter event loop, making it listen for events
window.mainloop()

