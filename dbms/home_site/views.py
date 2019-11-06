from django.shortcuts import render

# Create your views here.
def home_detail_view(request):
	return render(request,"home_site/detail.html",{})