from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from ..models import Book, Profile
import requests
import os


def book_list_view(request):
    # Instead of permission denied, consider a redirect to the home page.
    if not request.user.is_authenticated:
        raise PermissionDenied

    profile = Profile.objects.filter(
        user__id=request.user.id
        )

    fb_id = list(profile.values('fb_id'))[0]['fb_id']

    endpoint = 'https://graph.facebook.com/{}?fields=friends'.format(fb_id)
    headers = {'Authorization': 'Bearer {}'.format(os.environ.get('FB_GRAPH_TOKEN'))}
    response = requests.get(endpoint, headers=headers).json()

    friends_data = response['friends']['data']
    friends = []
    for friend in friends_data:
        friends.append(friend['id'])

    profile.update(friends=friends)
    all_books = []
    for friend in friends:
        books = Book.objects.filter(owner=friend)
        friend_profile = Profile.objects.filter(fb_id=friend)
        # import pdb; pdb.set_trace()
        if len(friend_profile):
            friend_name = list(friend_profile.values('first_name'))[0]['first_name'] + ' ' + list(friend_profile.values('last_name'))[0]['last_name']

        if len(books):
            for book in books.values():
                book_obj = {
                    'title': book['title'],
                    'author': book['author'],
                    'owner': friend_name
                    }
                all_books.append(book_obj)

    context = {
        'books': all_books
    }



    return render(request, 'books/book_list.html', context)


# def book_detail_view(request, pk=None):
#     if not request.user.is_authenticated:
#         return redirect(reverse('login'))

#     book = get_object_or_404(Book, id=pk, user__username=request.user.username)

#     context = {
#         'book': book,
#     }

#     return render(request, 'books/book_detail.html', context)