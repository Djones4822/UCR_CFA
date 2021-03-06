#!/usr/bin/env python3
import App


def print_help():
    print("To exit, type quit")
    print("To scrape and save to database, type scrape")
    print("That's all for now")


def scrape():
    App.scrape_all()


actions = {'help': print_help, 'quit': quit, 'scrape': scrape}

print("*" * 80)
print(" " * 27 + "UCR_CFA")
print("""
      .::::::::::.        -(_)====u         .::::::::::.
    .::::''''''::::.                      .::::''''''::::.
  .:::'          `::::....          ....::::'          `:::.
 .::'             `:::::::|        |:::::::'             `::.
.::|               |::::::|_ ___ __|::::::|               |::.
`--'               |::::::|_()__()_|::::::|               `--'
 :::               |::-o::|        |::o-::|               :::
 `::.             .|::::::|        |::::::|.             .::'
  `:::.          .::\-----'        `-----/::.          .:::'
    `::::......::::'                      `::::......::::'
      `::::::::::'                          `::::::::::
""")
print("Connecting to " + str(App.engine))
print("Connected to:" + App.get_db_info())
print("*" * 80)
print("If you need it, ask for \"help\"")

while(True):
    command = input("% ")

    if command in actions:
        actions[command]()
    else:
        print("Nope.")
