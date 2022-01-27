from time import time
import dateutil.parser
from django.utils import timezone
import pytz

# RestFramework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
#Django
from django.http.response import JsonResponse
from django.contrib import messages
from django.shortcuts import render
#JSON
import json
from jsonfield import JSONField
from datetime import datetime, timedelta
#Amazon Scraper Built on Selenium
from .scrape import scrape
#Importing models and serializers
from Crawler_App import serializers
from .models import ProductDetails, HtmlModel
#Selenium
from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_html(sku):
    """Gets HTML from the page source"""
    chrome_options=Options()
    chrome_options.add_argument("--headless")
    chrome_path=which('chromedriver')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(f"https://www.amazon.in/dp/{sku}/")
    _html = driver.page_source
    return _html


class ProductDetailsApiView(APIView):
    """Gets and Stores Product Details into the Database upon receiving input as sku/url"""
    serializer_class = serializers.SKUSerializer   #expects sku/url as input

    def get(self, request, format=None):
        """Displays the Product Details"""
        t1 = time()
        products = ProductDetails.objects.all()
        products_serializer = serializers.ProductDetailsSerializer(products, many=True)
        t2 = time()
        return Response({'products':products_serializer.data,
                         'time_taken': f'{t2-t1} s'})

    def post(self, request):
        """Updates the database with the Product Details and displays the Details"""
        t1 = time()
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid() :
            sku = serializer.validated_data.get('sku')

            if ("amazon.in" in str(sku)):
                temp_list = str(sku).split("/")
                try:
                    sku_index=temp_list.index("dp")+1
                except:
                    sku_index=temp_list.index("gp")+2          #For Amazon Fresh Products
                sku=temp_list[sku_index]

            one_hr_ago = timezone.now() - timedelta(hours=1)
            
            q1 = ProductDetails.objects.exclude(timestamp__lt=one_hr_ago)
            q2 = q1.filter(sku__exact=sku)
            
            if (len(q2)>0):
                product_serializer = serializers.ProductDetailsSerializer([q2[0]], many=True)
                d = {'message': 'Recently scraped within 60 min ',
                                 'details': product_serializer.data}
                
                t2 = time()
                return Response({'message': 'Recently scraped within 60 min ',
                                 'details': product_serializer.data,
                                 'time_taken': f'{t2-t1} s'})
                

            details = scrape(str(sku))
            title = details['title']
            price = details['price']
            desc = details['desc']
            ratings_map = json.dumps(details['ratings_map'])
            product_serializer = serializers.ProductDetailsSerializer(data={'sku':sku,'title':title,'price':price,
            'description': desc, 'ratings':ratings_map})
            
            if product_serializer.is_valid():
                product_serializer.save()
            t2 = time()
            return Response({'details':details,
                             'time_taken': f'{t2-t1} s'})

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )


class HtmlApiView(APIView):
    """Gets the HTML from page source and stores it into the database"""
    serializer_class = serializers.SKUSerializer   #expects sku/url as input

    def get(self, request, format=None):
        """Displays the HTML"""
        htmls = HtmlModel.objects.all()
        html_serializer = serializers.HtmlSerializer(htmls, many=True)
        return Response(html_serializer.data)
        
    def post(self, request):
        """Stores the HTML in database"""
        t1 = time()
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid() :
            sku = serializer.validated_data.get('sku')
            if ("amazon.in" in str(sku)):
                temp_list = str(sku).split("/")
                sku_index=temp_list.index("dp")+1
                sku=temp_list[sku_index]
            _html = get_html(str(sku))
            html_serializer = serializers.HtmlSerializer(data={'sku':sku,'_html':_html})
            if html_serializer.is_valid():
                html_serializer.save()
            t2 = time()
            return Response({'html':_html,
                             'time_taken': f'{t2-t1} s'})

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )
            

class ProductDetailsHistoryApiView(APIView):
    """Gets and Displays the Product Details History from Database """
    serializer_class = serializers.ProductHistorySerializer   #expects sku/url as input

    def get(self, request, format=None):
        """Displays the Product details"""
        products = ProductDetails.objects.all()
        products_serializer = serializers.ProductDetailsSerializer(products, many=True)
        return Response(products_serializer.data)

    def post(self, request):
        """Displays Product Details History from Database"""
        t1 = time()
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid() :
            sku = serializer.validated_data.get('sku')
            if ("amazon.in" in str(sku)):
                temp_list = str(sku).split("/")
                sku_index=temp_list.index("dp")+1
                sku=temp_list[sku_index]
            timestamp = serializer.validated_data.get('timestamp')
            q1 = ProductDetails.objects.filter(sku__exact=sku)
            q2 = q1.exclude(timestamp__gte=timestamp).order_by('-timestamp')[0]
            history_serializer = serializers.ProductDetailsSerializer([q2], many=True)
            t2 = time()
            return Response({'history':history_serializer.data,
                             'time_taken': f'{t2-t1} s'})

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )


class PriceTrendApiView(APIView):
    """Displays Price trend of a Product"""
    serializer_class = serializers.SKUSerializer   #expects sku/url as input

    def get(self, request, format=None):
        """Displays All the Products"""
        products = ProductDetails.objects.all()
        products_serializer = serializers.ProductDetailsSerializer(products, many=True)
        return Response(products_serializer.data)

    def post(self, request):
        """Displays the Price Trend of a Product"""
        t1 = time()
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid() :
            sku = serializer.validated_data.get('sku').strip()
            print(sku)
            if ("amazon.in" in str(sku)):
                temp_list = str(sku).split("/")
                # print(temp_list)
                sku_index=temp_list.index("dp")+1
                sku=temp_list[sku_index]
                # print(sku)
            trend = ProductDetails.objects.filter(sku__exact=sku).order_by('-timestamp')
            # print(q1)
            # query = f'''SELECT * FROM hello_app_tutorial WHERE sku in(\'{sku}\') '''
            #and to_date(timestamp)<to_date({timestamp}) order by timestamp desc
            # trend = ProductDetails.objects.raw(q1)
            trend_serializer = serializers.PriceTrendSerializer(trend, many=True)
            t2 = time()
            return Response({'trend':trend_serializer.data,
                             'time_taken': f'{t2-t1} s'})
            
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )                