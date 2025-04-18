import wikipediaapi
import json



def main(): 
	wiki = wikipediaapi.Wikipedia(
        user_agent="WikiMorti/1.0 (xetayi2137@isorax.com)", 
        language='en'
    )

	# generate pages to scrape
	months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	
	years = [x for x in range(1992, 2024)]

	tot_data = {}
	
	for year in years:
		tot_data[year] = {}
		for month in months:
			print("Processing", year, month)
			page = wiki.page('Deaths_in_'+month+"_"+str(year))
			
			parsed_page = parse_page(page.text, month, year)
			tot_data[year][month] = parsed_page
			print("Added",sum(len(v) for v in parsed_page.values()),"deaths")
  
		with open('deadge.json', 'w') as f:
			json.dump(tot_data, f, indent=3)



"""
Parses a page representing a month of a year and
returns the corresponding deaths. 
"""
def parse_page(text, month, year):
	day_to_deaths = {}
	day = 1
	# find where the doc with deaths starts: month + year
	text_divided = text.split("\n")
	parsing_day = False
	for line in text_divided:
  	# find the first day -> 1
		if line == str(day):
			day_to_deaths[day] = []
			day += 1
			parsing_day = True
  	# until we find the n2, parse the line
		elif line != "" and not line.startswith("=") and parsing_day:	
			parsed_line = parse_line(line)
			if parsed_line != None:
				day_to_deaths[day-1].append(parsed_line)	

	return day_to_deaths



"""
Parses a line indicating a death occurence. 
If the line is not parsable (doesn't respect the standards)
None is retuned.
"""
def parse_line(line):
	line_to_list = line.split(', ')
	person = {}
  
	if len(line_to_list) > 1:
		person["name"] = line_to_list[0]

		try:	
			person["age"] = int(line_to_list[1].split("-")[0].strip())
		except ValueError as e:
			return None

		person["info"] = line_to_list[2:]

		return person
	else:
		return None




"""
Pretty prints a python object via json
"""
def pprint(obj):
	print(json.dumps(obj, indent=3))



if __name__ == "__main__":
    main()