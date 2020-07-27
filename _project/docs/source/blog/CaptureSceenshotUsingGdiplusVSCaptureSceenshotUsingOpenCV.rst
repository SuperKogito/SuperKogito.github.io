[28-07-2020] Comparing screen capturing using GDI+ and OpenCV on Windows in C++
================================================================================

.. meta::
  :description: Compare screen shooting using Gdiplus and OpenCV
  :keywords: Screen capture, Gdiplus, OpenCV
  :author: Ayoub Malek

.. post:: July 28, 2020
  :tags: [Win32],[Gdiplus], [OpenCV], [Screen Capture]
  :category: C++
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

To follow up on my last two blogs (`[25-07-2020] Capturing the screen on Windows in C++ using OpenCV`_ \& `[26-07-2020] Capturing the screen on Windows in C++ using GDI+`_ ), we compare in this post both approaches.
In order to compare both approaches, we examines their run-times and CPU usages.

| ***Keywords***: GDI+, OpenCV, Screen capture, Screenshots, Comparison

Benchmarking Code
-----------------
To capture the run-times of each approach, we will need to add a Timer, that we will use to capture the start and end times of each approach.
For this you can use whatever implementation you deem useful. I personally used [this snippet](https://gist.github.com/yfzhang/ecad60e24eb1e08cf4c733ace3fee174).

.. code-block: C++
  :linenos:
  #include <chrono>
  #include <iostream>

  /*
   * Timer class to measure the run-times in seconds of code snippets.
   */
  class Timer
  {
  public:
      Timer() : beg_(clock_::now()) {}
      void reset() { beg_ = clock_::now(); }
      double elapsed() const { return std::chrono::duration_cast<second_> (clock_::now() - beg_).count();}

  private:
      typedef std::chrono::high_resolution_clock clock_;
      typedef std::chrono::duration<double, std::ratio<1> > second_;
      std::chrono::time_point<clock_> beg_;
  };

The Testing setup
-----------------
Now let's write the main capture function, which will take a window handle to get its associated contextual device and return a `HBITMAP` object with the screenshot information.
The function first defines handles to the device context and the associated Region of interest (defined using start-x, start-y, width and height).
The bitmap and its header are then created and the screen pixel data are passed to them.
Finally the device contexts are deleted to avoid memory leaks.
For aesthetic and simplicity reasons, I chose to initialize the bitmap header in a separate function.
The previously described steps looks as follows in C++:

.. code-block:: C++
  :linenos:


  int main()
  {
      // initializations
      Timer tmr;
      int repetitions = 50;
      HWND hWnd = GetDesktopWindow();

      tmr.reset();
      double t = tmr.elapsed();

      // Initialize GDI+.
      GdiplusStartupInput gdiplusStartupInput;
      ULONG_PTR gdiplusToken;
      GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

      std::wcout << "Benchmarks for GDI+ variant of the screenshooter" << std::endl;
      std::wcout << "***********************************************************" << std::endl;
      // benchmarks for GDI+
      tmr.reset();
      for (int i = 0; i < repetitions; i++)
      {
          // capture and encode screenshot
          std::vector<BYTE> data;
          HBITMAP hBmp = GdiPlusScreenCapture(hWnd);
          saveToMemory(&hBmp, data, "png");
          data.clear();
      }
      GdiplusShutdown(gdiplusToken);
      t = tmr.elapsed();
      std::wcout << " | Number of Runs       [#] = " << repetitions << std::endl;
      std::wcout << " | Run duration         [s] = " << t << std::endl;
      std::wcout << " | Average Run duration [ms] = " << t / repetitions << std::endl;
      std::wcout << "***********************************************************" << std::endl;

      std::wcout << "Benchmarks for OpenCV variant of the screenshooter" << std::endl;
      std::wcout << "***********************************************************" << std::endl;
      // benchmarks for OpenCV
      tmr.reset();
      for (int i = 0; i < repetitions; i++)
      {
          // capture and encode screenshot
          std::vector<uchar> buf;
          Mat src = captureScreenMat(hWnd);
          cv::imencode(".png", src, buf);
          cv::imwrite("aminemalek.png", src);
          buf.clear();
          src.release();
      }
      t = tmr.elapsed();
      std::wcout << " | Number of Runs       [#] = " << repetitions << std::endl;
      std::wcout << " | Run duration         [s] = " << t << std::endl;
      std::wcout << " | Average Run duration [ms] = " << t / repetitions << std::endl;
      std::wcout << "***********************************************************" << std::endl;
      return 0;
  }

Benchmarking results
--------------------
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

.. _`[25-07-2020] Capturing the screen on Windows in C++ using OpenCV` : https://superkogito.github.io/blog/CaptureScreenUsingOpenCv.html
.. _`[26-07-2020] Capturing the screen on Windows in C++ using GDI+` : https://superkogito.github.io/blog/CaptureScreenUsingGdiplus.html
.. _`Win32 API` : https://docs.microsoft.com/en-us/windows/win32/
