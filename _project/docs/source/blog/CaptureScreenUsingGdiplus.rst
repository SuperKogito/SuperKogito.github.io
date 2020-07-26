[26-07-2020] Capturing the screen on Windows in C++ using GDI+
=================================================================

.. meta::
  :description: Capturing the screen using Gdiplus
  :keywords: Screen capture, Gdiplus
  :author: Ayoub Malek

.. post:: July 26, 2020
  :tags: [Win32],[Gdiplus],[Screen Capture]
  :category: C++
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

`GDI+/ Gdiplus`_ is part of the `Win32 API`_, that helps C/C++ programmers with graphics related tasks on Windows.
In this blog, we will be writing a simple algorithm to capture the content of the screen on Windows using Gdiplus in C++.

| ***Keywords***: GDI+, Screen capture, Screenshots


GDI+ / Gdiplus introduction
---------------------------
Gdiplus is part of the `Win32 API`, so we don't have to do any additional actions to be able to use the library.
A simple :code:`#include "Gdiplus.h"` should be sufficient.
Moreover, as hinted in the previous blog, we will notice a notable difference in run-times between this implementation and the OpenCV variant, since GDI+ is built on top of the Windows Graphics Device Interface (GDI).

Capture screenshot
------------------
Now let's write the main capture function, which will take a window handle to get its associated contextual device and return a `HBITMAP` object with the screenshot information.
The function first defines handles to the device context and the associated Region of interest (defined using start-x, start-y, width and height).
The bitmap and its header are then created and the screen pixel data are passed to them.
Finally the device contexts are deleted to avoid memory leaks.
For aesthetic and simplicity reasons, I chose to initialize the bitmap header in a separate function.
The previously described steps looks as follows in C++:

.. code-block:: C++
  :linenos:

  BITMAPINFOHEADER createBitmapHeader(int width, int height)
  {
      BITMAPINFOHEADER  bi;

      // create a bitmap
      bi.biSize = sizeof(BITMAPINFOHEADER);
      bi.biWidth = width;
      bi.biHeight = -height;  //this is the line that makes it draw upside down or not
      bi.biPlanes = 1;
      bi.biBitCount = 32;
      bi.biCompression = BI_RGB;
      bi.biSizeImage = 0;
      bi.biXPelsPerMeter = 0;
      bi.biYPelsPerMeter = 0;
      bi.biClrUsed = 0;
      bi.biClrImportant = 0;

      return bi;
  }

  HBITMAP GdiPlusScreenCapture(HWND hWnd)
  {
      // get handles to a device context (DC)
      HDC hwindowDC = GetDC(hWnd);
      HDC hwindowCompatibleDC = CreateCompatibleDC(hwindowDC);
      SetStretchBltMode(hwindowCompatibleDC, COLORONCOLOR);

      // define scale, height and width
      int scale = 1;
      int screenx = GetSystemMetrics(SM_XVIRTUALSCREEN);
      int screeny = GetSystemMetrics(SM_YVIRTUALSCREEN);
      int width = GetSystemMetrics(SM_CXVIRTUALSCREEN);
      int height = GetSystemMetrics(SM_CYVIRTUALSCREEN);

      // create a bitmap
      HBITMAP hbwindow = CreateCompatibleBitmap(hwindowDC, width, height);
      BITMAPINFOHEADER bi = createBitmapHeader(width, height);

      // use the previously created device context with the bitmap
      SelectObject(hwindowCompatibleDC, hbwindow);

      // Starting with 32-bit Windows, GlobalAlloc and LocalAlloc are implemented as wrapper functions that call HeapAlloc using a handle to the process's default heap.
      // Therefore, GlobalAlloc and LocalAlloc have greater overhead than HeapAlloc.
      DWORD dwBmpSize = ((width * bi.biBitCount + 31) / 32) * 4 * height;
      HANDLE hDIB = GlobalAlloc(GHND, dwBmpSize);
      char* lpbitmap = (char*)GlobalLock(hDIB);

      // copy from the window device context to the bitmap device context
      StretchBlt(hwindowCompatibleDC, 0, 0, width, height, hwindowDC, screenx, screeny, width, height, SRCCOPY);   //change SRCCOPY to NOTSRCCOPY for wacky colors !
      GetDIBits(hwindowCompatibleDC, hbwindow, 0, height, lpbitmap, (BITMAPINFO*)&bi, DIB_RGB_COLORS);

      // avoid memory leak
      DeleteDC(hwindowCompatibleDC);
      ReleaseDC(hWnd, hwindowDC);

      return hbwindow;
  }


Save Screenshot to memory
-------------------------
Unlike the case of OpenCV, in order to **save the captured bitmap to the memory** as a `PNG` or `JPEG` etc. we must write some code for that.
This can be done using the following Boolean function:

.. code-block:: C++
   :linenos:

   bool saveToMemory(HBITMAP* hbitmap, std::vector<BYTE>& data, std::string dataFormat = "png")
   {
       Gdiplus::Bitmap bmp(*hbitmap, nullptr);
       // write to IStream
       IStream* istream = nullptr;
       CreateStreamOnHGlobal(NULL, TRUE, &istream);

       // define encoding
       CLSID clsid;
       if (dataFormat.compare("bmp") == 0) { CLSIDFromString(L"{557cf400-1a04-11d3-9a73-0000f81ef32e}", &clsid); }
       else if (dataFormat.compare("jpg") == 0) { CLSIDFromString(L"{557cf401-1a04-11d3-9a73-0000f81ef32e}", &clsid); }
       else if (dataFormat.compare("gif") == 0) { CLSIDFromString(L"{557cf402-1a04-11d3-9a73-0000f81ef32e}", &clsid); }
       else if (dataFormat.compare("tif") == 0) { CLSIDFromString(L"{557cf405-1a04-11d3-9a73-0000f81ef32e}", &clsid); }
       else if (dataFormat.compare("png") == 0) { CLSIDFromString(L"{557cf406-1a04-11d3-9a73-0000f81ef32e}", &clsid); }

       Gdiplus::Status status = bmp.Save(istream, &clsid, NULL);
       if (status != Gdiplus::Status::Ok)
           return false;

       // get memory handle associated with istream
       HGLOBAL hg = NULL;
       GetHGlobalFromStream(istream, &hg);

       // copy IStream to buffer
       int bufsize = GlobalSize(hg);
       data.resize(bufsize);

       // lock & unlock memory
       LPVOID pimage = GlobalLock(hg);
       memcpy(&data[0], pimage, bufsize);
       GlobalUnlock(hg);
       istream->Release();
       return true;
   }

The main call
---------------
Let's bind everything together inside the :code:`main()` function and test this, so you can also have an idea on how to use the previous code.
In code this looks like this:

.. code-block:: c++
  :linenos:

  int main()
  {
      // Initialize GDI+.
      GdiplusStartupInput gdiplusStartupInput;
      ULONG_PTR gdiplusToken;
      GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

      // get the bitmap handle to the bitmap screenshot
      HWND hWnd = GetDesktopWindow();
      HBITMAP hBmp = GdiPlusScreenCapture(hWnd);

      // save as png to memory
      std::vector<BYTE> data;
      std::string dataFormat = "bmp";

      if (saveToMemory(&hBmp, data, dataFormat))
      {
          std::wcout << "Screenshot saved to memory" << std::endl;

          // save from memory to file
          std::ofstream fout("Screenshot-m1." + dataFormat, std::ios::binary);
          fout.write((char*)data.data(), data.size());
      }
      else
          std::wcout << "Error: Couldn't save screenshot to memory" << std::endl;


      // save as png (method 2)
      CImage image;
      image.Attach(hBmp);
      image.Save(L"Screenshot-m2.png");

      GdiplusShutdown(gdiplusToken);
      return 0;
  }

**The full code can be found in this** `gist: CaptureScreenUsingGdiplus.cpp`_.

Limitations
-----------
Similar to the OpenCV variant, this implementation is a bit limited; In a multi-monitors setups, if you play with the DPI and the scaling settings of the screens, you will notice that the resulting screenshots can be cropped.
This can be solved by setting the C++ project DPI-awareness to True.
In Visual Studio 2019, this can be done under: :code:`Project > Project-Name Properties > Manifest Tool > Input and Output > DPI Awareness`

Another limitations is that this code only allows for one screenshot to be captured, which is not always the best option.
Some users might want to only capture a specific screen. This can be solved -as we will see in future posts- by manipulating the start-x, start-y, width and the height variables.

Conclusion
----------
To summarize, in this post we introduced a small example of how to capture the screen content using the `Win32 API`_ : GDI+ also known as Gdiplus.
We also went through saving the captured screenshot to the hard drive or to memory in order to use it in the code again.
The code is fairly simple and supports both `PNG` \& `JPEG` and seems to be faster than the OpenCV version, but is it really? This will be explored in details in my next post, so stay tuned.


References and Further readings
--------------------------------
.. [1] : GDI+, Microsoft, https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-gdi-start
.. [2] : About GDI+, Microsoft, https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-about-gdi--about
.. [3] : Does GDI+ have standard image encoder CLSIDs?, Stackoverflow, https://stackoverflow.com/questions/5345803/does-gdi-have-standard-image-encoder-clsids
.. [4] : GDI+ Bitmap Save problem, Stackoverflow, https://stackoverflow.com/questions/1584202/gdi-bitmap-save-problem

.. _`gist: CaptureScreenUsingGdiplus.cpp` : https://gist.github.com/SuperKogito/00e0ad0d5b2b567d74a10fe18c048776
.. _`GDI+/ Gdiplus` : https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-gdi-start
.. _`Win32 API` : https://docs.microsoft.com/en-us/windows/win32/
