import os
from django.shortcuts import render
from django.conf import settings
from .utils import huffman_compress, encode_stego, decode_stego

def home(request):
    return render(request, 'core/home.html')

def encode_view(request):
    if request.method == "POST":
        img = request.FILES.get('image')
        msg = request.POST.get('message')
        
        # Save temp upload
        path = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(path, 'wb+') as f:
            for chunk in img.chunks(): f.write(chunk)
            
        # Process
        bin_data, codes = huffman_compress(msg)
        out_name = "encoded_" + img.name.split('.')[0] + ".png"
        out_path = os.path.join(settings.MEDIA_ROOT, out_name)
        
        encode_stego(path, bin_data, codes, out_path)
        return render(request, 'core/encode.html', {'result': out_name})
    return render(request, 'core/encode.html')

def decode_view(request):
    if request.method == "POST":
        img = request.FILES.get('image')
        path = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(path, 'wb+') as f:
            for chunk in img.chunks(): f.write(chunk)
            
        decoded_text = decode_stego(path)
        return render(request, 'core/decode.html', {'message': decoded_text})
    return render(request, 'core/decode.html')