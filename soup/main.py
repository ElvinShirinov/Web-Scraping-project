from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests, time, pandas as pd
#We add the necessary libraries

start_time = time.time()
#We use it for the time determination of the process.


class carSpider():

    #We define our values.
    def __init__(self):
        self.nameList = []
        self.priceList = []
        self.yearList = []
        self.machineList = []
        self.kmList = []

    def get_cars_table(self, car, model, year_from, year_to):
        url = "https://turbo.az/"

        data = {'q[make][]': car, 'q[model][]': model, 'q[year_from]': year_from, 'q[year_to]': year_to}
        url = urljoin(url, '/autos')
        res = requests.get(url, params=data)
        # We take our values.

        soup = BeautifulSoup(res.content, "html.parser")

        #It is ensured that the listed products are detected in the correct specified place.
        try:
            product_main = soup.findAll("div", {"class": "products"})[1]
        except IndexError:
            product_main = soup.findAll("div", {"class": "products"})[0]

        nameAll = product_main.findChildren("div", {"class": "products-i__name"})
        priceAll = product_main.findChildren("div", {"class": "products-i__price"})
        otherAll = product_main.findChildren("div", {"class": "products-i__attributes"})

        #We specify the part with the products and loop it to get all the values there.

        for name in nameAll:
            self.nameList.append(name.get_text())

        for price in priceAll:
            self.priceList.append(price.get_text())

        for other in otherAll:
            s = other.get_text().split(",")
            self.yearList.append(s[0])
            self.machineList.append(s[1][1:])
            self.kmList.append(s[2][1:])

        #We filter the values by breaking them down.

    def getPandaTable(self):
        #We are using Pandas to get the data neatly in tabular form.

        productList = pd.DataFrame({
            "name": self.nameList,
            "price": self.priceList,
            "year": self.yearList,
            "machine": self.machineList,
            "km": self.kmList
        })

        return productList.sort_values(by=['year'], ascending=False)

#We initialize our values.
soup = carSpider()
soup.get_cars_table(4, 149, 2010, 2022)
soup.get_cars_table(4, 150, 2010, 2022)
soup.get_cars_table(4, 154, 2010, 2022)
# make 4 = Mercedes, Model: C180,C200,C250, Year:2010-2022

print(soup.getPandaTable())
print("--- %s seconds ---" % (time.time() - start_time))
