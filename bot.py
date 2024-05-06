import botogram
from json import load
import random

API_TOKEN = " INSERT Token here  "

my_bot = botogram.create(API_TOKEN)
my_bot.about = 'Your pal for navigating the Nigerian Job market'
my_bot.before_help = ["show jobs: This show shows you the current jobs that's hiring this week", "\njobs_today: this shows you 20 random jobs "]
file_choice = ["job_gurus.json", "jobberman.json"]

@my_bot.command("Hello")
def job_handler(chat, message, args):
    buttons = botogram.Buttons()
    buttons[0].callback("Jobs for the Week", "week_jobs")
    buttons[1].callback("job of the day", "day_jobs")
    chat.send("Welcome, what are you interested in today?",attach=buttons)

@my_bot.callback("week_jobs")
def week_jobs(chat, query):
    chosen_file = random.choice(file_choice) #gives the illusion of a different job being added
    with open(chosen_file, "r") as job_file:
        week_job_data = load(job_file)
        
    if chosen_file == file_choice[0]:
        for job in week_job_data:
            chat.send(f"Job Name:{job['job_name']} \n Description:{job['description']}\n Link:{job['apply']}\n Date:{job['date_published']}")
    else:
        for job in week_job_data:
            chat.send(f"Job name:{job['job_name']}\n Company name:{job['company_name']}\n location{job['location']}\n Link:{job['link']}\n Salary:{job['salary']}")

@my_bot.callback("day_jobs")
def day_jobs(chat,query):
    chosen_file = random.choice(file_choice)
    with open(chosen_file, "r") as job_file:
        day_job_data = load(job_file)
    if chosen_file == file_choice[0]:
        for job_counter in range(20):
            chosen_job = random.choice(day_job_data)
            chat.send(f"Job Name:{chosen_job['job_name']} \n Description:{chosen_job['description']}\n Link:{chosen_job['apply']}\n Date:{chosen_job['date_published']}")
    else:
        for job_counter in range(20):
            chosen_job = random.choice(day_job_data)
            chat.send(f"Job name:{chosen_job['job_name']}\n Company name:{chosen_job['company_name']}\n location{chosen_job['location']}\n Link:{chosen_job['link']}\n Salary:{chosen_job['salary']}")

if __name__ == "__main__":
    my_bot.run()
