# import os
# from django.shortcuts import render
# from django.conf import settings
# from .utils import huffman_compress, encode_stego, decode_stego

# def home(request):
#     return render(request, 'core/home.html')

# def encode_view(request):
#     if request.method == "POST":
#         img = request.FILES.get('image')
#         msg = request.POST.get('message')
        
#         # Save temp upload
#         path = os.path.join(settings.MEDIA_ROOT, img.name)
#         with open(path, 'wb+') as f:
#             for chunk in img.chunks(): f.write(chunk)
            
#         # Process
#         bin_data, codes = huffman_compress(msg)
#         out_name = "encoded_" + img.name.split('.')[0] + ".png"
#         out_path = os.path.join(settings.MEDIA_ROOT, out_name)
        
#         encode_stego(path, bin_data, codes, out_path)
#         return render(request, 'core/encode.html', {'result': out_name})
#     return render(request, 'core/encode.html')

# def decode_view(request):
#     if request.method == "POST":
#         img = request.FILES.get('image')
#         path = os.path.join(settings.MEDIA_ROOT, img.name)
#         with open(path, 'wb+') as f:
#             for chunk in img.chunks(): f.write(chunk)
            
#         decoded_text = decode_stego(path)
#         return render(request, 'core/decode.html', {'message': decoded_text})
#     return render(request, 'core/decode.html')

import os
from django.shortcuts import render
from django.conf import settings
from .utils import huffman_compress, encode_stego, decode_stego, cleanup_old_files

def home(request):
    cleanup_old_files(settings.MEDIA_ROOT) # Cleanup trigger
    return render(request, 'core/home.html')

def encode_view(request):
    cleanup_old_files(settings.MEDIA_ROOT) # Cleanup trigger
    if request.method == "POST":
        img = request.FILES.get('image')
        msg = request.POST.get('message')
        
        # Save temp upload
        path = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(path, 'wb+') as f:
            for chunk in img.chunks(): f.write(chunk)
            
        # Process
        bin_data, codes = huffman_compress(msg)
        out_name = "encoded_" + "".join(img.name.split('.')[:-1]) + ".png"
        out_path = os.path.join(settings.MEDIA_ROOT, out_name)
        
        encode_stego(path, bin_data, codes, out_path)
        
        # Remove the original uploaded (unencoded) file to save space
        if os.path.exists(path):
            os.remove(path)
            
        return render(request, 'core/encode.html', {'result': out_name})
    return render(request, 'core/encode.html')

def decode_view(request):
    cleanup_old_files(settings.MEDIA_ROOT) # Cleanup trigger
    if request.method == "POST":
        img = request.FILES.get('image')
        path = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(path, 'wb+') as f:
            for chunk in img.chunks(): f.write(chunk)
            
        try:
            decoded_text = decode_stego(path)
        except Exception:
            decoded_text = "Error: Could not decode. Is this a valid StegoHuff image?"
            
        # Remove the file after decoding to keep server clean
        if os.path.exists(path):
            os.remove(path)
            
        return render(request, 'core/decode.html', {'message': decoded_text})
    return render(request, 'core/decode.html')