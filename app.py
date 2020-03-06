import numpy as np
from flask import Flask, request, jsonify, render_template,redirect, url_for
import pandas as pd
import json
import os
product_json=[]
with open('netaporter_gb_similar.json',encoding="utf8") as fp:
    for product in fp.readlines():
        product_json.append(json.loads(product))
data= pd.DataFrame(product_json)
l1=  data['price']
kk = data['_id']
app = Flask(__name__)
query = []
filters = []
queries = ['discounted_products_list','discounted_products_count and avg_discount','expensive_list','competition_discount_diff_list']
filter_list = ['Discount','Brand Name ','Competition'] 
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    if(int_features[0]>4 or int_features[0]<0 or int_features[1]>3 or int_features[1]<0):
        return render_template('index.html',message = 'please enter query and filter in given range')
    else:
        query.append(int_features[0])
        filters.append(int_features[1])
        p = query[0]
        q= filters[0]
        if(q==1):
            return render_template('ppt.html', message ='query is {} where filter = {} '.format(queries[p-1], filter_list[q-1]))
        elif (q==2):
            return render_template('papa.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        else :
             return render_template('papa.html' , message = 'query is {} and you want filter = {}'.format(queries[p-1], filter_list[q-1]))
@app.route('/fil1',methods=['POST'])
def fil1():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        discount_rate = int(features[1])
        if ( discount_rate > 100 or discount_rate < 0):
            return render_template('ppt.html', chota_message ='Plz make sure symbol can be (>, < ,==) and discount rate is > 0 and < 100')
        else:
            l3=[]
            l4= []
            n=10
            count = 0
            for i in range(len(l1)):
                dit = l1[i]
                p1 = dit['offer_price']
                p2 = dit['regular_price']
                if (p2['value'] - p1['value'])/100 > n/100:
                    l3.append(i)
                    l4.append(p2['value'] - p1['value'])
            l2= []
            for i in l3:
                l2.append(kk[i])
        return render_template('yoga.html', galaxies = l2 )
if __name__ == "__main__":
    app.run(debug=True)