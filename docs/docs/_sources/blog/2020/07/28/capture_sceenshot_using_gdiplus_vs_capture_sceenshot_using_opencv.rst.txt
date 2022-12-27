:og:description: Compare screen shooting using Gdiplus and OpenCV
:og:keywords: Screen capture, Gdiplus, OpenCV, c++, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/capture_sceenshot_using_gdiplus_vs_capture_sceenshot_using_opencv.png
:og:image:alt: comparie screen capturing using GDI+ and OpenCV on Windows in C++

Comparing screen capturing using GDI+ and OpenCV on Windows in C++
==================================================================

.. post:: July 28, 2020
  :tags: Cplusplus, Windows, Gdiplus, OpenCV, Screen-capture
  :category: Image processing
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

To follow up on my last two blogs (`Capturing the screen on Windows in C++ using OpenCV`_ \& `Capturing the screen on Windows in C++ using GDI+`_ ), we compare in this post both approaches.
In order to compare both approaches, we examines their run-times and CPU usages.

Benchmarking Code
~~~~~~~~~~~~~~~~~
To capture the run-times of each approach, we will need to add a Timer, that we will use to capture the start and end times of each approach.
For this you can use whatever implementation you deem useful. I personally used the following snippet, which can be found here_ :

.. code-block:: C++
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
~~~~~~~~~~~~~~~~~
Now let's write the main testing code.
We already have all the components ready in the last two posts, so all we need is combine the previous screen-shooting codes with the timer calls.

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
~~~~~~~~~~~~~~~~~~~~~
The testing results confirms the previously mentioned intuition that screen shooting using GDI+ is faster than the OpenCV variant.
However, upon examining the results in details, we realize that the right answer to the question of **which library is better?** is a complex one (as it is the case, almost always).

.. code-block::

   Benchmarks for GDI+ variant of the screenshooter
   *********************************************************
   | Number of Runs       [#]  = 50
   | Run duration         [s]  = 7.3564
   | Average Run duration [ms] = 0.147128
   *********************************************************
   Benchmarks for OpenCV variant of the screenshooter
   *********************************************************
   | Number of Runs       [#]  = 50
   | Run duration         [s]  = 17.8956
   | Average Run duration [ms] = 0.357913
   *********************************************************

Conclusion
~~~~~~~~~~~
To summarize, in this post we compared the previously implemented screen-shooting methods using GDI+ and OpenCV.
The test results confirmed the previous intuition about the GDI+ being faster as it uses the native Windows API.
However, the OpenCV variant is still a decent option and sometimes even a better one because -unlike GDI+- it supports various operating systems other than Windows.

Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2020/07/28/capture_sceenshot_using_gdiplus_vs_capture_sceenshot_using_opencv.html&title=Comparing%20screen%20capturing%20using%20GDI+%20and%20OpenCV%20on%20Windows%20in%20C++"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2020/07/28/capture_sceenshot_using_gdiplus_vs_capture_sceenshot_using_opencv.html&text=Comparing%20screen%20capturing%20using%20GDI+%20and%20OpenCV%20on%20Windows%20in%20C++"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2020/07/28/capture_sceenshot_using_gdiplus_vs_capture_sceenshot_using_opencv.html&title=Comparing%20screen%20capturing%20using%20GDI+%20and%20OpenCV%20on%20Windows%20in%20C++" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2020/07/28/capture_sceenshot_using_gdiplus_vs_capture_sceenshot_using_opencv.html&title=Comparing%20screen%20capturing%20using%20GDI+%20and%20OpenCV%20on%20Windows%20in%20C++"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.2022

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- GDI+, Microsoft, https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-gdi-start
- About GDI+, Microsoft, https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-about-gdi--about
- Does GDI+ have standard image encoder CLSIDs?, Stackoverflow, https://stackoverflow.com/questions/5345803/does-gdi-have-standard-image-encoder-clsids
- GDI+ Bitmap Save problem, Stackoverflow, https://stackoverflow.com/questions/1584202/gdi-bitmap-save-problem
- Capturing an Image, Microsoft, http://msdn.microsoft.com/en-us/library/windows/window/dd183402%28v=vs.85%29.aspx
- OPENCV Desktop Capture, Stackoverflow, https://stackoverflow.com/questions/34466993/opencv-desktop-capture
- How to capture the desktop in OpenCV (ie. turn a bitmap into a Mat)?, Stackoverflow, https://stackoverflow.com/questions/14148758/how-to-capture-the-desktop-in-opencv-ie-turn-a-bitmap-into-a-mat

.. _`Capturing the screen on Windows in C++ using OpenCV` : https://superkogito.github.io/blog/CaptureScreenUsingOpenCv.html
.. _`Capturing the screen on Windows in C++ using GDI+` : https://superkogito.github.io/blog/CaptureScreenUsingGdiplus.html
.. _`Win32 API` : https://docs.microsoft.com/en-us/windows/win32/
.. _here : https://gist.github.com/yfzhang/ecad60e24eb1e08cf4c733ace3fee174
