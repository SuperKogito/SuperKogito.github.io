[20-07-2020] Capturing the screen on Windows in C++ using OpenCV
================================================================

.. meta::
   :description: Capturing the screen using OpenCV
   :keywords: Screen capture, OpenCV
   :author: Ayoub Malek

.. post:: July 20, 2019
   :tags:[OpenCV],[Screen Capture]
   :category:C++
   :author: Ayoub Malek
   :location: Munich
   :language: English

-----------------------

OpenCV is just a great computer vision tool with a wide variety of capabilities, that is available in both C++ and Python.
In this first blog about OpenCV, I will be introducing a simple algorithm to capture the content of the screen on Windows using OpenCV in C++.

| **Keywords**: OpenCV, Screen capture, Screenshots


Build library and Includes
---------------------------
In order to use OpenCV in C++, we have first to install the library.
In my case, I am using Visual Studio 2019 so I had the build the library from source and correctly link it to my project.
You can choose any build architecture that suits you, but most my upcoming posts will be using the x86 architecture as I will be combining my code with win32 based GUIs.
To install and link OpenCV correctly, I suggest referring to this very helpful video [OpenCV 4 Building with CMake & Visual Studio 2017 Setup](https://youtu.be/By-PKbWDZNk).

Once the project is correctly, we can start writing some code.
First we need to include the needed headers. In this case we need the OpenCV header (opencv2/opencv.hpp) and the Windows header (Windows.h) which we will use to get the desktop window handle:

.. code-block:: c++
  :linenos:

  #pragma once
  #include <Windows.h>
  #include <opencv2/opencv.hpp>

  using nammespace cv;


Capture screenshot function
----------------------------
now let's write the main capture function, which will take a window handle to get its associated contextual device and return a cv::Mat object (https://docs.opencv.org/trunk/d3/d63/classcv_1_1Mat.html) with the screenshot information.
The function first defines handles to the device context and the associated Region of interest (defined using start-x, start-y, width and height).
The bitmap and its header are then created and filled with the screen pixel data.
This data is also passed to the Mat object. Finally the device contexts are deleted and deleted to avoid memory leaks.
 For astatic and simplicity reason, I chose to initialize the bitmap header in a separate function.
The previously described steps looks as follows in c++:

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


The whole thing
---------------
In order to test this, and for you to have an idea on how to use the previous code. Let call it in the main function, encode the output as a PNG and save the screenshot to the hard drive.
In code this looks like this:

.. code-block:: C++
  :linenos:

  int main()
  {
  	// capture image
  	HWND hwnd = GetDesktopWindow();
  	Mat src = captureScreenMat(hwnd);

  	// save img
  	cv::imwrite("Screenshot.png", src);

  	buf.clear();
  	return 0;
  }


Just in case you need, in memory png data then just copy the data in the Mat object to a vector as the following:

.. code-block:: c++
  :linenos:

  // encode result in case you need in memory byte data
  std::vector<uchar> buf;
  cv::imencode(".png", src, buf);

The full code can be found in this gist (https://gist.github.com/SuperKogito/a6383dddcf4ee459b979e12550cc6e51).
*In case you prefer having JPEG data, then just replicate all the previous steps while replacing ".png" with ".jpg"

Limitations
-----------
The previous implementation is a bit limited. As it is somewhat slow comparing to the screen capture windows function associated with the capture screen button.
This can be explained by the fact that OpenCV was not built such a basic task.

Furthermore, in a multi-monitors setup, if you play with the DPI and the scaling settings of the screens, you will notice that the resulting screenshots can be cropped.
This can be solved by setting the C++ project DPI-awareness to True.
In Visual Studio 2019 , this can be done under: Project > ProjectName Properties > Manifest Tool > Input and Output > DPI Awareness

Another limitations is that this code only allows for one screenshot of all screens, which is not always the best option.
Some users might want to only capture a specific screen. This can be solved -as we will see in future posts- by manipulating the start-x, start-y, width and the height.

Conclusion
----------
To summarize, in this post we introduced a small example of how to capture the screen content using OpenCV and save it to the hard drive or to memory.
The code is fairly simple and supports both PNG and JPEG. On the other hand, the code is slightly slow and therefore using the native Windows solution might result in better performance.
This option will be explored in my next posts, so stay tuned.


References and Further readings
--------------------------------
http://msdn.microsoft.com/en-us/library/windows/window/dd183402%28v=vs.85%29.aspx
https://stackoverflow.com/questions/34466993/opencv-desktop-capture
https://stackoverflow.com/questions/14148758/how-to-capture-the-desktop-in-opencv-ie-turn-a-bitmap-into-a-mat