from django.shortcuts import render, get_object_or_404
from django.db import transaction, IntegrityError

from store.forms import ContactModelForm
from store.models import Album, Artiste, Contact, Booking


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    return render(request, "store/index.html", {
        "albums": albums
    })


def listing(request):
    albums = Album.objects.filter(available=True)
    return render(request, "store/store.html", {
        "albums": albums
    })


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    artistes = album.artistes.all()
    context = {
        'album': album,
        'artistes': artistes,
    }

    if request.method == 'POST':
        form = ContactModelForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)

                    if not contact.exists():
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                    else:
                        contact = contact.first()

                    album = get_object_or_404(Album, pk=pk)
                    booking = Booking.objects.create(
                        contact=contact,
                        album=album
                    )
                    album.available = False
                    album.save()

                    context = {
                        'album_title': album.title
                    }
                    return render(request, 'store/success.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne c'est produite.Merci de recommencer!"

    form = ContactModelForm()
    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, "store/album_detail.html", context)


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)
        if not albums.exists():
            albums = Album.objects.filter(artistes__name__icontains=query)
    title = f"Resultat pour la recherche: {query}"
    context = {
        "albums": albums,
        "title": title
    }
    return render(request, "store/search.html", context)