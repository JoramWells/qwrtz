from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.parsers import MultiPartParser,FileUploadParser,FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,status
from .serializers import PostSerializer,XmlSerializer,CsvSerializer,ProductSerializer,ProductSearchSerializer
from compression_middleware.decorators import compress_page
from .models import Post,XmlModel,Csv,Product,ProductSearch
from rest_framework.permissions import IsAuthenticated
import xml.etree.ElementTree as et
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from .forms import CsvModelForm
from .modules import *
import csv
from django.db import migrations, models

from json import dumps


queryset = XmlModel.objects.all()
d3Queryset = Product.objects.all()

stop_words = set(stopwords.words('english'))
def home(request):
    return render(request,'index.html')

def index(request):
    path = './cancer.xml'
    xtree = et.parse(path)
    xroot = xtree.getroot()
    for child in xroot:
        text = child.text.replace(',','')
        text = text.split()
        text = ' '.join(text) 
        XmlModel.objects.create(
            description= text
        )
        # print(child.text)
    render(request,'index.html')




# Requesting all the data from the database
class XmlViewset(viewsets.ViewSet):
    permission_classes=(IsAuthenticated, )
    def list(self,request):
        # authenticated user
        print(request.user)
        print(get_current_site(request))
        # get all requests of a specific user
        posts = XmlModel.objects.filter(user=request.user)
        serializer = XmlSerializer(posts,many=True)
        return Response(serializer.data)

# Requesting all the data from do3ens model
class ProductViewset(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        print(request.user)
        print(get_current_site(request))
        products = Product.objects.filter(user=request.user)
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)



#Save a query to csv, makes it easy to work with dataframes for nlp
def query_to_csv(queryset, filename='items.csv', **override):
    field_names = [field.name for field in queryset.model._meta.fields]
    def field_value(row, field_name):
        if field_name in override.keys():
            return override[field_name]
        else:
            return row[field_name]
    with open(filename, 'w+', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
        writer.writerow(field_names) 
        for row in queryset.values(*field_names):
            writer.writerow([field_value(row, field) for field in field_names])


#POST search queries
class PostViewSet(viewsets.ViewSet):
    permission_classes=(IsAuthenticated, )
    def create(self,request):
        serializer = PostSerializer(data=request.data)
        searchData = request.data['keyword']
        
        # Array to store tokenized input
        arr = []

        # Str to store arr
        str1 = " "

        # Tokenize the input 'Tokenize', 'the' 'input'
        searched_tokens = word_tokenize(searchData)

        # Removing stop words from the tokenized input
        for w in searched_tokens:
            if w not in stop_words:

                # Append non-stop words to arr
                arr.append(w)
            else:
                pass

        
        post=Post()
        post.keyword =str1.join(arr)
        post.min_videos = 100 #request.POST.get('videos')
        post.save()
        q = Post.objects.all().order_by('-created_on')[:1]

        # save the query to serchin.csv
        query_to_csv(q, filename='serchin.csv', user=1, group=1)
        d = read_data('serchin.csv')
        key = d['keyword']
        key = key[0]
        url = d['min_videos']
        url =url[0]

        # if the searched object is not found
        if str(key) == "nan":
            return Response('')
        else:
            s1 = SearchView( key,url)
            s2 = s1.postl()
            print(s2)
    

        if len(s2) == 0:
            return Response('')
        url=[]
        for i in s2:
            c=XmlModel.objects.get(pk=i)
            url.append(XmlSerializer(c).data )
            context={
                'url':url
                }
            
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(url)


# do3ens POST search queries

class ProductSearchViewset(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    # get recently searched items
    def list(self,request):
        search = ProductSearch.objects.all()
        serializer=ProductSearchSerializer(search,many=True)
        print(serializer)
        return Response(serializer.data)
    def create(self,request):
        serializer=ProductSearchSerializer(data=request.data)
        searchData = request.data['searchTerm']
        userInfo = request.data['userInfo']


        token_arr=[]

        # Space separator *****
        arr_str=" "
        searched_tokens = word_tokenize(searchData)

        # Remove stop word *****
        for w in searched_tokens:
            if w not in stop_words:
                token_arr.append(w)
            else:
                pass
        product = ProductSearch()
        product.userInfo = userInfo
        product.searchTerm=arr_str.join(token_arr)
        product.min_search=100
        product.save()
        q=ProductSearch.objects.all().order_by('-creted_on')[:1]
        query_to_csv(q,filename='do3ens.csv', user=1,group=1)
        d=read_data('do3ens.csv')
        key=d['searchTerm']
        key=key[0]
        url=d['min_search']
        url=url[0]
        if str(key)=="nan":
            return Response('')
        else:
            s1=SearchView(key,url)
            s2=s1.postl()
            print(s2)
        if len(s2) == 0:
            return Response('')
        url=[]
        for i in s2:
            c=Product.objects.get(pk=i)
            url.append(ProductSerializer(c).data)
            context={
                'url':url
            }
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(url)


class CsvViewSet(APIView):

    # Authenticate the request
    permission_classes=(IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)
    def post(self, request, format=None):

        # Save the csv files to media
        Csv.objects.create(file_name=request.data['file'])

        #Get activated csv true
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path,'r') as f:
            reader = csv.reader(f)
            for i,row in enumerate(reader):

                # If its an empty csv is file, pass
                if len(row) == 0:
                    pass
                else:
                    # row = "".join(row)
                    # row = row.split(",")
                    # row = row.split()
                    # product = len(row)
                    Product.objects.create(
                        user=request.user,
                        productName = row[1],
                        price = row[3],
                        image=row[7],
                        description=row[10]
                    )
                    
                    # print(len(row))
                    # print(type(row))
                    print(row)
                    # print(request.user)

        # After reading, set activated to true
        obj.activated = True

        #Save the activated object
        obj.save()
        # serializer = CsvSerializer(data=request.data['file'])
        # print(request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(status=200)

# def create_model(name,fields=None,app_label='',module='',options=None,admin_opts=None):
#     class Meta:
#         pass
#     if app_label:
#         setattr(Meta,'app_label',app_label)
#     if options is not None:
#         for key,value in options.iteritems():
#             setattr(Meta,key,value)
#     attrs = {'__module__':module,'Meta':Meta}
#     if fields:
#         attrs.update(fields)
#     model=type(name,(models.Model,), attrs)
#     if admin_opts is not None:
#         class Admin(admin.ModelAdmin):
#             pass
#         for key,value in admin_opts:
#             setattr(Admin,key,value)
#         admin.site.register(model,Admin)
#     return model







query_to_csv(d3Queryset, filename='dozenske.csv', user=1, group=1)

