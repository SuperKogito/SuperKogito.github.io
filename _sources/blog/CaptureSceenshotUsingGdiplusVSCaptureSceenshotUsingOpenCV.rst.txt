Comparing screen capturing using GDI+ and OpenCV on Windows in C++
==================================================================

.. raw:: html

  <div class="blog-post-tags">
    <ul class="blog-posts-details">
    <li id="Date"><span>Date:</span>                 28 July 2020 </li>
    <li id="author"><span>Author:</span>            <a href="author/ayoub-malek.html">Ayoub Malek</a> </li>
    <li id="location"><span>Location:</span>        <a href="location/munich.html">Munich</a>
    </li>  <li id="language"><span>Language:</span> <a href="language/english.html">English</a>
    </li>  <li id="category"><span>Category:</span> <a href="category/image-processing.html">Image processing</a>
    </li>
    <li id="tags"><span>Tags:
          </span>
          <a class="post-tags" href="tag/cplusplus.html">C++</a>
          <a class="post-tags" href="tag/windows.html">Windows</a>
          <a class="post-tags" href="tag/gdiplus.html">GDI+</a>
          <a class="post-tags" href="tag/screenshot.html">Screenshot</a>
          <a class="post-tags" href="tag/benchmarking.html">Benchmarking</a>

    </li>
    </ul>
  </div>


.. meta::
  :description: Compare screen shooting using Gdiplus and OpenCV
  :keywords: Screen capture, Gdiplus, OpenCV
  :author: Ayoub Malek

.. post:: July 28, 2020
  :tags: Cplusplus, Windows, Gdiplus, OpenCV, Screenshot
  :category: Image processing, 2020
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

To follow up on my last two blogs (`Capturing the screen on Windows in C++ using OpenCV`_ \& `Capturing the screen on Windows in C++ using GDI+`_ ), we compare in this post both approaches.
In order to compare both approaches, we examines their run-times and CPU usages.

Benchmarking Code
-----------------
To capture the run-times of each approach, we will need to add a Timer, that we will use to capture the start and end times of each approach.
For this you can use whatever implementation you deem useful. I personally used the following snippet, which can be found here_:

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
--------------------
The testing results confirms the previously mentioned intuition that screen shooting using GDI+ is faster than the OpenCV variant.
However, upon examining the results in details, we realize that the right answer to the question of **which library is better?** is a complex one (as it is the case, almost always).

.. code-block:: C++

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


Edit
-----
This post is still lacking and is subject to future edits that will include code improvements and better suited tests.


Conclusion
----------
To summarize, in this post we compared the previously implemented screen-shooting methods using GDI+ and OpenCV.
The test results confirmed the previous intuition about the GDI+ being faster as it uses the native Windows API.
However, the OpenCV variant is still a decent option and sometimes even a better one because -unlike GDI+- it supports various operating systems other than Windows.


References and Further readings
--------------------------------
.. [1] : GDI+, Microsoft, https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-gdi-start
.. [2] : About GDI+, Microsoft, https://docs.microsoft.com/en-us/windows/win32/gdiplus/-gdiplus-about-gdi--about
.. [3] : Does GDI+ have standard image encoder CLSIDs?, Stackoverflow, https://stackoverflow.com/questions/5345803/does-gdi-have-standard-image-encoder-clsids
.. [4] : GDI+ Bitmap Save problem, Stackoverflow, https://stackoverflow.com/questions/1584202/gdi-bitmap-save-problem
.. [5] Capturing an Image, Microsoft, http://msdn.microsoft.com/en-us/library/windows/window/dd183402%28v=vs.85%29.aspx
.. [6] OPENCV Desktop Capture, Stackoverflow, https://stackoverflow.com/questions/34466993/opencv-desktop-capture
.. [7] How to capture the desktop in OpenCV (ie. turn a bitmap into a Mat)?, Stackoverflow, https://stackoverflow.com/questions/14148758/how-to-capture-the-desktop-in-opencv-ie-turn-a-bitmap-into-a-mat

.. _`Capturing the screen on Windows in C++ using OpenCV` : https://superkogito.github.io/blog/CaptureScreenUsingOpenCv.html
.. _`Capturing the screen on Windows in C++ using GDI+` : https://superkogito.github.io/blog/CaptureScreenUsingGdiplus.html
.. _`Win32 API` : https://docs.microsoft.com/en-us/windows/win32/
.. _here : https://gist.github.com/yfzhang/ecad60e24eb1e08cf4c733ace3fee174
