
<p align="center">
  <a href="https://bch.hs.kr/smain.html">
    <img src="https://user-images.githubusercontent.com/86881143/155121564-74be7870-037e-43f3-992e-a39c3de779b7.png" height="180px">
  </a>
</p>
<h1 align="center"> BugoBot </h1>

The BugoBot, Discord bot, is developed for all students of Bucheon High School. But if you change some dummy codes, you can create your own service!

- [Food Menu API](#food-menu-api)
  - [School Type](#school-type)
  - [School Code](#school-code)
  - [Import Meal Menu](#import-meal-menu)
  - [Parameter](#parameter)
  - [Example](#example)
  - [Result](#result)
- [License](#license)

## Food Menu API

You can get a school food menu as [JSON](https://opentutorials.org/course/1375/6844) via an [HTTP GET request](https://opentutorials.org/course/3385/21674). So data can be called from any platform.

When a meal is requested more than once, the meal is saved on the server by the requested school, year, and month, greatly improving response speed. Also support elementary, middle, and high schools in Korea.

## School Type

  * Elementay School : `elementary`
  * Middle School : `middle`
  * High school : `high`

## School Code

You can get your school code [here](https://schoolmenukr.ml/code/app)!

Then go to the [lunch_api.py](./codes/api/lunch_api.py) code and fix this one:

```python
# get url
self.today_url = 'https://schoolmenukr.ml/api/your_school_type/your_school_code?year=2022&allergy=hidden' + today_month + today_date
self.tomorrow_url = 'https://schoolmenukr.ml/api/your_school_type/your_school_code?year=2022&allergy=hidden' + tomorrow_month + tomorrow_date
```

Fix `your_school_type` type and `your_school_code`!

## Import Meal Menu

`https://schoolmenukr.ml/api/your_school_type/your_school_code` is the main address. And you can add more condition of address.

### Parameter

 > This part is optional.

<code>https://<span></span>schoolmenukr.<span></span>ml/api/your_school_type/your_school_code<strong>?[variable_name1]=[value1]&[variable_name2]=[value2]</strong></code>

| Variable Name | Explanation | Initial Value |
| :------: | ------ | ------ |
| year | By specifying a specific year, the menu corresponding to that year is loaded. | Year of current date | 
| month | By specifying a specific month, the menu for that month is called up. | Month of current date |
| date | By specifying a specific day, the menu for that day is called up. | Day of current date |
| allergy | When set to 'hidden', allergy information is not displayed, and when set to 'formed', information is displayed structured. | None |

### Example

> Python
```python
import requests
import json

url = 'https://schoolmenukr.ml/api/middle/X123456789?year=2018&month=5'
response = requests.get(url)
school_menu = json.loads(response.text)
print(school_menu)
```

### Result
```
{
    menu: [
        ...,
        {
            date:"5",
            breakfast:["찹쌀밥","홍합미역국5.6.","닭갈비5.6.13.","김구이13.","배추김치9.13.","방울토마토12."],
            lunch:["흑미밥","콩나물국5.13.","돼지등뼈김치찜9.10.13.","도토리묵무침5.6.13.","총각김치9.13.","청포도"],
            dinner:["찹쌀밥","오징어짬뽕국5.6.","배추겉절이13.","포도쥬스5.13.","만두오꼬노미야끼1.5.6.10.12.13."]
        },
        ...
    ],
    server_message: ["foo", "bar", ...]
}
```

## License

© 2021, Hey-bugo. Released under [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

**BugoBot** is authored and maintained by [@CharlesbrownK](https://github.com/CharlesbrownK).
