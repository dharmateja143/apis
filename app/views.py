from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from bs4 import BeautifulSoup
import json
from rest_framework.permissions import AllowAny
import requests
from lxml import html
from rest_framework.response import Response
# Create your views here.
class Currency(APIView):
    permission_classes=(AllowAny,)
    def post(self,request):
        url=request.data['url']
        page = requests.get(url).text
        soup = BeautifulSoup(page,'lxml')
        table_data=[[cell.text for cell in row("td")] for row in soup("tr")]
        table_data.pop(0)
        for i in range(len(table_data)):
            table_data[i][0] = table_data[i][0].replace("\n", "")
            table_data[i][0]=table_data[i][0].replace("\t", "")
        var = ['TICKER 8 MATCHES','LAST', 'CHG%', 'CHG', 'HIGH','LOW','RATING']
        table_data.insert(0,var)
        #print(type(table_data))
        data={'status':200}
        data_list=[]
        for i in range(1,len(table_data)):
            data_dict ={
                'TICKER':table_data[i][0],
                'CHG':table_data[i][3],
                'HIGH':table_data[i][4],
                'LOW':table_data[i][5]
                }
            data_list.append(data_dict)
        data.update({'data':data_list})
        print(data)
        return Response(data)
