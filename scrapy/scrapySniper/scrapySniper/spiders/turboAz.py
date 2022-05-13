import scrapy, time, pandas as pd
#We add the necessary libraries

start_time = time.time()
#We use it for the time determination of the process.

class carSpider(scrapy.Spider):
    name = "turboaz"
    url = 'https://turbo.az/autos'

    #We define our values.
    def __init__(self):
        self.nameList = []
        self.priceList = []
        self.yearList = []
        self.machineList = []
        self.kmList = []
        self.modelList = ['149', '150', '154']

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
        #We initialize our scrapy.

    def parse(self, response):
        headers = {
            "X-Requested-With": "XMLHttpRequest",
        }
        #We make our definition in order to get the values properly.

        for model in self.modelList:
            #We loop it to get the data of different models.

            data = {'q[make][]': '4', 'q[model][]': model, 'q[year_from]': '2010', 'q[year_to]': '2022'}
            #make 4 = Mercedes, Model: C180,C200,C250, Year:2010-2022

            yield scrapy.FormRequest(
                url=self.url,
                headers=headers,
                method='GET',
                formdata=data,
                callback=self.parse_value
            )
            #We take our values.


    def parse_value(self, response):

        #It is ensured that the listed products are detected in the correct specified place.
        try:
            product_main = response.css("div.products")[1]
        except IndexError:
            product_main = response.css("div.products")[0]

        nameAll = product_main.css("div.products-i__name")
        priceAll = product_main.css("div.product-price")
        otherAll = product_main.css("div.products-i__attributes")

        #We specify the part with the products and loop it to get all the values there.

        for name in nameAll:
            self.nameList.append(self.listToString(name.xpath('text()').extract()))

        for price in priceAll:
            currency = self.listToString(price.css("span").xpath('text()').extract())
            self.priceList.append(self.listToString(price.xpath('text()').extract()) + currency)

        for other in otherAll:
            s = self.listToString(other.xpath('text()').extract()).split(",")
            self.yearList.append(s[0])
            self.machineList.append(s[1][1:])
            self.kmList.append(s[2][1:])


        #We filter the values by breaking them down.

        print(self.getPandaTable())
        print("--- %s seconds ---" % (time.time() - start_time))

    def listToString(self, s):
        #We edit the data that comes as a list and convert it to a string value.
        str1 = " "
        return (str1.join(s))

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
