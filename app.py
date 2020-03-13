import numpy as np
from flask import Flask, request, jsonify, render_template,redirect, url_for
import pandas as pd
import json
import os
product_json=[]
#loading of data
with open('netaporter_gb_similar.json',encoding="utf8") as fp:
    for product in fp.readlines():
        product_json.append(json.loads(product))
data= pd.DataFrame(product_json)
#competition id
my_tid= ['5d0cc7b68a66a100014acdb0' ,'5da94e940ffeca000172b12a' ,'5da94ef80ffeca000172b12c' ,'5da94f270ffeca000172b12e' , '5da94f4e6d97010001f81d72']
#brand names
brands=['prada',
 'a.p.c. atelier de production et de création',
 'the row',
 'gucci',
 'saint laurent',
 'jimmy choo',
 'christian louboutin',
 'ancient greek sandals',
 'castañer',
 'giuseppe zanotti',
 'balenciaga',
 'loewe',
 'dodo bar or',
 'matteau',
 'jennifer chamandi',
 'golden goose',
 'aesop',
 'rag & bone',
 'spanx',
 'common projects']
#class through which we can access our queries
class queries_net:
    #this function returns the product id satisfy the filters
    def list_of_product(self,list_of_products):
        l2=[]
        #data['_id'] contains the ids of the product
        kk=data['_id']
        for i in list_of_products:
            l2.append(kk[i])
        return l2
    #this function returns the count and avg discount for the given filter
    def count_and_avg_discount(self,list_of_products,price_dictionary):
        #list_of_product is the list we get after applying filter
        #price dictionary is the dictionary which contains the price related information which is provided 
        count = 0
        disc=0
        sum1=0
        value_of_discounted_product=[]
        for i in list_of_products:
            dit = price_dictionary[i]
            p1 = dit['offer_price']
            p2 = dit['regular_price']
            #we are cqlculating avg of a product and append it in list.
            value_of_discounted_product.append(((p2['value'] - p1['value'])/p2['value']))
            count=count+1
            #after getting count and list of discounted product we are returning avg discount and count of products
        for i in value_of_discounted_product:
            sum1=sum1+i
        if(count!=0):
            disc = float(sum1/count)
        return count,disc
    #expensive list means if the retailer is selling product greater than any of the competitors
    def expensive_list(self,list_of_products,price_dictionary,similar_dictionary):
        #list_of_product is the list we get after applying filter
        #price dictionary is the dictionary which contains the price related information which is provided 
        #similar_dictionary is the dictionary which contains similar product information
        l3=[]
        for k in list_of_products:
            dit = price_dictionary[k]
            #taking value of basket price from price_dictionary
            jolly = dit['basket_price']
            jolly2 = jolly['value']
            yy = similar_dictionary[k]
            condition = 0
            #basket price of competitors is in website result dictionary of similar dictionary
            ee= yy['website_results']
            #it contains the key of the competitors
            kk1 = list(ee.keys())
            for j in range(len(kk1)):
                rrq =  ee[kk1[j]]
                pp = rrq['knn_items']
                #the basket price of competitors is inside knn_items
                if(len(pp)!=0):
                    #here we are checking if the competitors is selling the same product than its knn it should not be empty
                    c=pp[0]
                    ta = c['_source']
                    llb = ta['price']
                    llb1=llb['basket_price']
                    llb2= llb1['value']
                    #comparing both site basket_price value if net a porter is selling product higher than any of the competitors than condition =1
                    if(jolly2>llb2):
                        #why break is used if my condition find any price higher than the competitors than my query becomes true :NAP products where they are selling at a price higher than any of the competition
                        #it saves time because we dont have to compare all competitors 
                        condition = 1
                        break                
            if condition == 1:
                l3.append(k)
        return l3
    #this function is for whether they are selling at a price n% higher than a competitor X
    def competition(self,discount_n,id_no,list_of_product,similar_product_dict,price_dict):
        
        ltr = []
        for i in list_of_product:
            dit = price_dict[i]
            p1 = dit['basket_price']
            jool = p1['value']
            yy = similar_product_dict[i]
            ee= yy['website_results']
            kl = list(ee.keys())
            for j in range(len(kl)):
                rrq =  ee[kl[j]]
                pp = rrq['knn_items']
                #in this one condition is also added which is used for checking the competitor selected by us is in our all competitors list
                if(len(pp)!=0 and my_tid[id_no-1] == kl[j]):
                    c=pp[0]
                    ta = c['_source']
                    llb = ta['price']
                    llb1=llb['basket_price']
                    llb2= llb1['value']
                    avg = ((jool+llb2)/2)
                    #here we are calculating percentage diff
                    #comparing the discount percentage with the percent provided by user
                    if((((jool-llb2)/avg)*100) > discount_n):
                        ltr.append(i)
                        continue
        return ltr
#this class is used to filter the query result
class filters:
    #THIS FUNCTION IS USED TO FILTER OUR QUERY BASED ON DISCOUNT RATE
    def discout_rates(self,price_dictionary,symbol,n):
        #price dictionary is dictionary of price
        #symbol is id of symbol ex 1. less_than 2.equal to 3. greater tham
        #BELOW I AM APPLYING CONDITION WHICH SYMBOL IS SELECTED AND COMPUTE ACCORDING TO THAT
        #N: IS THE DISCOUNT RATE
        if(symbol == 1):
            l3=[]
            for i in range(len(price_dictionary)):
                dit = price_dictionary[i]
                p1 = dit['offer_price']
                p2 = dit['regular_price']
                if ((p2['value'] - p1['value'])/p2['value'])*100 < n:
                    l3.append(i)               
        elif(symbol == 3):
            l3=[]
            for i in range(len(price_dictionary)):
                dit = price_dictionary[i]
                p1 = dit['offer_price']
                p2 = dit['regular_price']
                if ((p2['value'] - p1['value'])/p2['value'])*100 > n:
                    l3.append(i)
        else:
            l3=[]
            for i in range(len(price_dictionary)):
                dit = price_dictionary[i]
                p1 = dit['offer_price']
                p2 = dit['regular_price']
                if ((p2['value'] - p1['value'])/p2['value'])*100 == n:
                    l3.append(i)
    #THIS FUNCTION FILTER OUR QUERY BASED ON BRAND NAME WE SELECT
        return l3
    def brand_filter(self,brand_dictionary,brand_id):
        #BRAND DICTIONARY IS THE DICTIONARY WHICH CONTAINS INFORMATION REGARDING BRAND
        #BRAND ID IS THE ID OF THE BRAND SELECTED BY USER
        l_item=[]
        for i in range(len(brand_dictionary)):
            p=brand_dictionary[i]
            cd = p['name']
            l_item.append(cd)
        pp=[]
        for i in range(len(l_item)):
            if l_item[i] == brands[brand_id-1]:
                pp.append(i)
        return pp
    #THIS FUNCTION FILTER OUR QUERY BASED ON COMPETITOR NAME WE SELECT
    def competition_name(self,similar_dict,c):
        #SIMILAR DICTIONARY IS THE DICTIONARY WHICH CONTAINS INFORMATION REGARDING COMPETITORS
        #BRAND ID IS THE ID OF THE BRAND SELECTED BY USER
        lol = []
        for i in range(len(similar_dict)):
            yy = similar_dict[i]
            ee= yy['website_results']
            kl = list(ee.keys())
            for j in range(len(kl)):
                rrq =  ee[kl[j]]
                pp = rrq['knn_items']
                #if my list of competitors is not empty and competitor entered by user matches then
                if(len(pp)!=0 and my_tid[c-1] == kl[j]):
                    lol.append(i)
                    break
        return lol
#here i am creating flask app
app = Flask(__name__)
queries = ['NAP products ','NAP_products_count and avg_discount','expensive_list','competition_discount_diff_list']
filter_list = ['Discount','Brand Name ','Competition'] 
#home is the main page of our API
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    query=[]
    filters=[]
    int_features = [int(x) for x in request.form.values()]
    if(int_features[0]>4 or int_features[0]<0 or int_features[1]>3 or int_features[1]<0):
        return render_template('index.html',message = 'please enter query and filter in given range')
    else:
        query.append(int_features[0])
        filters.append(int_features[1])
        p = query[0]
        q= filters[0]
        if(p==1 and q==1):
            return render_template('ppt.html', message ='query is {} where filter = {} '.format(queries[p-1], filter_list[q-1]))
        elif (p==2 and q==1):
            return render_template('ppt2.html', message ='query is {} where filter = {} '.format(queries[p-1], filter_list[q-1]))
        elif (p==3 and q==1):
            return render_template('ppt3.html', message ='query is {} where filter = {} '.format(queries[p-1], filter_list[q-1]))
        elif(p==4 and q==1):
            return render_template('Q4F4.html', message ='query is {} where filter = {} '.format(queries[p-1], filter_list[q-1]))
        elif (p==1 and q==3):
            return render_template('Q1F.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        elif (p==2 and q==3):
            return render_template('Q2F.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        elif(p== 3 and q== 3):
            return render_template('Q3F.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        elif ( p == 4 and q == 3):
            return render_template('Q4F.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        elif (p==1 and q==2):
            return render_template('Q1F1.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        elif (p==2 and q==2):
            return render_template('Q2F2.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        elif(p== 3 and q== 2):
            return render_template('Q3F3.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
        elif ( p == 4 and q == 2):
            return render_template('Q4F4.html' , message = 'query is {} where  filter = {}'.format(queries[p-1], filter_list[q-1]))
#this function is for when our query is give list of product and filter = discount
@app.route('/fil1',methods=['POST'])
def fil1():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        discount_rate = int(features[1])
        if ( discount_rate > 100 or discount_rate < 0):
            return render_template('ppt.html', chota_message ='Plz make sure symbol can be (>, < ,==) and discount rate is > 0 and < 100')
        else:
            price_dictionary=data['price']
            n=discount_rate
            obj  = filters()
            obj2  = queries_net()
            my_filter_list = obj.discout_rates(price_dictionary,symbol,n)
            my_query_1 = obj2.list_of_product(my_filter_list)
        return render_template('yoga.html', galaxies = my_query_1 )
#this function is for when our query is give count and avg discount of product and filter = discount
@app.route('/fil2',methods=['POST'])
def fil2():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        discount_rate = int(features[1])
        if ( discount_rate > 100 or discount_rate < 0):
            return render_template('ppt2.html', chota_message ='Plz make sure symbol can be (>, < ,==) and discount rate is > 0 and < 100')
        else:
          n=discount_rate
          price_dictionary=data['price']
          object_filter = filters()
          object_query = queries_net()
          my_filter_list = object_filter.discout_rates(price_dictionary,symbol,n)
          count,disc = object_query.count_and_avg_discount(my_filter_list,price_dictionary)
        return render_template('yoga1.html', count = count , avg = disc )
#this function is for when our query is expensive list and filter = discount    
@app.route('/fil3',methods=['POST'])
def fil3():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        discount_rate = int(features[1])
        if ( discount_rate > 100 or discount_rate < 0):
            return render_template('ppt3.html', chota_message ='Plz make sure symbol can be (>, < ,==) and discount rate is > 0 and < 100')
        else:
            price_dictionary =  data['price']
            similar_product_dictionary = data['similar_products']
            n=discount_rate
            object_filter = filters()
            object_query = queries_net()
            my_filter_list = object_filter.discout_rates(price_dictionary,symbol,n)
            l2  = object_query.expensive_list(my_filter_list,price_dictionary,similar_product_dictionary)
            my_query_3 = object_query.list_of_product(l2)
            return render_template('yoga.html', galaxies = my_query_3 )
#this function is for when our query is give list of product and filter = competitor
@app.route('/fil5', methods=['POST'])
def fil5():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        similar_dict=data['similar_products']
        obj  = filters()
        obj2  = queries_net()
        my_filter_list = obj.competition_name(similar_dict,symbol)
        my_query_1 = obj2.list_of_product(my_filter_list)
        return render_template('yoga.html', galaxies = my_query_1 )
#this function is for when our query is give count and avg discount of product and filter = competitor
@app.route('/fil6', methods=['POST'])
def fil6():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        price_dictionary=data['price']
        similar_dictionary=data['similar_products']
        object_filter = filters()
        object_query = queries_net()
        my_filter_list = object_filter.competition_name(similar_dictionary,symbol)
        count,disc = object_query.count_and_avg_discount(my_filter_list,price_dictionary)
        return render_template('yoga1.html', count = count , avg = disc )
#this function is for when our query is give expemsive list of product and filter = competitor
@app.route('/fil7',methods=['POST'])
def fil7():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        price_dictionary =  data['price']
        similar_dictionary = data['similar_products']
        object_filter = filters()
        object_query = queries_net()
        my_filter_list = object_filter.competition_name(similar_dictionary,symbol)
        l2  = object_query.expensive_list(my_filter_list,price_dictionary,similar_dictionary)
        my_query_3 = object_query.list_of_product(l2)
        return render_template('yoga.html', galaxies = my_query_3 )
@app.route('/fil8',methods=['POST'])
#this function is for when our query is give list of product where they are selling greater than n% from competitor and filter = competitor
def fil8():
    if request.method  == 'POST':
         features = [x for x in request.form.values()]
         symbol = int(features[0])
         discount_rate = int(features[1])
         price_dictionary=data['price']
         similar_dictionary = data['similar_products']
         obj  = filters()
         obj2  = queries_net()
         my_filter_list = obj.competition_name(similar_dictionary,symbol)
         my_query_1 = obj2.competition(discount_rate,symbol,my_filter_list,similar_dictionary,price_dictionary)
         my_query_3 = obj2.list_of_product(my_query_1)      
         return render_template('yoga.html', galaxies = my_query_3)     
#this function is for when our query is give list of product and filter = brand_name
@app.route('/fil9', methods=['POST'])
def fil9():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        brand_index = int(features[0])
        brand_dictionary = data['brand']
        obj_brand = filters()
        obj_id = queries_net()
        filter_list= obj_brand.brand_filter(brand_dictionary,brand_index)
        brand_id = obj_id.list_of_product(filter_list)
        return render_template('yoga.html', galaxies = brand_id)
#this function is for when our query is give count and avg_discount of product and filter = brand_name
@app.route('/fil10', methods=['POST'])
def fil10():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        brand_index = int(features[0])
        brand_dictionary = data['brand']
        price_dictionary = data['price']
        obj_brand_count = filters()
        obj_id_1 = queries_net()
        filter_list= obj_brand_count.brand_filter(brand_dictionary,brand_index)
        count,disc = obj_id_1.count_and_avg_discount(filter_list,price_dictionary)
        return render_template('yoga1.html', count = count , avg = disc )
#this function is for when our query is give expensive list of product and filter = competitor
@app.route('/fil11', methods=['POST','GET'])
def fil11():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        brand_index = int(features[0])
        brand_dictionary = data['brand']
        price_dictionary= data['price']
        similar_dictionary= data['similar_products']
        obj_brand_exp = filters()
        obj_id_2 = queries_net()
        filter_list= obj_brand_exp.brand_filter(brand_dictionary,brand_index)
        brand_id_exp = obj_id_2.expensive_list(filter_list,price_dictionary,similar_dictionary)
        my_query_3 = obj_id_2.list_of_product(brand_id_exp)
        return render_template('yoga.html', galaxies = my_query_3)
if __name__ == "__main__":
    app.run(debug=True)
