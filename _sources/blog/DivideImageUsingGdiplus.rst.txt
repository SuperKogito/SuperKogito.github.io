[28-09-2020] Divide an image into blocks using Gdiplus in C++
=============================================================

.. meta::
  :description: Divide an image into multiple blocks with fixed height and width using OpenCV in C++
  :keywords: Image divide, C++, OpenCV
  :author: Ayoub Malek

.. post:: September 29, 2020
  :tags: [C++], [OpenCV]
  :category: C++
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

In the previous blog, we used OpenCV to divide an image into multiple blocks of a certain height and width, which is useful when we need to apply a certain image transformation block-wise.
This blog will provide a an alternative solution with an explanation and a C++ implementation for how to divide an image into multiple blocks with custom height and width using the Gdiplus api.

| ***Keywords***:  Gdiplus, Divide image into blocks

Approach
--------
The approach implemented in the following code, is in theory the same as the one described in the previous blog: `Divide an image into blocks using OpenCV in C++`_
There are various ways of approaching this problem, most approaches out there compute the number of blocks in xy-directions and use for loops to cut the blocks.
In this blog, the dimensions of the blocks are prioritized.
However, we will make sure to crop the side blocks and lower blocks correctly even if their dimensions are different than other blocks.
To elaborate on this a bit more: if the image width = 512 px and the block width = 128 px -> we will get 512 / 128 = 4 blocks.
However if the image width = 576 px and the block width = 128 px -> we should get 4 blocks with 128 px and 1 block with width 64 px.
Therefore on each loop we need to check/ compute the block dimensions.
To keep the code fast and optimal, we will use a while loop, that will loop over the y-coordinates (Top to bottom) then the x-coordinates (left to right).
The previously described steps can are implemented in the following snippet:


.. code-block:: C++
  :linenos:

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

The previous snippet represents a small function with an integer output reflecting the run status of the function.
divideImage() takes in 4 inputs which are the image to divide, the blocks width, the blocks height and a vector variable to store the cropped blocks in.


The main call
-------------
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


Limitations
-----------
In some case the user might want to have equally sized blocks, that case the dimensions of the blocks should be pre-computed in case the user want to use this snippet.
However, tweaking the code for such use-case should be simple to do.

Conclusion
----------
To summarize, in this post we introduced a small example of how to divide an image into multiple blocks with predefined height and width using OpenCV in C++.
We also went through saving the resulting blocks to the hard drive in order to verify that the code is functional.
The code is fairly simple and supports various image encoding types(`PNG`, `JPEG` etc.) but do we need OpenCV to achieve this? can this be done differently?
The next blog should provide an answer for this.

References and Further readings
--------------------------------
.. [1] Capturing an Image, Microsoft, http://msdn.microsoft.com/en-us/library/windows/window/dd183402%28v=vs.85%29.aspx
.. [2] OPENCV Desktop Capture, Stackoverflow, https://stackoverflow.com/questions/34466993/opencv-desktop-capture
.. [3] How to capture the desktop in OpenCV (ie. turn a bitmap into a Mat)?, Stackoverflow, https://stackoverflow.com/questions/14148758/how-to-capture-the-desktop-in-opencv-ie-turn-a-bitmap-into-a-mat

https://graphicdesign.stackexchange.com/questions/30008/crop-a-big-picture-into-several-small-size-pictures
https://www.mathworks.com/matlabcentral/answers/33103-divide-256-256-image-into-4-4-blocks
https://answers.opencv.org/question/53694/divide-an-image-into-lower-regions/

.. _`cv::Mat object`: https://docs.opencv.org/trunk/d3/d63/classcv_1_1Mat.html
.. _`gist: CaptureSceenshotUsingOpenCV.cpp`: https://gist.github.com/SuperKogito/a6383dddcf4ee459b979e12550cc6e51
.. _`OpenCV 4 Building with CMake & Visual Studio 2017 Setup`: https://youtu.be/By-PKbWDZNk
