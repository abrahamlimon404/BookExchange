from django.http import HttpResponse
from django.shortcuts import render
from .models import MainMenu
from .forms import BookForm
from .models import ShoppingCart
from django.http import HttpResponseRedirect
from .models import Book
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Favorite
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q



from .forms import CommentForm
from .models import Comment


from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url=reverse_lazy('login'))
def index(request):
    return render(request, 'bookMng/index.html',
                  {'item_list': MainMenu.objects.all()})

def aboutus(request):
    return render(request, 'bookMng/aboutus.html',
                  {'item_list': MainMenu.objects.all()})

@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
                book.original_owner = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                      'submitted': submitted
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def searchbook(request):
    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(name__contains=searched)
        for book in books:
            book.pic_path = book.picture.url[14:]

        return render(request,
                     'bookMng/searchbook.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'searched': searched,
                          'book': books})
    else:
        return render(request,
                      'bookMng/searchbook.html',
                      {
                          'item_list': MainMenu.objects.all()}
                          )

@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    user = request.user

    # Get all books
    all_books = Book.objects.all()

    # Filter out duplicates based on all fields except 'username'
    distinct_books = []
    seen_books = set()

    for book in all_books:
        key = (
            book.name,
            book.web,
            book.price,
            book.publishdate,
            book.picture,
            book.pic_path
        )

        # Check if this combination has been seen before
        if key not in seen_books:
            seen_books.add(key)
            distinct_books.append(book)

    for b in distinct_books:
        b.pic_path = b.picture.url[14:]

    return render(request, 'bookMng/displaybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books': distinct_books,
    })


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,'bookMng/mybooks.html',
                  {'item_list': MainMenu.objects.all(),
                   'books': books})

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    comments = Comment.objects.filter(book=book)

    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'comments': comments,
    })
@login_required(login_url='login')
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if the user deleting the book is the creator
    if request.user == book.username:
        # If the current owner is different from the original owner, revert the ownership
        if book.username != book.original_owner:
            book.username = book.original_owner
            book.save()
        else:
            book.delete()  # Delete the book from the database
    else:
        # Remove the book from the user's books only if they own it
        if book in request.user.book_set.all():
            request.user.book_set.remove(book)

    return render(request, 'bookMng/book_delete.html', {'item_list': MainMenu.objects.all(), 'book': book})

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def comments(request):
    commentlist = Comment.objects.all()
    #book = models.ForeignKey(Book, on_delete=models.CASCADE)

    return render(request,
                  'bookMng/comments.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'commentlist': commentlist,

    })

def postcomment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    submitted = False

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.user
            comment.book = book
            comment.save()
            # Manually construct the URL for the book details page
            book_detail_url = f'/book_detail/{book_id}/'
            return redirect(book_detail_url)

    else:
        form = CommentForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'bookMng/postcomment.html', {
        'form': form,
        'item_list': MainMenu.objects.all(),
        'submitted': submitted,
        'book': book
    })

def postcommentpost(request):

    submitted = False
    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            # form.save()
            comment = form.save(commit=False)
            try:
                comment.username = request.user
            except Exception:
                pass
            comment.save()
            return HttpResponseRedirect('/postcommentpost?submitted=True')
    else:
        form = CommentForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postcomment.html',
                 {
                    'form': form,
                    'item_list': MainMenu.objects.all(),
                    'submitted': submitted,

                 })

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def myfavorites(request):
    favorite_books = Favorite.objects.filter(username=request.user)
    books = []
    for fav_item in favorite_books:
        books += Book.objects.filter(id=fav_item.book_id)

    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/myfavorites.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })

def addfavorite(request, book_id):
    # book = Book.objects.get(id=book_id)
    inDB = False

    for entry in Favorite.objects.all():
        if (entry.username == request.user and entry.book_id == book_id):
            inDB = True

    if inDB:
        pass

    else:
        entry = Favorite.objects.create()
        try:
            entry.username = request.user
            entry.book_id = int(book_id)
        except Exception:
            pass
        entry.save()

    return render(request,
                  'bookMng/addfavorite.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })

def deletefavorite(request, book_id):
        favorite_book = Favorite.objects.filter(username=request.user, book_id=book_id)

        favorite_book.delete()
        return redirect(request.META.get('HTTP_REFERER', 'index'))




@login_required(login_url=reverse_lazy('login'))
def viewcart(request):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    books = shopping_cart.books.all()

    total_price = sum(book.price for book in books)

    return render(request,
                  'bookMng/shoppingCart.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'total_price': total_price,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def addtocart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    shopping_cart.books.add(book)

    return redirect('displaybooks')


@login_required(login_url=reverse_lazy('login'))
def deletefromcart(request, book_id):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    book = get_object_or_404(Book, id=book_id)

    if book in shopping_cart.books.all():
        shopping_cart.books.remove(book)
        return redirect('viewcart')

@login_required(login_url='login')
def checkout(request):
    user = request.user
    shopping_cart = ShoppingCart.objects.get(user=user)
    books_to_add = shopping_cart.books.all()

    # Use a transaction to ensure atomicity
    with transaction.atomic():
        for original_book in books_to_add:
            # Update the existing book's username and keep the original_owner the same
            Book.objects.filter(id=original_book.id).update(username=user)

    shopping_cart.books.clear()

    return redirect('mybooks')
