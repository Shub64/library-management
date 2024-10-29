from django.shortcuts import render, redirect  
from django.http import HttpResponse 
from django.template import loader
from .models import books, users, issued_books
from django.views.decorators.http import require_POST 
from django.db.models import Q  
from datetime import date  
from django.shortcuts import render, get_object_or_404  


@require_POST   
def submit_page(request):  
    form_type = request.POST.get('form_type')  
        
    if form_type == 'searchbook_form':    
        Bookname = request.POST.get('Bookname')
        x=str(Bookname)
        Author = request.POST.get('Author')
        y=str(Author)   
        mybook = books.objects.filter(book_name__icontains=x,author_name__icontains=y).values()
        template=loader.get_template('newapp/searchbook.html')
        content = {
            'mybook': mybook,
        }  
        return HttpResponse(template.render(content, request))

    elif form_type == 'viewbooks_form':
        Genre = request.POST.get('Category')
        Bookname1 = request.POST.get('Bookname')
        genstr=str(Genre)
        x=str(Bookname1)
        if x=='' and genstr != '':
            if genstr == 'Other':
                mybook=books.objects.filter(Q(genre__isnull=True) | Q(genre='')).values()

            else:
                mybook=books.objects.filter(genre__icontains=genstr).values()

            return render(request, 'newapp/viewbooks.html', {'mybook': mybook})
        
        elif x!='' and genstr == '':
            mybook=books.objects.filter(book_name__icontains=x).values()
            return render(request, 'newapp/viewbooks.html', {'mybook': mybook})
        
        elif x=='' and genstr =='':
            return render(request, 'newapp/viewbooks.html')
        
        else:
            if genstr == 'Other':
                mybook=books.objects.filter(Q(genre__isnull=True) | Q(genre='')).values()

            else:
                mybook = books.objects.filter(Q(book_name__icontains=x)|Q(genre__icontains=genstr)).values()  
            return render(request, 'newapp/viewbooks.html', {'mybook': mybook})
        
    elif form_type == 'issuebook_form':
        Bookname = request.POST.get('Bookname')
        BookID = request.POST.get('BookID')
        current_date = date.today()
        Bookname1=str(Bookname)
        z=int(BookID)
        mybook = books.objects.filter(book_name__icontains=Bookname1,book_id=z).first()
        content = {
            'current_date':current_date,
        }
        if mybook:    
            mybook_dict = {  
                'book_id': mybook.book_id,  
                'book_name': mybook.book_name,  
                'author_name': mybook.author_name,  
                'edition': mybook.edition,  
            }  
            book = get_object_or_404(books,book_id=z)
            add_book=issued_books(book_id=book.book_id,book_name=book.book_name,author_name=book.author_name,edition=book.edition,genre=book.genre,issued_date=current_date)
            add_book.save()  
            book.delete()  
            content['mybook'] = [mybook_dict]    
        else:  
            content['mybook'] = []   

        return render(request, 'newapp/issuebook.html', content) 

    elif form_type == 'login_form':
        Username = request.POST.get('username')
        Pass_wd = request.POST.get('password')
        US = str(Username)
        PS=str(Pass_wd)
        myuser = users.objects.filter(User_Name=US,Pass_word=PS).first()
        if myuser:
            return redirect('Home')
        else:
            return render(request,'newapp/login.html')
        
    elif form_type == 'register_form':
        Username=request.POST.get('username')
        Pass_wd=request.POST.get('password')
        BirthD=request.POST.get('Birthday')
        Contact=request.POST.get('contact')
        Cont = str(Contact)
        add_user=users(User_Name=Username,Pass_word=Pass_wd,contact_details=Cont,user_birthday=BirthD)
        add_user.save()
        return redirect('login')

    elif form_type == 'returnbook_form':
        BOOKid = request.POST.get('BookID')
        action = request.POST.get('submit_action')
        Bid=int(BOOKid)
        mybook = issued_books.objects.filter(book_id=Bid).first()
        if mybook:
            context = {}
            if action == 'Check':
                issueddate = mybook.issued_date
                current_date = date.today()
                penalty = 0
                difference = (current_date - issueddate).days
                if difference > 7:
                    penalty_days = 7 
                    penalty= difference*penalty_days

                context["penalty"] =penalty
                book1 = issued_books.objects.all()
                context['mybook']=book1
                
            if action == 'Return':
                book = get_object_or_404(issued_books,book_id=Bid)
                add_book=books(book_id=book.book_id,book_name=book.book_name,author_name=book.author_name,edition=book.edition,genre=book.genre)
                add_book.save()  
                book.delete()
                book1 = issued_books.objects.all()  
                context['mybook']=book1
                context['book']=mybook

            return render(request, 'newapp/returnbook.html', context)

        return render(request, 'newapp/returnbook.html')
        

    else:
        return HttpResponse("Invalid form type.")    

def searchbook(request):  
    return render(request, 'newapp/searchbook.html')

def viewbooks(request):  
    return render(request, 'newapp/viewbooks.html')

def issuebook(request):  
    return render(request, 'newapp/issuebook.html')

def login(request):  
    return render(request, 'newapp/login.html')

def registeration(request):  
    return render(request, 'newapp/registeration.html')

def home1(request):  
    return render(request, 'newapp/home1.html')

def Home(request):
    return render(request,'newapp/Home.html')

def returnbook(request): 
    book = issued_books.objects.all()  
    context = {  
        "mybook": book  
    }  
    return render(request, 'newapp/returnbook.html', context) 

