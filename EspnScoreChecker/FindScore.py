from bs4 import BeautifulSoup
import requests
import tkinter
import customtkinter
import math

URL = "https://www.espn.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def userInterface():
    #Give 5 options nfl nba mlb nhl soccer 
    #Display all the teams
    #Display what time the next game is
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")
    app = customtkinter.CTk()
    app.geometry("720x480")
    app.title("Espn Tracker")
    title = customtkinter.CTkLabel(app,text="Pick a league",font=("Arial", 24))
    title.grid(row=0, column=0, columnspan=2, pady=20)
    displayButtons(app)
    app.mainloop()

def displayButtons(app):
    nba_button = customtkinter.CTkButton(app,text="NBA",command=lambda: getTeams("nba",app),width=300,height=125)
    nba_button.grid(row=1, column=0, padx=30, pady=20)
    nfl_button = customtkinter.CTkButton(app,text="NFL",command=lambda: getTeams("nfl",app),width=300,height=125)
    nfl_button.grid(row=1, column=1, padx=30, pady=20)
    nhl_button = customtkinter.CTkButton(app,text="NHL",command=lambda: getTeams("nhl",app),width=300,height=125)
    nhl_button.grid(row=2, column=0, padx=30, pady=30)
    mlb_button = customtkinter.CTkButton(app,text="MLB",command=lambda: getTeams("mlb",app),width=300,height=125)
    mlb_button.grid(row=2, column=1, padx=30, pady=30)

def clear_all_widgets(root):
    for widget in root.winfo_children():
        widget.destroy()


def displayTeams(app, teams):
    num_teams = len(teams)
    columns = 4  # Fixed number of columns for better layout
    rows = (num_teams + columns - 1) // columns  # Calculate the necessary number of rows

    for index, (team, url) in enumerate(teams.items()):
        row = 2 + (index // columns)  # Start from row 2 to avoid overlapping with league buttons
        col = index % columns
        button = customtkinter.CTkButton(app, text=team, command=lambda t=team: scrape(teams,team,app), width=150, height=40)
        button.grid(row=row, column=col, padx=10, pady=10)

def getTeams(option,app):
    espn_teams_url = URL+f'{option}/teams'
    response = requests.get(espn_teams_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    teams_section = soup.find('div', {'class': 'layout__column layout__column--1'}).findAll('div', {'class': 'ContentList__Item','role':'listitem'})
    global teams
    teams = {}
    for t in teams_section:
        team_name = t.find_all('h2',class_='di clr-gray-01 h5')[0].get_text()
        team_url = t.find('a', href=True)['href']
        full_url = "https://www.espn.com" + team_url
        teams[team_name] = full_url
    clear_all_widgets(app)
    displayTeams(app,teams)
    

def getUrl(teams,team):
    team_url = teams[team].split("_")
    team_url = team_url[0]+"schedule/_"+team_url[1]
    return team_url

def scrape(teams,team,app):
    page = requests.get(getUrl(teams,team), headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    home = soup.find('span',class_='db fw-bold').get_text()
    try:
        first_game = soup.find('tr',attrs={'class': 'Table__TR Table__TR--sm Table__even','data-idx':'2'}).findAll('td')
    except AttributeError:
        first_game = soup.find('tr',attrs={'class': 'filled Table__TR Table__TR--sm Table__even','data-idx':'2'}).findAll('td')
    
    date = first_game[1].get_text().strip()
    oppenent = first_game[2].get_text().split(" ")[1]
    time = first_game[3].get_text().strip()
    channel = first_game[4].get_text()
    clear_all_widgets(app)
    result_label = customtkinter.CTkLabel(app, text=f'The {home} plays against {oppenent}, {date} at {time}, available on {channel}', font=("Arial", 16))
    result_label.grid(row=10, column=0, columnspan=5, pady=20)
    print(f'The {home} plays against {oppenent}, {date} at {time}, available on {channel}')


userInterface()


