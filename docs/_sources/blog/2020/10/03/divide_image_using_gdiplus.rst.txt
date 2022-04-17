:og:description: Divide an image into multiple blocks with fixed height and width using Gdiplus in C++
:og:keywords: Image divide, C++, Gdiplus, GDI+, Win32, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/divide_image_using_gdiplus.png
:og:image:alt: divide an image into blocks using gdi+ in c++

Divide an image into blocks using GDI+ in C++
=============================================

.. post:: October 03, 2020
  :tags: Cplusplus, Gdiplus, Windows
  :category: Image processing, 2020
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

In the previous blog, we used OpenCV to divide an image into multiple blocks of a certain height and width, which is useful when we need to apply a certain image transformation block-wise.
This blog will provide an alternative implementation using the Windows API, specifically the `GDI+`_ library.

Approach
~~~~~~~~
Similarly to the approach introduced in the previous blog (`Divide an image into blocks using OpenCV in C++`_) using OpenCV, this alternative aims to crop the blocks one by one after computing their coordinates and dimensions.
At the same time, we will make sure to crop the side blocks and lower blocks correctly even if their dimensions are different than other blocks.

  From `Divide an image into blocks using OpenCV in C++`_:

  *To elaborate on this a bit more: if the image width = 512 px and the block width = 128 px -> we will get 512 / 128 = 4 blocks.
  However if the image width = 576 px and the block width = 128 px -> we should get 4 blocks with 128 px and 1 block with width 64 px.
  Therefore on each loop we need to check/ compute the block dimensions.*


Similarly, we also use while loops in this alternative to keep the code fast and optimal.
The previously described code is implemented in the following snippet:


.. code-block:: C++
  :linenos:

  #include <Windows.h>
  #include <minmax.h>
  #include <gdiplus.h>
  #include <SDKDDKVer.h>
  #pragma comment(lib,"gdiplus.lib")
  #include "atlimage.h"


  bool saveToMemory(Gdiplus::Bitmap* tile, std::vector<BYTE>& data, std::string dataFormat)
  {
    // write to IStream
    IStream* istream = nullptr;
    CreateStreamOnHGlobal(NULL, TRUE, &istream);

    // define encoding
    CLSID clsid;
    if (dataFormat.compare("bmp") == 0)
    {
      CLSIDFromString(L"{557cf400-1a04-11d3-9a73-0000f81ef32e}", &clsid);
      Gdiplus::Status status = tile->Save(istream, &clsid, NULL);
      if (status != Gdiplus::Status::Ok)
        return false;
    }
    else if (dataFormat.compare("jpg") == 0)
    {
      CLSIDFromString(L"{557cf401-1a04-11d3-9a73-0000f81ef32e}", &clsid);
      // Before we call Image::Save, we must initialize an EncoderParameters object.
      // The EncoderParameters object has an array of EncoderParameter objects.
      // In this case, there is only one EncoderParameter object in the array.
      // The one EncoderParameter object has an array of values.
      // In this case, there is only one value (of type ULONG)
      Gdiplus::EncoderParameters encoderParameters;
      encoderParameters.Count = 1;
      encoderParameters.Parameter[0].Guid = Gdiplus::EncoderQuality;
      encoderParameters.Parameter[0].Type = Gdiplus::EncoderParameterValueTypeLong;
      encoderParameters.Parameter[0].NumberOfValues = 1;

      // Save the image as a JPEG with quality level 0.
      int quality = 70;
      encoderParameters.Parameter[0].Value = &quality;

      Gdiplus::Status status = tile->Save(istream, &clsid, &encoderParameters);
      if (status != Gdiplus::Status::Ok)
        return false;
    }
    else if (dataFormat.compare("png") == 0)
    {
      CLSIDFromString(L"{557cf406-1a04-11d3-9a73-0000f81ef32e}", &clsid);
      Gdiplus::Status status = tile->Save(istream, &clsid, NULL);
      if (status != Gdiplus::Status::Ok)
        return false;
    }

    // get memory handle associated with istream
    HGLOBAL hg = NULL;
    GetHGlobalFromStream(istream, &hg);

    // copy IStream to buffer
    int bufsize = GlobalSize(hg);
    data.resize(bufsize);

    // lock & unlock memory
    LPVOID pimage = GlobalLock(hg);
    if (pimage != 0)
      memcpy(&data[0], pimage, bufsize);

    GlobalUnlock(hg);
    istream->Release();
    return true;
  }

  int gdiplusDivideImage(Gdiplus::Bitmap* img, const int blockWidth, const int blockHeight, std::vector<std::vector<BYTE>>& blocks)
  {
    int imgWidth = img->GetWidth();
    int imgHeight = img->GetHeight();

    int bhSize = 0;
    int bwSize = 0;
    int blockId = 0;
    int y0 = 0;

    while (y0 < imgHeight)
    {
      bhSize = ((y0 + blockHeight) > imgHeight) * (blockHeight - (y0 + blockHeight - imgHeight)) + ((y0 + blockHeight) <= imgHeight) * blockHeight;

      int x0 = 0;
      while (x0 < imgWidth)
      {
        bwSize = ((x0 + blockWidth) > imgWidth) * (blockWidth - (x0 + blockWidth - imgWidth)) + ((x0 + blockWidth) <= imgWidth) * blockWidth;
        blockId += 1;

        Gdiplus::Bitmap* bmp = img->Clone(x0, y0, bwSize, bhSize, PixelFormat24bppRGB);

        // encode block
        std::vector<BYTE> pngbytes;

        // encode block
        if (!(saveToMemory(bmp, pngbytes, "png")))
        {
          std::cout << "Cannot save block_" << std::to_string(x0) << "_" << std::to_string(y0) << "to png" << std::endl;
          return EXIT_FAILURE;
        }
        // update starting coordinates
        x0 = x0 + blockWidth;

        // append to vec
        blocks.push_back(pngbytes);
      }
      // update starting coordinates
      y0 = y0 + blockHeight;
    }
    return EXIT_SUCCESS;
  }


The previous snippet includes two main functions:

- :code:`saveToMemory()` : used to save the image bytes to the memory using a specific encoding.
- :code:`gdiplusDivideImage()` : divides an input image into blocks with an integer output reflecting the run status of the function.

The main call
~~~~~~~~~~~~~~
Let's call the previous function in a main function and save the resulting blocks in a defined directory to visualize the results and verify, that the code is doing what it is supposed to.
For the purpose of this test I chose to use the famous Lenna picture, that can downloaded from here_.
In code this can be done as follows:

.. code-block:: C++
  :linenos:

  int main()
  {
    // initilialize GDI+
    CoInitialize(NULL);
    ULONG_PTR token;
    Gdiplus::GdiplusStartupInput tmp;
    Gdiplus::GdiplusStartup(&token, &tmp, NULL);

    // init vars
    std::vector<std::vector<BYTE>> imgblocks;

    // load img
    Gdiplus::Bitmap* bitmap = Gdiplus::Bitmap::FromFile(L"Lenna.png");

    // divide img
    int divstatus = gdiplusDivideImage(bitmap, blockw, blockh, imgblocks);

    // create repository for blocks
    if (!CreateDirectory(L"blocksFolder", NULL))
    {
      std::wcout << "Directory Error: Cannot create directory for blocks." << std::endl;
      return 1;
    }

    // save blocks
    for (int j = 0; j < imgblocks.size(); j++)
    {
      std::string blockId = std::to_string(j);
      std::string blockImgName = "blocksFolder/block#" + blockId + ".png";

      // write from memory to file for testing:
      std::ofstream fout(blockImgName, std::ios::binary);
      fout.write((char*)imgblocks[j].data(), imgblocks[j].size());
    }
    return 0;
  }

The full code can be found in this `gist: DivideImageUsingGdiplus.cpp`_.

Result
~~~~~~
The resulting blocks should look something like this:

.. image:: ../../../../_static/blog-plots/opencv/divided_lenna.png
   :align: center


.. raw:: html

   <div class="clt">
   <center><a href="../../../../figures/fig19.html" >Figure 19: divided image into multiple blocks </a> </center>
   </div>


Limitations
~~~~~~~~~~~

- This code is practical and simple to use on Windows but unfortunately, on the contrary to the OpenCV variant, it does not support different operating systems like Linux for example.
- In some cases the user might want to have equally sized blocks; in that case the dimensions of the blocks should be pre-computed if the user wants to use this snippet.

Conclusion
~~~~~~~~~~
This post provided an alternative C++ implementation to the previous OpenCV code used to divide an image into multiple blocks with predefined height and width.
Similarly, we also saved the resulting blocks to the hard drive in order to verify that the code is functional.
The code is fairly simple and supports various image encoding types(`PNG`, `JPEG` etc.) but unlike the OpenCV implementation, it only supports Windows since it is based in part on the Win32 API, specifically the GDI+ library.

Share this blog
~~~~~~~~~~~~~~~~
.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u={{url}}&title={{title}}" target="blank"><i class="fab fa-facebook-f"></i></a>
    <a class="twitter" href="https://twitter.com/intent/tweet?status={{title}}+{{url}}" target="blank"><i class="fa fa-twitter"></i></a>
    <a class="googleplus" href="https://plus.google.com/share?url={{url}}" target="blank"><i class="fa fa-google-plus"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url={{url}}&title={{title}}&source={{source}}" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit" href="http://www.reddit.com/submit?url={{url}}&title={{title}}" target="_blank" title="Submit to Reddit" target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.2022

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Image class (gdiplusheaders.h), Microsoft, https://docs.microsoft.com/en-us/windows/win32/api/gdiplusheaders/nl-gdiplusheaders-image
- GDI+, Microsoft, https://docs.microsoft.com/en-us/windows/win32/api/_gdiplus/
- Crop a big picture into several small size pictures, Graphic design, https://graphicdesign.stackexchange.com/questions/30008/crop-a-big-picture-into-several-small-size-pictures
- Divide 256*256 image into 4*4 blocks, Matlab, Stackoverflow, https://www.mathworks.com/matlabcentral/answers/33103-divide-256-256-image-into-4-4-blocks

.. _`Divide an image into blocks using OpenCV in C++` : DivideImageUsingOpenCv.html
.. _`GDI+` : https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-gdi-start
.. _`gist: DivideImageUsingGdiplus.cpp`: https://gist.github.com/SuperKogito/434ac8489f8b99aa10377966180e3a35
.. _here : https://en.wikipedia.org/wiki/Lenna#/media/File:Lenna_(test_image).png
