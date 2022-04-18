:og:description: Capturing the screen using OpenCV
:og:keywords: Screen capture, OpenCV, c++, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/capture_screen_using_opencv.png
:og:image:alt: Capturing the screen on Windows in C++ using OpenCV

Capturing the screen on Windows in C++ using OpenCV
===================================================

.. post:: July 25, 2020
  :tags: Cplusplus, Windows, OpenCV, Screen-capture
  :category: Image processing
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

OpenCV is just a great computer vision tool with a wide variety of capabilities, that is available in both C++ and Python.
In this first blog about OpenCV, I will be introducing a simple algorithm to capture the content of the screen on Windows using OpenCV in C++.

Build library and Includes
~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to use OpenCV in C++, we have first to install the library.
In my case, I am using Visual Studio 2019 so I had to build the library from source and correctly link it to my project.
You can choose any build architecture that suits you, but most of my upcoming posts will be using the x86 architecture as I will be combining my code with win32 based GUIs.
To install and link OpenCV correctly, I suggest referring to this very helpful video `OpenCV 4 Building with CMake & Visual Studio 2017 Setup`_.

Once the project is correctly setup, we can start writing some code.
So first we need to include the needed headers.
In this case we need the OpenCV header (:code:`opencv2/opencv.hpp`) and the Windows header (:code:`Windows.h`) which we will use to get the desktop window handle:

.. code-block:: C++
   :linenos:

   #pragma once
   #include <Windows.h>
   #include <opencv2/opencv.hpp>

   using nammespace cv;


Capture screenshot function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Now let's write the main capture function, which will take a window handle to get its associated contextual device and return a `cv::Mat object`_ including the screenshot information.
This function will first define handles to the device context and the associated Region of interest (defined using start-x, start-y, width and height).
The bitmap and its header are then created and filled with the screen pixels data.
This data is also passed to the Mat object. Finally the device contexts are deleted to avoid any memory leaks.
For aesthetic \& simplicity reasons, I chose to initialize the bitmap header in a separate function (:code:`BITMAPINFOHEADER createBitmapHeader(int, int)`).
The previously described steps looks as follows in C++:

.. code-block:: c++
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

   Mat captureScreenMat(HWND hwnd)
   {
    	Mat src;

    	// get handles to a device context (DC)
    	HDC hwindowDC = GetDC(hwnd);
    	HDC hwindowCompatibleDC = CreateCompatibleDC(hwindowDC);
    	SetStretchBltMode(hwindowCompatibleDC, COLORONCOLOR);

    	// define scale, height and width
    	int screenx = GetSystemMetrics(SM_XVIRTUALSCREEN);
    	int screeny = GetSystemMetrics(SM_YVIRTUALSCREEN);
    	int width = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    	int height = GetSystemMetrics(SM_CYVIRTUALSCREEN);

    	// create mat object
    	src.create(height, width, CV_8UC4);

    	// create a bitmap
    	HBITMAP hbwindow = CreateCompatibleBitmap(hwindowDC, width, height);
    	BITMAPINFOHEADER bi = createBitmapHeader(width, height);

    	// use the previously created device context with the bitmap
    	SelectObject(hwindowCompatibleDC, hbwindow);

    	// copy from the window device context to the bitmap device context
    	StretchBlt(hwindowCompatibleDC, 0, 0, width, height, hwindowDC, screenx, screeny, width, height, SRCCOPY);  //change SRCCOPY to NOTSRCCOPY for wacky colors !
    	GetDIBits(hwindowCompatibleDC, hbwindow, 0, height, src.data, (BITMAPINFO*)&bi, DIB_RGB_COLORS);            //copy from hwindowCompatibleDC to hbwindow

    	// avoid memory leak
    	DeleteObject(hbwindow);
    	DeleteDC(hwindowCompatibleDC);
    	ReleaseDC(hwnd, hwindowDC);

    	return src;
    }


The main call
~~~~~~~~~~~~~
In order to test this, and for you to have an idea on how to use the previous code, in your future projects.
Let's call it inside of a main function, encode the output as a `PNG` and save the captured screenshot to the hard drive.
In code this looks like this:

.. code-block:: c++
  :linenos:

  int main()
  {
  	// capture image
  	HWND hwnd = GetDesktopWindow();
  	Mat src = captureScreenMat(hwnd);

  	// save img
  	cv::imwrite("Screenshot.png", src);

    // clean-ups
  	buf.clear();
  	return 0;
  }


Just in case you need, in memory `PNG` data then just copy the data in the `cv::Mat object`_ to a vector like the following:

.. code-block:: c++
  :linenos:

  // encode result in case you need in memory byte data
  std::vector<uchar> buf;
  cv::imencode(".png", src, buf);


**The full code can be found in this** `gist: CaptureSceenshotUsingOpenCV.cpp`_.
*In case you prefer having `JPEG` data, then just replicate all the previous steps while replacing :code::`".png"` with :code::`".jpg"`.*

Limitations
~~~~~~~~~~~
- The previous implementation is a bit limited. As it is somewhat slow comparing to the screen capture windows function associated with the capture screen button. This can be explained by the fact that unlike the windows function, OpenCV was not built for such a basic task.

- Furthermore, in a multi-monitors setup, if you play with the DPI and the scaling settings of the screens, you will notice that the resulting screenshots can be cropped. This can be solved by setting the C++ project DPI-awareness to `True`. In Visual Studio 2019, this can be done under: :code:`Project > Project-Name Properties > Manifest Tool > Input and Output > DPI Awareness`

- Another limitations is that this code only allows for one screenshot of all screens, which is not always the best option. Some users might want to only capture a specific screen. This can be solved -as we will see in future posts- by manipulating the start-x, start-y, width and the height variables used in the capture function.

Conclusion
~~~~~~~~~~
To summarize, in this post we introduced a small example of how to capture the screen content using OpenCV and save it to the hard drive as an image or to the memory to use it inside your code.
The code is fairly simple and supports both `PNG` and `JPEG`.
On the other hand, the code is slightly slow and therefore using the native Windows solution might result in better performance.
This option will be explored in my next posts, so stay tuned.

Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2020/07/25/capture_screen_using_opencv.html&title=Capturing%20the%20screen%20on%20Windows%20in%20C++%20using%20OpenCV"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2020/07/25/capture_screen_using_opencv.html&text=Capturing%20the%20screen%20on%20Windows%20in%20C++%20using%20OpenCV"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2020/07/25/capture_screen_using_opencv.html&title=Capturing%20the%20screen%20on%20Windows%20in%20C++%20using%20OpenCV" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2020/07/25/capture_screen_using_opencv.html&title=Capturing%20the%20screen%20on%20Windows%20in%20C++%20using%20OpenCV"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.2022

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Capturing an Image, Microsoft, http://msdn.microsoft.com/en-us/library/windows/window/dd183402%28v=vs.85%29.aspx
- OPENCV Desktop Capture, Stackoverflow, https://stackoverflow.com/questions/34466993/opencv-desktop-capture
- How to capture the desktop in OpenCV (ie. turn a bitmap into a Mat)?, Stackoverflow, https://stackoverflow.com/questions/14148758/how-to-capture-the-desktop-in-opencv-ie-turn-a-bitmap-into-a-mat

.. _`cv::Mat object`: https://docs.opencv.org/trunk/d3/d63/classcv_1_1Mat.html
.. _`gist: CaptureSceenshotUsingOpenCV.cpp`: https://gist.github.com/SuperKogito/a6383dddcf4ee459b979e12550cc6e51
.. _`OpenCV 4 Building with CMake & Visual Studio 2017 Setup`: https://youtu.be/By-PKbWDZNk
