# coding: utf-8
import numpy as np
from seaborn import heatmap
import pandas as pd
import itertools
import math
import json
import scrapy
import matplotlib.pyplot as plt
from scrapy.crawler import CrawlerProcess

##########################General Meths#########################
def cost_plus(cost):
    
    return cost + (cost*0.4)

def max_cost_plus(cost):
    
    return (cost/(100-40))*100

#####################Advanced Meths############################
def pricebot(prod_name):
    class PriceBot(scrapy.Spider):
        name = 'pricebot'
        query = prod_name
        start_urls = ['http://www.shopping.com/'+query+'/products?CLT=SCH']

        def parse(self, response):

            prices_container = response.css('div:nth-child(2) > span:nth-child(1) > a:nth-child(1)')
            t_cont = response.css('div:nth-child(2)>h2:nth-child(1)>a:nth-child(1)>span:nth-child(1)')

            title = t_cont.xpath('@title').extract()
            price = prices_container.xpath('text()').extract()
            #Sanitise prices results
            prices = []
            for p in price:
                prices.append(p.strip('\n'))
            #Grouping Prices To Their Actual Products
            product_info = dict(zip(title, prices))
            with open('product_info.txt','w') as f:
                f.write(json.dumps(product_info))

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(PriceBot)
    process.start()

#Credit: datascience.com
def dynamic_pricer(cost,time):
    def price(x, a=200, b=10, d=10, t=np.linspace(1,10,10)):
        """ Returns the price given a demand x and time t
        See equation 4 above"""
        p = (a - b * x) * d / (d + t)
        return p

    def demand(p, a=200, b=10, d=10, t=np.linspace(1,10,10)):
        """ Return demand given an array of prices p for times t
        (see equation 5 above)"""

        return  math.fabs(1.0 / b  * ( a - p * ( d + t ) / d ))

    def price_values(p=0,t=0):

        p_vals = []
        for x in range(1, t, 1):
            p -= (0.033*p)
            p_vals.append(p)

        return np.array(p_vals)

    t_vals = np.linspace(1,time,10)
    p_vals = price_values(cost_plus(cost),10)
    tmp = list(itertools.product(t_vals,p_vals))
    rev_df = pd.DataFrame(tmp, columns=['time','price'])
    rev_df['demand'] = rev_df.apply(lambda row : demand(row['price'], t=row['time']), axis=1)
    rev_df['revenue'] = rev_df.apply(lambda row : row['price']*row['demand'], axis=1)
    rev_df_demand = rev_df.pivot('time','price',values='demand')
    heatmap(rev_df_demand, annot=True, fmt=".2f")
    plt.title('Heatmap of Demand')

    rev_df_revenue = rev_df.pivot('time','price',values='revenue')
    heatmap(rev_df_revenue, annot=True, fmt=".2f")
    plt.title('Heatmap of Revenue')


