from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .models import Cat, Toy
from .forms import FeedingForm


# Create your views here.
class Home(LoginView):
    template_name = "home.html"


def about(request):
    response = requests.get("https://catfact.ninja/fact")
    return render(request, "about.html", {"fact": response.json().get("fact")})


@login_required
def cat_index(request):
    cats = Cat.objects.filter(user=request.user)
    return render(request, "cats/index.html", {"cats": cats})


def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toy_ids_cat_has = cat.toys.all().values_list("id")
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=toy_ids_cat_has)
    feeding_form = FeedingForm()
    return render(
        request,
        "cats/detail.html",
        {"cat": cat, "feeding_form": feeding_form, "toys": toys_cat_doesnt_have},
    )


@login_required
def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect("cat-detail", cat_id=cat_id)


@login_required
def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole toy object
    # cat = Cat.objects.get(id=cat_id)
    # cat.toys.add(toy_id)
    # same as above 2 lines
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect("cat-detail", cat_id=cat_id)


@login_required
def remove_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect("cat-detail", cat_id=cat_id)


def signup(request):
    error_message = ""
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect("cat-index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "signup.html", context)
    # Same as:
    # return render(
    #     request,
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )


class CatCreate(CreateView, LoginRequiredMixin):
    model = Cat
    fields = ["name", "breed", "description", "age"]

    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class CatUpdate(UpdateView, LoginRequiredMixin):
    model = Cat
    fields = ["breed", "description", "age"]


class CatDelete(DeleteView, LoginRequiredMixin):
    model = Cat
    success_url = "/cats/"  # Redirect to the index page for cats after a cat is deleted


class ToyCreate(CreateView, LoginRequiredMixin):
    model = Toy
    fields = "__all__"


class ToyList(ListView, LoginRequiredMixin):
    model = Toy


class ToyDetail(DetailView, LoginRequiredMixin):
    model = Toy


class ToyUpdate(UpdateView, LoginRequiredMixin):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(DeleteView, LoginRequiredMixin):
    model = Toy
    success_url = "/toys/"
