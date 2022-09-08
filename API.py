import requests, time, re, pytz
from datetime import date
import datetime
from bs4 import BeautifulSoup as BS

def Login(User, Password):
	session = requests.Session()
	response1 = session.get('https://www.faaflightschools.com/')
	data = {
		'kt_login_user': User,
		'kt_login_password': Password,
		'kt_login1': 'Login'
	}
	response = session.post('https://www.faaflightschools.com/login.php', data=data)
	return response1.cookies.get_dict()['PHPSESSID']

def Get_Schedule(PHPID, Month = date.today().month, Day = date.today().day, Year = date.today().year, nr_days=7):
	params = {
	'm': Month,
	'y': Year,
	'd': Day,
	'sch_date': f"{Year}-{Month}-{Day}",
	'nr_days': nr_days-1,
	}

	response = requests.get('https://www.faaflightschools.com/adminclients/schedule.php', params=params, cookies={"PHPSESSID": PHPID})
	return response.text

def Get_Reserved_Resources(html, TimeZone = pytz.timezone('America/New_York')):
	Array_To_Return = []
	doc = BS(html, 'html.parser')
	First_Subsection = doc.find(id = "content_bottom")
	Days = First_Subsection.find_all("table", {"class": "schedule_day_h"})
	for Day in Days:
		for Tags in Day.find_all("tr"):
			for Tag in Tags:
				if str(Tag).__contains__("day_h_reserved_instruction"):
					TimeDelta = datetime.timedelta(minutes= 15 * int(Tag["colspan"]))
					Start_Time = TimeZone.localize(datetime.datetime.strptime(Day.find_all("td")[1].text + " " +re.findall("[0-9:]+.[A-z:]+", Tag.text)[0], "%A, %B %d, %Y %I:%M %p"))
					End_Time = Start_Time + TimeDelta
					Resource_Name = Tags.find_all("td")[0].text
					Is_Plane = bool(re.search("[0-9]+[A-z]", Resource_Name))
					Compiled_Data = {
						"Start_Time": Start_Time,
						"End_Time": End_Time,
						"Resource_Name": Resource_Name,
						"TimeDelta": TimeDelta,
						"Is_Plane": Is_Plane
					}
					Array_To_Return.append(Compiled_Data)
	return Array_To_Return

def Merge_Reserved_Resources(Array_):
	New_Array = []
	for item in Array_:
		if item["Is_Plane"] == True:
			for item_2 in Array_:
				if item["Start_Time"] == item_2["Start_Time"] and item_2["Is_Plane"] == False:
					if item["Is_Plane"] == True:
						New_Array.append(item)
					else:
						New_Array.append(item_2)
	return New_Array
