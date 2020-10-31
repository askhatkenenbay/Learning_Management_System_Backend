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
<<<<<<< HEAD
	return render(request, 'floormate.html')

def good(request):
	return render(request, 'good.html')

=======
	return render(request, 'floormate.html')
>>>>>>> 6fe32a8ed11b0d70961d2a4bbfd516173f7a9228
