from django.shortcuts import render

def mainpage(request):
    if request.method == "POST":
        return render(
            request,
            "subpage.html"
        )

    return render(
        request,
        "mainpage.html"
    )

def subpage(request):
    return render(
        request,
        "subpage.html"    
    )