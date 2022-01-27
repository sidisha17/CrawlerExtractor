# Crawler_Project

Built a Rest API service to crawl and extract several product attributes of a given product’s SKU as input from its Amazon page using Python, Django and Selenium.

Steps to run the project:

1.	Install Anaconda Navigator. (https://www.anaconda.com/products/individual)
2.	Create a new virtual environment(Refer Image anaconda_environment.png in Screenhots folder):
    Open Anaconda Navigator and open the Environments on the left and then Create at the bottom to create a virtual environment
3.	Download the Crawler_Project folder and extract it
4.	Open your terminal (either from Anaconda Navigator, click the Virtual Environment created and select Open Terminal or 
    open command prompt and run conda avtivate <Virtual_environment>) and navigate to the Crawler_Project folder
5.	Once inside the folder please run: C:\Users\<>\Crawler_Project> pip install -r requirements.txt
6.	Once installed please run: C:\Users\<>\Crawler_Project> python manage.py runserver
7.	Once the server is running, please use either of the following :
7.a. Open Postman Collection and import the attached JSON file and try out the APIs 
or
7.b. navigate to the development server at http://127.0.0.1:8000/ and try out the APIs:
        Sample inputs(POST):
        api/get-product-details-view/ : {"sku":"https://www.amazon.in/Pigeon-Stovekraft-Stainless-instant-noodles/dp/B08HRBDLNW/?_encoding=UTF8&pd_rd_w=2tKyO&pf_rd_p=e60c70f0-0541-4ba5-b6fc-ada95198a5fe&pf_rd_r=91ECZN6YQGK02WH9JF6P&pd_rd_r=251ae8cf-5737-49e3-9854-8290366cbe48&pd_rd_wg=S93h0&ref_=pd_gw_crs_zg_bs_976442031"}
        OR {"sku":"B08HRBDLNW”}
       
       ​api/html-view/: {"sku": "B074ZF7PVZ"}

       api/get-product-historydetails-view/ : { "sku": "B074ZF7PVZ", "timestamp": "2021-04-27T23:12"}

       ​api​/price-trend-view​/: {"sku":"B074ZF7PVZ"}
