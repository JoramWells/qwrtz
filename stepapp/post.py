class ProductSearchViewset(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def create(self,request):
        serializer=ProductSearchSerializer(data=request.data)
        searchData = request.data['keyword']

        token_arr=[]
        arr_str=""
        searched_tokens = word_tokenize(searchData)
        for w in searched_tokens:
            if w not in stop_words:
                arr_str.append(w)
            else:
                pass
        product = ProductSearch()
        product.searchTerm=arr_str.join(arr)
        product.min_search=100
        product.save()
        q=ProductSearch.objects.all().order_by('-created_on')[:1]
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


class 


