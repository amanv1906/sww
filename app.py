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
kk = data['_id']
my_tid= ['5d0cc7b68a66a100014acdb0' ,'5da94e940ffeca000172b12a' ,'5da94ef80ffeca000172b12c' ,'5da94f270ffeca000172b12e' , '5da94f4e6d97010001f81d72']
brands= ['tan-luxe',
 'uma oils',
 'marc jacobs beauty',
 'prada',
 'givenchy',
 'off-white',
 'eyeko',
 'mugler',
 'alaïa',
 'vetements',
 'j brand',
 'a.p.c. atelier de production et de création',
 'borgo de nor',
 'eve lom',
 'nars',
 'chantecaille',
 'the row',
 'lano - lips hands all over',
 'kevyn aucoin',
 'heidi klein']
def competitors(c):
    l6=data.iloc[[c],[10,14]]
    l = l6['similar_products']
    l7 = l6['price']
    coro= l7[c]
    jolly = coro['basket_price']
    jolly2 = jolly['value']
    yy = l[c]
    condition = 0
    ee= yy['website_results']
    kk = list(ee.keys())
    for j in range(len(kk)):
        rrq =  ee[kk[j]]
        pp = rrq['knn_items']
        if(len(pp)!=0):
            c=pp[0]
            ta = c['_source']
            llb = ta['price']
            llb1=llb['basket_price']
            llb2= llb1['value']
            if(jolly2<llb2):
                condition = 1
                break
    return condition
app = Flask(__name__)
queries = ['NAP products ','NAP_products_count and avg_discount','expensive_list','competition_discount_diff_list']
filter_list = ['Discount','Brand Name ','Competition'] 
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
    
@app.route('/fil1',methods=['POST'])
def fil1():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        discount_rate = int(features[1])
        if ( discount_rate > 100 or discount_rate < 0):
            return render_template('ppt.html', chota_message ='Plz make sure symbol can be (>, < ,==) and discount rate is > 0 and < 100')
        else:
            n=discount_rate
            if(symbol == 1):
                l3=[]
                l4= []
                l2=[]
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 < n:
                        l3.append(i)
                        l4.append(p2['value'] - p1['value'])
                for i in l3:
                    l2.append(kk[i])
                
            elif(symbol == 3):
                l3=[]
                l4= []
                l2=[]
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 > n:
                        l3.append(i)
                        l4.append(p2['value'] - p1['value'])
                for i in l3:
                    l2.append(kk[i])
            else:
                l3=[]
                l4= []
                l2=[]
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 == n:
                        l3.append(i)
                        l4.append(p2['value'] - p1['value'])
                for i in l3:
                    l2.append(kk[i])
        return render_template('yoga.html', galaxies = l2 )
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
            if(symbol == 1):
                l3= []
                l4 = []
                count = 0
                sum1 = 0
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 < n:
                        l3.append(i)
                        l4.append(((p2['value'] - p1['value'])/p2['value']))
                        count = count + 1
                for i in l4:
                    sum1 = sum1 + i
                disc = 0
                if(count!=0):
                    disc = float(sum1/count)
            elif(symbol == 3):
                l3=[]
                l4 = []
                count = 0
                sum1 = 0
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 > n:
                        l3.append(i)
                        l4.append(((p2['value'] - p1['value'])/p2['value']))
                        count = count + 1
                for i in l4:
                    sum1 = sum1 + i
                disc = 0
                if(count !=0 ):
                    disc = float(sum1 / count)
            else:
                l3 = []
                l4 = []
                count = 0
                sum1  = 0
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if (int((p2['value'] - p1['value'])/p2['value']))*100 == n:
                        l3.append(i)
                        l4.append(((p2['value'] - p1['value'])/p2['value']))
                        count = count + 1
                for i in l4:
                    sum1 = sum1 + i
                disc = 0
                if(count !=0):
                    disc= float(sum1 /count)
        return render_template('yoga1.html', count = count , avg = disc )
        
@app.route('/fil3',methods=['POST'])
def fil3():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        discount_rate = int(features[1])
        if ( discount_rate > 100 or discount_rate < 0):
            return render_template('ppt3.html', chota_message ='Plz make sure symbol can be (>, < ,==) and discount rate is > 0 and < 100')
        else:
            l1=  data['price']
            n=discount_rate
            if(symbol == 1):
                l3=[]
                l4= []
                l2=[]
                for k in range(len(l1)):
                    my_no = k
                    dit = l1[k]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 < n:
                        
                        rr = competitors(my_no)
                    if rr == 0:
                        l3.append(k)
                for ck in l3:
                    l2.append(kk[ck])
                
            elif(symbol == 3):
                l1=data['price']
                l3=[]
                l4= []
                l2=[]
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 > n:
                        rr=competitors(0)
                        if rr == 0:
                            l3.append(i)
                for i in l3:
                    l2.append(kk[i])
            else:
                l1=data['price']
                l3=[]
                l4= []
                l2=[]
                for i in range(len(l1)):
                    dit = l1[i]
                    p1 = dit['offer_price']
                    p2 = dit['regular_price']
                    if ((p2['value'] - p1['value'])/p2['value'])*100 == n:
                        rr = competitors(0)
                        if(rr == 0):
                            l3.append(i)
                for i in l3:
                    l2.append(kk[i])
        return render_template('yoga.html', galaxies = l2 )
@app.route('/fil5', methods=['POST'])
def fil5():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        l6=data['similar_products']
        lol = []
        l2=[]
        for i in range(len(l6)):
            yy = l6[i]
            ee= yy['website_results']
            kl = list(ee.keys())
            for j in range(len(kl)):
                rrq =  ee[kl[j]]
                pp = rrq['knn_items']
                if(len(pp)!=0 and my_tid[symbol-1] == kl[j]):
                    lol.append(i)
                    break
        for j in lol:
            l2.append(kk[j])
    return render_template('yoga.html', galaxies = l2 )
@app.route('/fil6', methods=['POST'])
def fil6():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        l6=data['similar_products']
        l1 = data['price']
        l4 = []
        count = 0
        for i in range(len(l6)):
            dit = l1[i]
            p1 = dit['offer_price']
            p2 = dit['regular_price']
            yy = l6[i]
            ee= yy['website_results']
            kl = list(ee.keys())
            for j in range(len(kl)):
                rrq =  ee[kl[j]]
                pp = rrq['knn_items']
                if(len(pp)!=0 and my_tid[symbol-1] == kl[j]):
                    count = count + 1
                    l4.append(((p2['value'] - p1['value'])/p2['value']))
                    break
        sum1 = 0
        for j in l4:
            sum1 =sum1+ j
        if(count != 0):
            disc = float(sum1/count)
        return render_template('yoga1.html', count = count , avg = disc )
@app.route('/fil7',methods=['POST'])
def fil7():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        l6=data['similar_products']
        l1 = data['price']
        ltr = []
        l_final = []
        condition = 0
        for i in range(len(l1)):
            dit = l1[i]
            p1 = dit['basket_price']
            jool = p1['value']
            yy = l6[i]
            ee= yy['website_results']
            kl = list(ee.keys())
            for j in range(len(kl)):
                rrq =  ee[kl[j]]
                pp = rrq['knn_items']
                if(len(pp)!=0 and my_tid[symbol-1] == kl[j]):
                    condition= 1
                    continue
            if condition == 1:
                for j in range(len(kl)):
                    rrq =  ee[kl[j]]
                    pp = rrq['knn_items']
                    if(len(pp)!=0):
                        c=pp[0]
                        ta = c['_source']
                        llb = ta['price']
                        llb1=llb['basket_price']
                        llb2= llb1['value']
                        if(jool>llb2):
                            ltr.append(i)
        for i in ltr:
            l_final.append(kk[i])
        return render_template('yoga.html', galaxies = l_final)
@app.route('/fil8',methods=['POST'])
def fil8():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        discount = int(features[1])
        n=discount
        l6=data['similar_products']
        l1 = data['price']
        ltr = []
        l_final = []
        for i in range(len(l1)):
            dit = l1[i]
            p1 = dit['basket_price']
            jool = p1['value']
            yy = l6[i]
            ee= yy['website_results']
            kl = list(ee.keys())
            for j in range(len(kl)):
                rrq =  ee[kl[j]]
                pp = rrq['knn_items']
                if(len(pp)!=0 and my_tid[symbol-1] == kl[j]):
                    c=pp[0]
                    ta = c['_source']
                    llb = ta['price']
                    llb1=llb['basket_price']
                    llb2= llb1['value']
                    avg = ((jool+llb2)/2)
                    if((((jool-llb2)/avg)*100) > n):
                        ltr.append(i)
                        continue
        for i in ltr:
            l_final.append(kk[i])
        return render_template('yoga.html', galaxies = l_final)
@app.route('/fil9', methods=['POST'])
def fil9():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        sala = data['brand']
        l_item=[]
        l2=[]
        for i in range(len(sala)):
            p=sala[i]
            cd = p['name']
            l_item.append(cd)
        pp=[]
        for i in range(len(l_item)):
            if l_item[i] == brands[symbol-1]:
                pp.append(i)
        for j in pp:
            l2.append(kk[j])
        return render_template('yoga.html', galaxies = l2 )
@app.route('/fil10', methods=['POST'])
def fil10():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        sala = data['brand']
        l1 = data['price']
        count = 0
        disc=0
        l_item=[]
        for i in range(len(sala)):
            p=sala[i]
            cd = p['name']
            l_item.append(cd)
        pp=[]
        sum1 = 0
        for i in range(len(l_item)):
            dit = l1[i]
            p1 = dit['offer_price']
            p2 = dit['regular_price']
            if l_item[i] == brands[symbol-1]:
                count = count+1
                pp.append(((p2['value'] - p1['value'])/p2['value']))
        for j in pp:
            sum1 = sum1 +  j
        if(count!=0):
            disc = float(sum1/count)
        return render_template('yoga1.html', count = count , avg = disc )
@app.route('/fil11', methods=['POST','GET'])
def fil11():
    if request.method  == 'POST':
        features = [x for x in request.form.values()]
        symbol = int(features[0])
        sala = data['brand']
        l1 = data['price']
        l6=data['similar_products']
        l_item=[]
        l2=[]
        for i in range(len(sala)):
            p=sala[i]
            cd = p['name']
            l_item.append(cd)
        ppt= []
        for k in range(len(l_item)):
            if l_item[k] == brands[symbol-1]:
                dit = l1[k]
                p1 = dit['basket_price']
                jool = p1['value']
                yy=l6[k]
                ee= yy['website_results']
                kl = list(ee.keys())
                for j in range(len(kl)):
                    rrq =  ee[kl[j]]
                    pp = rrq['knn_items']
                    if(len(pp)!=0):
                        c=pp[0]
                        ta = c['_source']
                        llb = ta['price']
                        llb1=llb['basket_price']
                        llb2= llb1['value']
                        if(jool>llb2):
                            ppt.append(j)
                            continue
        for j in ppt:
            l2.append(kk[j])
        return render_template('yoga.html', galaxies = l2)
if __name__ == "__main__":
    app.run(debug=True)