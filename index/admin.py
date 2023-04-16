from django.contrib import admin
from .models  import Sort,Book,Author,Comment,User,Cart,PayCart,MyOrder

# Register your models here.
admin.site.register(Sort)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(PayCart)
admin.site.register(MyOrder)