#   Copyright (C) 2022 Junghoon Kim
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>

class BugoLunchMenu:
    
    def __init__(self):
        # import modules
        import datetime
        from datetime import date, timedelta
        
        # today information
        today = str(datetime.date.today())
        if (today[6] == '0'):
            today_date = '&date=' + today[9:10]
        else:
            today_date = '&date=' + today[8:10]
        if (today[5] == '0'):
            today_month = '&month=' + today[6]
        else:
            today_month = '&month=' + today[5:7]


        # tomorrow information
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        if (tomorrow[6] == '0'):
            tomorrow_date = '&date=' + tomorrow[9:10]
        else:
            tomorrow_date = '&date=' + tomorrow[8:10]
        if (tomorrow[5] == '0'):
            tomorrow_month = '&month=' + tomorrow[6]
        else:
            tomorrow_month = '&month=' + tomorrow[5:7]
        
        # get url
        self.today_url = 'https://schoolmenukr.ml/api/middle/J100001889?year=2022&allergy=hidden' + today_month + today_date
        self.tomorrow_url = 'https://schoolmenukr.ml/api/middle/J100001889?year=2022&allergy=hidden' + tomorrow_month + tomorrow_date
    
    
    def td_lunch(self):
        # import modules
        import json
        import requests
        
        response = requests.get(self.today_url)
        school_menu = json.loads(response.text)
        td_menu = school_menu['menu']
        td_menu = td_menu[0]
        td_menu = td_menu['lunch']
        
        return td_menu
        
        
    def tm_lunch(self):
        # import modules
        import json
        import requests
        
        response = requests.get(self.tomorrow_url)
        school_menu = json.loads(response.text)
        td_menu = school_menu['menu']
        td_menu = td_menu[0]
        td_menu = td_menu['lunch']
        
        return td_menu
