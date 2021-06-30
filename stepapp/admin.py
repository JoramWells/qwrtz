from django.contrib import admin
from .models import Post,Csv,XmlModel,Product,ProductSearch

admin.site.register(XmlModel)
admin.site.register(Post)
admin.site.register(Csv)
admin.site.register(Product)
admin.site.register(ProductSearch)



