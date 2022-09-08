import API, Config

PHPID_ = API.Login(Config.Email, Config.Password)['PHPSESSID']

Data = API.Merge_Reserved_Resources(API.Get_Reserved_Resources(API.Get_Schedule(PHPID=PHPID_)))

print(f"Next Flight: {Data[0]['Start_Time'].strftime('%A %d, at %I:%M %p')}")