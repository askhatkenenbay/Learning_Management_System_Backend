from django.shortcuts import render

def chal_list(request):
    return render(request,'list.html')

def breath(request):
	return render(request, 'breath.html')

def yoga(request):
	return render(request, 'yoga.html')

def friends(request):
	return render(request, 'friends.html')

def parents(request):
	return render(request, 'parents.html')

def floormate(request):
	return render(request, 'floormate.html')

def good(request):
	return render(request, 'good.html')


