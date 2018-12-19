import requests
from bs4 import BeautifulSoup
import csv

# Grab the url of the national statistics page.
nat_url = "https://www.bls.gov/oes/current/oes_nat.htm"
page = requests.get(nat_url)

# Check if the page was accessed successfully If code is 200, it implies success
print(page.status_code)

# See page content or the source code of the webpage
# print(page.content)


# Soupify the page (parse the html)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())


# Create a new CSV to store national data in.
job_csv = open("job_data_national.csv", "w")
writer = csv.writer(job_csv)

# Create labels for the columns we're about to scrape.
writer.writerow(
    ["NationOrState", "OccupationCode", "OccupationTitle", "Level", "Employment", "EmploymentRSE", "EmploymentPer1000",
     "MedianHrWage", "MeanHrWage", "AnnualMeanWage", "MeanWageRSE", "LocationQuotient"])

# Add all of the data from the website's national data table to the CSV.
temp_list = []
tables = soup.find_all('tr')
for rows in tables[3:]:
    temp_list.append("National")  # Identify each row as nationwide
    row = rows.find_all('td')
    for item in row:
        if item.string in ["(1)", "(2)", "(3)", "(4)"]:
            # Write none when a footnote between 1 and 4 is detected.
            # These footnotes indicate special conditions that are hard to quantify.
            temp_list.append(None)
        elif item.string == "(5)" and item is row[8]:
            # This indicates a job whose wage >= $208,000 per year.
            temp_list.append(208000)
        elif item.string == "(5)" and item in [row[6], row[7]]:
            # This indicates a job whose wage >= $100 per hour.
            temp_list.append(100)
        else:
            temp_list.append(item.string)
    temp_list.append(1)  # Add the location quotient as 1 for all national rows
    print(temp_list)  # Print the current row so the user can see it as it's added.
    writer.writerow(temp_list)
    print("Row added to file.")
    temp_list = []

# This section: create a CSV that will store state names and URLs.

# Start with a url to add onto to create links for each state.
state_url_base = "https://www.bls.gov/oes/current/oes_"

# Create a dictionary to pair state names with state abbreviations.
dic_states = {"Alabama": "al",
              "Alaska": "ak",
              "Arizona": "az",
              "Arkansas": "ar",
              "California": "ca",
              "Colorado": "co",
              "Connecticut": "ct",
              "Delaware": "de",
              "District of Colombia": "dc",
              "Florida": "fl",
              "Georgia": "ga",
              "Guam": "gu",
              "Hawaii": "hi",
              "Idaho": "id",
              "Illinois": "il",
              "Indiana": "in",
              "Iowa": "ia",
              "Kansas": "ka",
              "Kentucky": "ky",
              "Louisiana": "la",
              "Maine": "me",
              "Maryland": "md",
              "Massachusetts": "ma",
              "Michigan": "mi",
              "Minnesota": "mn",
              "Mississippi": "ms",
              "Missouri": "mt",
              "Nebraska": "ne",
              "Nevada": "nv",
              "New Hampshire": "nh",
              "New Jersey": "nj",
              "New Mexico": "nm",
              "New York": "ny",
              "North Carolina": "nc",
              "North Dakota": "nd",
              "Ohio": "oh",
              "Oklahoma": "ok",
              "Oregon": "or",
              "Pennsylvania": "pa",
              "Puerto Rico": "pr",
              "Rhode Island": "ri",
              "South Carolina": "sc",
              "South Dakota": "sd",
              "Tennessee": "tn",
              "Texas": "tx",
              "Utah": "ut",
              "Vermont": "vt",
              "Virgin Islands": "vi",
              "Virginia": "vi",
              "Washington": "WA",
              "West Virginia": "wv",
              "Wisconsin": "wi",
              "Wyoming": "wy",
              }

# Iterate through the dictionary to write the state names and urls in a CSV.
state_csv = open('job_state_links.csv', 'w')
writer_state = csv.writer(state_csv)
for key, value in dic_states.items():
    tempurl = state_url_base + value + ".htm"
    writer_state.writerow([key, tempurl])
    print("Added", key, "with", tempurl)

# NOTE: this file was originally 2 separate Python files.
# The first contained everything above this point.
# The second contained everything below.
# If you try to run this, and run into problems...
# That's why. Separate them again and it should work.

job_csv2 = open("job_data_states.csv", "w")

csv_file = open("job_state_links.csv", "r")
read = csv.reader(csv_file)
writer = csv.writer(job_csv2)

# Create labels for the columns we're about to scrape.
writer.writerow(
    ["NationOrState", "OccupationCode", "OccupationTitle", "Level", "Employment", "EmploymentRSE", "EmploymentPer1000",
     "MedianHrWage", "MeanHrWage", "AnnualMeanWage", "MeanWageRSE", "LocationQuotient"])

for rowboat in read:
    if rowboat:
        # Grab the url of the STATE's statistics page.
        state_url = rowboat[1]
        state_name = rowboat[0]
        page = requests.get(state_url)

        # Check if the page was accessed successfully. If code is 200, it implies success
        print(page.status_code)

        # See page content or the source code of the webpage
        # print(page.content)

        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.prettify())

        # Add all of the data from the website's state data table to the CSV.
        writer = csv.writer(job_csv2)
        temp_list = []
        tables = soup.find_all('tr')
        for rows in tables[3:]:
            temp_list.append(state_name)  # Identify as state's name
            row = rows.find_all('td')
            for item in row:
                if item is row[6]:  # Skip the location quotient column
                    pass
                elif item.string in ["(1)", "(2)", "(3)", "(4)", "(6)", "(7)", "(8)", "(9)"]:
                    # Write a null when a footnote between 1 and 4 is detected.
                    # These footnotes indicate special conditions that are hard to quantify.
                    temp_list.append(None)
                elif item.string == "(5)" and item is row[9]:
                    # This indicates a job whose wage >= $208,000 per year.
                    temp_list.append(208000)
                elif item.string == "(5)" and item in [row[6], row[7]]:
                    # This indicates a job whose wage >= $100 per hour.
                    temp_list.append(100)
                else:
                    temp_list.append(item.string)
            if row[6].string == "(8)":
                temp_list.append(None)
            else:
                temp_list.append(row[6].string)  # Append the location quotient at the end of each row
            print(temp_list)  # Print the current row so the user can see it as it's added.
            writer.writerow(temp_list)
            # print("Row added to file.")
            temp_list = []
