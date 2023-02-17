from django.shortcuts import render,redirect
from .models import Image
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Create your views here.
from django.http import HttpResponseNotAllowed

def my_view(request):
    if request.method == "POST":
        # if the post request has a file under the input name 'document', then save the file.
        if 'images' in request.FILES:
            request_file = request.FILES.getlist('images')
            # request_file = request.FILES['images']
            # print(len(request_file))
        else:
            request_file =None
        if request_file:
            # save attached file
            img_url_store = []
            for img in request_file:
                # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                # the file_url variable now contains the url to the file. This can be used to serve the file when needed.
                file = fs.save(img.name, img)
                file_url = fs.url(file)
                img_url_store.append(file_url)
            # print(img_url_store)
       
            final_url = ','.join(img_url_store)
            # print("final url", final_url)
            record = Image(image=final_url)
           
            record.save()
            messages.success(request,'Uploaded Successfully !!')  

            # print(file_url)
        
    images = Image.objects.all()
    # print(images,"oooooooooooooooooooooooooooooo")

    all_image = []
    for first_ob in images:
        lst = first_ob.image.split(',')
        img_id=first_ob.id
        # print(lst,"llllllllllllllllllllllllllllllllllllllllllllllllllll")
        # print(img_id,"iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        img_lst=[]
        img_lst.append(img_id)
        print(img_lst)
        for i in lst:
            img_lst.append(i)
        all_image.append(img_lst)
        # all_image=[j[1:] for j in all_image]
       
    print("qqqqqqqqqqqqqqqqqqqqqqqqqqq:  ", all_image)

    return render(request, "index.html", {'final_images': all_image })


def update_image(request, id):
    if request.method == "POST":
        image_name = request.POST['image_name']
        # print("Image name is:---------",image_name)
        new_file = request.FILES.get('new_images')
        # print("New file is :*********************",new_file)

        # retrieve the image record by ID
        image = Image.objects.get(id=id)
        # print("iiiiiiiiiiiiiiiiiiiiiiiii",image)

        # split the image field by comma to get a list of URLs
        image_urls = image.image.split(',')
        # print(image_urls,"UUUUUUUUUUUUUUUUUUUUUUUU")

        # find the index of the old image URL to be replaced
        old_url_index = image_urls.index(image_name)
        # print("ooooooooooooooooooooooooooooooo",old_url_index)

        # if a new file was uploaded, replace the old URL with the new URL
        if new_file:
            fs = FileSystemStorage()
            file_name = fs.save(new_file.name, new_file)
            # print("new_file.name:   ",new_file.name)
            # print("new_file:@@@@@@@@@@@@@@@@@@@",new_file)
            # print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV",file_name)
            file_url = fs.url(file_name)
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",file_url )
            image_urls[old_url_index] = file_url
        # else:
        #     # if no new file was uploaded, just remove the old URL
        #     image_urls.pop(old_url_index)
        # # join the list of URLs back into a comma-separated string
        new_image_field = ','.join(image_urls)
        # print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn:",new_image_field)
        # update the image record with the new image field value
        image.image = new_image_field
        # print("imimimimimimimimimimimimimi: ",image.image)
        image.save()
        messages.success(request,'Updated Successfully !!')  

        return redirect('bulk_upload')

# def update_image(request, file_path):
#     image=None
#     if request.method == "POST":
#         # retrieve the image record by ID
#         image = Image.objects.get(id=file_path)
#         print(image,"..................")
#         # save the new image file
#         if 'images' in request.FILES:
#             request_file = request.FILES['images']
#             print(request_file)
#             fs = FileSystemStorage()
#             print(fs)
#             file = fs.save(request_file.name, request_file)
#             file_url = fs.url(file)
#             # update the image record with the new file URL
#             image.image = file_url
#             image.save()
#             return redirect('update_image')

#     return render(request, 'update_image.html', {'file_path': file_path})

def delete_image(request, id):
    if request.method == 'POST':
        print("yyyyyyyyyyyyyyyyyyyyyyyy")
        image_name = request.POST['image_delete']
        print('image_name:___________________',image_name)
        # get the image from the database
        images = Image.objects.get(id=id)
        print(images,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        img_value=images.image
        delete_img=img_value.split(',')
        print(delete_img,"bbbbbbbbbbbbbbbeeeeeeeeeeeeeeeeeeeeeeee")
        delete_img.remove(image_name)
        print(delete_img,"-----------------------------------------------------")
        new_value=','.join(delete_img)
        print(new_value,"mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
        images.image = new_value
        print(images.image,"llllllllllllllllllllllllllll")
        images.save()
        if not images.image:
                images.delete()

        # print('ajkadnjkanakjnkjnjkn',new_value)
        # redirect to the index page
        messages.success(request,'Deleted Successfully !!')  
        return redirect('bulk_upload')
        
    return render(request,'index.html')


# def delete_image(request, id):
#     if request.method == 'POST':
#     # get the image from the database
#         # image = get_object_or_404(Image, pk=pk)
#         image = Image.objects.get(Image,id=id)
#         print(image,"hjdbsdbnhfcsdfkcsjdcnfodkl")
#         image.delete()
#         # redirect to the index page
#         return redirect('/delete_image/')
#     return render(request,'index.html', {'images': image})


# def delete_image(request, id):
#     if request.method == 'POST':
#         # get the image from the database
#         image = Image.objects.get(id=id)
#         # delete the image file from the file system

#         image_urls = image.image.split(',')
#         for url in image_urls:
#             fs = FileSystemStorage()
#             file_path = url.replace('/media/', '')
#             if fs.exists(file_path):
#                 fs.delete(file_path)
#         # delete the image record from the database
#         image.delete()
#         # redirect to the index page
#         return redirect('bulk_upload')
#     else:
#         # if the request method is not POST, return a 405 Method Not Allowed error
#         return HttpResponseNotAllowed(['POST'])
