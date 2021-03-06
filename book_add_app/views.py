from django.shortcuts import render, get_object_or_404, redirect, reverse, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from book_share_project.models import Book, Profile, Document
import requests
import os
from book_add_app.forms import AddBookForm, DocumentForm
from .smart_scan import smart_scan
from .google_books import google_books





def book_list_view(request):
    """
        validates if user is logged in, and redirect to the book search page
    """
    if not request.user.is_authenticated:
        return redirect('home')

    # Setting default to google books api search
    return redirect('book_search')


def book_add_search(request):
    """
        Takes user input, validates it to search the list of books from Google API.
        Once receive API response, saves the book information (title, author, description, categories, and image url).
    """
    if not request.user.is_authenticated:
        return redirect('home')

    context = {'results': []}
    if request.method == "POST":

        form = AddBookForm()
        input_value = request.POST.get('query')
        print('here is out input_value', input_value)

        results = google_books(input_value, 4)
        context['results'] = results

    else:
        form = AddBookForm()

    return render(request, 'add/book_add_google.html', {'form': form, 'results': enumerate(context['results'])})



def book_post_view(request):
    """
        when user selects a book, it creates an instance of the book object,
        saves into the db under selected user
    """
    if request.method == "POST":
        # import pdb; pdb.set_trace()
        # TODO: Add this book to book model for that user.
        # user = User()

        fb_account = Profile.objects.filter(user__id=request.user.id)
        fb_id = list(fb_account.values('fb_id'))[0]['fb_id']

        Book.objects.create(
            user=request.user,
            owner=fb_id,
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            image_url=request.POST.get('image_url'),
        )

    return redirect('/add/search')


def book_add_scan(request):
    if not request.user.is_authenticated:
        return redirect('home')

    # Handle file upload
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('book_scan')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    results = []
    if len(documents):
        path = documents[0].docfile.url
        books = smart_scan(path)
        for book in books:
            result = google_books(book, 1)
            if len(result):
                results.append(result[0])
        results = list(reversed(results))

    # Render list page with the documents and the form
    return render(request, 'add/book_add_scan.html', {'documents': documents, 'form': form, 'results': enumerate(results)})

    # return render(request, 'add/book_add_scan.html')

    # def index(request):
    # return render_to_response('myapp/index.html')
