from django.http import HttpResponse


def index(request):
    product_num = request.GET.get('product', 1)
    urls = gen_fuel([product_num], regions, day)
    fuel_data = get_fuel_data(urls)
    fuel_data_rows = ''
    for value in fuel_data:
        fuel_data_rows = fuel_data_rows + """
            <tr>
                <td>{price} </td><td>{address} </td><td>{location} </td><td>{brand}</td><td>{latitude} </td><td>{longitude} </td>
            </tr>
        """.format(**value)

    return HttpResponse("<table>" + fuel_data_rows + "</table>")

def price_list(request):
    fuel_data_rows_string = ''
    for value in fuel_data:
        fuel_data_rows_string = fuel_data_rows_string + """
            <tr>
                <td>{price} </td><td>{address} </td><td>{location} </td><td>{brand}</td>
            </tr>
        """.format(**value)
    return HttpResponse("<table>" + fuel_data_rows_string + "</table>")

    """<table>
        <tr><td>Prices</tr>
            </td>Prices2</td>
        </tr>
    </table>''')
"""

# fuel data created from the below into a html file

import requests
from lxml import etree as ET
import collections, itertools
from pprint import pprint

# Returns a list of URLs based on the variables for fueld_types, regions and day.
def gen_fuel(fuel_types, regions, day):

    fuel_watch_urls_list = [
        'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}&Day={}'.format(*i)
        for i in itertools.product(fuel_types, regions, day)
    ]
    return fuel_watch_urls_list

# for each in listed_fuel_watch_urls:
#    print(each)

# Uses the URLs created with function def gen_fuel and from the XML grabs the data and adds it to a dictionary, leaving a list of dictionaries with all data.
def get_fuel_data(listed_fuel_watch_urls):
    for item in listed_fuel_watch_urls:
        item = requests.get(item)

        dataContent = ET.fromstring(item.content)

        allItems = dataContent.findall('.//item')
        list_of_dicts = []
        for info in allItems:

            price = info.find('price').text
            address = info.find('address').text
            location = info.find('location').text
            brand = info.find('brand').text
            lat = info.find('latitude').text
            long = info.find('longitude').text

            data_dict =  {
                'price': price,
                'address': address,
                'location': location,
                'brand': brand,
                'latitude': lat,
                'longitude': long,
            }
            list_of_dicts.append(data_dict)

        data1 = sorted(list_of_dicts, key=lambda k: k ['price'])
        return list_of_dicts


# These variables provide the information to what fuel types, area and day that the gen_fuel function uses to create the required URLS.
fuel_types = [1, 2, 6]
regions = [25, 27]
day = ['today', 'tomorrow']

# The out come of function gen_fuel and the variables for fuel type, region and days.
listed_fuel_watch_urls = gen_fuel(fuel_types, regions, day)

# This variable is the data provided from the list of dictonaries in function get_fuel_data and passes the list of URLs.
fuel_data = get_fuel_data(listed_fuel_watch_urls)

# pprint(fuel_data, indent=4)

# converts the list of dictionaries a string.
# fuel_data_string = str(fuel_data)

""" Empty string fuel_data_rows_string is created, a for loop iterates over fuel_data which contains the list 
of dictionaries and adds the value for keys price, address, location and name into a row which is contained in a string"""
fuel_data_rows_string = ""

for value in fuel_data:
    fuel_data_rows_string += """
        <tr>
            <td>{price} </td><td>{address} </td><td>{location} </td><td>{brand}</td>
        </tr>
    """.format(**value)

# Formats the html.
fuel_data_html = "<html><title>Fuel Report</title><body><tbody><table>" + fuel_data_rows_string + "</table></tbody></body></html>"

# Opens and creates a file named fuel_report.html with write access.
# fuel_file = open('fuel_report.html', 'w')

# Writes the the data from fuel_data_html into the fuel_report.html file.
# fuel_file.write(fuel_data_html)

# Closes fuel_report.html.
# fuel_file.close()

