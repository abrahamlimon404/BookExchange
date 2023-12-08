from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('searchbook', views.searchbook, name='searchbook'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('comments', views.comments, name='comments'),
    path('postcommentpost', views.postcommentpost, name="postcommentpost"),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('mybooks/postcomment/<int:book_id>', views.postcomment, name="postcomment"),
    path('displaybooks/postcomment/<int:book_id>', views.postcomment, name="postcomment"),
    path('book_detail/postcomment/<int:book_id>', views.postcomment, name="postcomment"),
    path('myfavorites', views.myfavorites, name='myfavorites'),
    path('addfavorite/<int:book_id>', views.addfavorite, name='addfavorite'),
    path('deletefavorite/<int:book_id>', views.deletefavorite, name='deletefavorite'),
    path('shoppingcart', views.viewcart, name='viewcart'),
    path('addtocart/<int:book_id>', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:book_id>', views.deletefromcart, name='deletefromcart'),
    path('checkout/', views.checkout, name='checkout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)