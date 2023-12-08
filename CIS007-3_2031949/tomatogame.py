import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import urllib.request
import io

class VegetableGame:
    API_URL = "http://marcconrad.com/uob/tomato/api.php"

    def __init__(self, root, player_name):
        self.root = root
        self.root.title("Vegetable Game")
        self.root.geometry("800x600+350+100")
        self.root.resizable(False, False)

        # Load background image
        background_image = Image.open("Game_screen.jpeg")
        self.background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Player information
        self.name = player_name
        self.score = 0
        self.timer_seconds = 60

        # Timer display
        self.timer_label = tk.Label(root, text=f'Time left: {self.timer_seconds} seconds', font=("times new Roman", 12))
        self.timer_label.place(x=350, y=50)

        # Timer initialization
        self.timer_id = None
        self.start_timer()

        # Displayed image
        self.imagelab = tk.Label(root)
        self.imagelab.place(x=70, y=100)

        # Logout button
        logout = tk.Button(root, text="Log Out", command=self.logout, cursor="hand2", font=(
            "Helvetica 15 underline"), bg="white", fg="red", activebackground="skyblue")
        logout.place(x=600, y=50, width=120)

        # Welcome message
        welcome_text = f'WELCOME {self.name}'
        title = tk.Label(root, text=welcome_text, font=("Impact", 25, "bold"), fg="red")
        title.place(x=100, y=50)

        # User answer entry
        self.answer = tk.Entry(root, font=("times new Roman", 14), bg="lightgray")
        self.answer.place(x=300, y=520, width=150, height=30)

        # Submit button
        result = tk.Button(root, text="Submit", cursor="hand2", command=lambda: self.check_answer(),
                           font=("times new Roman", 14), bg="White", fg="red")
        result.place(x=100, y=520, width=120)

        # Score display
        self.score_res = tk.Label(root, font=("times new Roman", 22))
        self.score_res.place(x=500, y=510)
        self.score_res.config(text=f'Score: {str(self.score)}')

        # Placeholder for the loaded image
        self.photo = None

        # Display the initial image
        self.show_image()

    def start_timer(self):
        # Update the timer display and schedule the next update
        if self.timer_seconds > 0:
            self.timer_label.config(text=f'Time left: {self.timer_seconds} seconds')
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            # If time is up, end the game
            self.timer_label.config(text='Time is up!')
            self.end_game()

    def end_game(self):
        # Display a message box to ask if the player wants to replay
        replay = messagebox.askyesno("Game Over", "Time is up! Do you want to play again?", parent=self.root)

        if replay:
            # Reset the game if the player chooses to replay
            self.score = 0
            self.score_res.config(text=f'Score: {str(self.score)}')
            self.timer_seconds = 60
            self.start_timer()
            self.show_image()
        else:
            # Log out if the player chooses not to replay
            self.logout()

    def show_image(self):
        # Fetch a new image and display it
        self.ques, self.soln = self.get_image()
        with urllib.request.urlopen(self.ques) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.photo = ImageTk.PhotoImage(image)
        self.imagelab.config(image=self.photo)
        self.imagelab.image = self.photo
        self.imagelab.update()

    def logout(self):
        # Destroy the game window and go back to the login page
        self.root.destroy()
        login_page()

    @staticmethod
    def get_image():
        # Fetch a new image and solution from an API
        response = urllib.request.urlopen(VegetableGame.API_URL)
        smile_json = json.loads(response.read())
        question = smile_json['question']
        solution = smile_json['solution']
        return question, str(solution)

    def check_answer(self):
        # Check if the user's answer is correct
        user_answer = self.answer.get()

        if user_answer.lower() == self.soln.lower():
            # Update the score, display the next image, and clear the answer entry
            self.score += 1
            self.score_res.config(text=f'Score: {str(self.score)}')
            self.show_image()
            self.answer.delete(0, tk.END)
        else:
            # Display a message if the answer is incorrect
            messagebox.showinfo("Incorrect", "Sorry, that's not the correct answer. Try again!")

def login_page():
    # Create a login window
    login = tk.Tk()
    login.title("Login Page")
    login.geometry("400x200+500+200")

    # Create a frame within the window
    frame = ttk.Frame(login, padding="10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # User name entry
    name_label = ttk.Label(frame, text="Enter your name:")
    name_label.grid(column=0, row=0, sticky=tk.W, pady=10)
    name_entry = ttk.Entry(frame, font=("times new Roman", 14), width=20)
    name_entry.grid(column=1, row=0, sticky=tk.W, pady=10)

    # Start game button
    start_game_button = ttk.Button(frame, text="Start Game", command=lambda: start_game(login, name_entry.get()))
    start_game_button.grid(column=1, row=1, sticky=tk.W, pady=10)

    # Start the login window's event loop
    login.mainloop()

def start_game(login, name):
    # Check if a name is entered, then start the game
    if not name:
        messagebox.showinfo("Error", "Please enter your name.")
    else:
        # Close the login window and start the game window
        login.destroy()
        root = tk.Tk()
        root.title("Vegetable Game")
        root.geometry("800x600+350+100")
        root.resizable(False, False)

        game = VegetableGame(root, name)
        root.mainloop()

# Start the login page
login_page()
