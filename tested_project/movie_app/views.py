from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Category, Review
from .forms import movieform, ReviewForm
from django.contrib import messages, auth


# Create your views here.
def index(request,c_slug=None):
    c_page = None
    movies = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movies = Movie.objects.all().filter(category=c_page, available=True)
    else:
        movies = Movie.objects.all().filter(available=True)

    return render(request,'index.html',{'category':c_page,'movie':movies})

def details(request,movie_id):
    movienew=Movie.objects.get(id=movie_id)
    return render(request,'details.html',{'movie':movienew})
    # return HttpResponse('this is movie numner %s'% movie_id)
def add_movie(request):
    if request.method=='POST':
        name=request.POST.get('name',)
        slug = request.POST.get('slug',)
        cast = request.POST.get('cast',)
        available = request.POST.get('available',)
        desc=request.POST.get('desc',)
        date=request.POST.get('date',)
        img=request.FILES['img']
        category_name = request.POST.get('category',)
        trailer_link= request.POST.get('trailer_link',)
        usr=User.objects.get(id=request.user.id)

        if category_name:

            category_obj, _ = Category.objects.get_or_create(name=category_name, defaults={
                'slug': category_name})  # Create a slug if needed
        else:

            return HttpResponse('Category name is required')
        if available is None:
            available = False
        movie1=Movie(name=name,desc=desc,date=date,img=img,user=usr,slug=slug,cast=cast,available=available,category=category_obj,trailer_link=trailer_link)
        movie1.save()


    return render(request,'add.html')


def update(request, id):
    # Retrieve the movie object
    try:
        movienew = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        messages.error(request, "Movie does not exist.")
        return redirect('/')

    # Check if the logged-in user is the owner of the movie
    if movienew.user != request.user:
        messages.error(request, "You are not authorized to update this movie.")
        return redirect('/')

    # Proceed with updating the movie
    forms = movieform(request.POST or None, request.FILES, instance=movienew)
    if forms.is_valid():
        forms.save()
        messages.success(request, "Movie updated successfully.")
        return redirect('/')

    return render(request, 'edit.html', {'movie': movienew, 'forms': forms})


def delete(request, id):
    # Retrieve the movie object
    movie_to_delete = get_object_or_404(Movie, id=id)

    # Check if the logged-in user is the owner of the movie
    if movie_to_delete.user != request.user:
        messages.error(request, "You are not able to delete this movie.")
        return redirect('/')

    # Proceed with deleting the movie
    if request.method == 'POST':
        movie_to_delete.delete()
        messages.success(request, "Movie deleted successfully.")
        return redirect('/')

    return render(request, 'delete.html', {'movie': movie_to_delete})
def review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user  # Set the logged-in user for the review
            review.save()

    else:
        form = ReviewForm()

    return render(request, 'review.html', {'movie': movie, 'reviews': reviews, 'form': form})
