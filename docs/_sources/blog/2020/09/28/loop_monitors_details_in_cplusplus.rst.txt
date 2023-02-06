:og:description: Loop over monitors and get their coordinates and dimensions in C++ when using a multiple monitors setup on windows.
:og:keywords: c++, multiple monitors setup, multi-monitors, monitors dimensions, C++, monitor coordinates, ayoub malek, blog post
:og:image: ../../../../_static/meta_images/loop_monitors_details_in_cplusplus.png
:og:image:alt: How to loop over monitors and get their coordinates on Windows in C++

How to loop over monitors and get their coordinates on Windows in C++?
======================================================================

.. post:: September 28, 2020
  :tags: Cplusplus, Windows
  :category: Image processing
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

The previous three blogs (`Capturing the screen on Windows in C++ using OpenCV`_ \& `Capturing the screen on Windows in C++ using GDI+`_ and `Comparing screen capturing using GDI+ and OpenCV on Windows in C++`_) described capturing a screenshot of only *one* monitor.
However, nowadays we often use multiple monitors and capturing the content of all of them or a specific one, two or more.
Therefore, we will need to retrieve the coordinates of the targeted monitors.
This blog will provide a short explanation and a C++ implementation for how to loop the existing monitors in a multiple monitors setup, get their dimensions and coordinates which can be used later into capturing the monitors content.

| ***Keywords***:  multiple monitors, multi-monitors dimensions, monitor coordinates, C++

Approach and implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The trick for looping the screens dimensions is to use the function :code:`EnumDisplayMonitors(NULL, NULL, MyInfoEnumProc, 0)`, which is available as part of the `Win32 API`_.
A nice approach to this, is to pack the enumeration code in a structure that can be looped to retrieve the information related to each monitor.
This can be done as in the following:

.. code-block:: C++
  :linenos:

  #include <windows.h>
  #include <vector>
  #include <iostream>


  // Structure that includes all screen hanldes and rectangles
  struct cMonitorsVec
  {
  	std::vector<int>       iMonitors;
  	std::vector<HMONITOR>  hMonitors;
  	std::vector<HDC>       hdcMonitors;
  	std::vector<RECT>      rcMonitors;

  	static BOOL CALLBACK MonitorEnum(HMONITOR hMon, HDC hdc, LPRECT lprcMonitor, LPARAM pData)
  	{
  		cMonitorsVec* pThis = reinterpret_cast<cMonitorsVec*>(pData);

  		pThis->hMonitors.push_back(hMon);
  		pThis->hdcMonitors.push_back(hdc);
  		pThis->rcMonitors.push_back(*lprcMonitor);
  		pThis->iMonitors.push_back(pThis->hdcMonitors.size());
  		return TRUE;
  	}

  	cMonitorsVec()
  	{
  		EnumDisplayMonitors(0, 0, MonitorEnum, (LPARAM)this);
  	}
  };



  int main()
  {
  	cMonitorsVec Monitors;

  	for (int monitorIndex=0;  monitorIndex < Monitors.iMonitors.size(); monitorIndex++)
  	{
  		std::wcout << "Screen id: " << monitorIndex << std::endl;
  		std::wcout << "-----------------------------------------------------" << std::endl;
  		std::wcout << " - screen left-top corner coordinates : (" << Monitors.rcMonitors[monitorIndex].left
  								   << "," << Monitors.rcMonitors[monitorIndex].top
  			                                           << ")" << std::endl;
  		std::wcout << " - screen dimensions (width x height) : (" << std::abs(Monitors.rcMonitors[monitorIndex].right - Monitors.rcMonitors[monitorIndex].left)
  								   << "," << std::abs(Monitors.rcMonitors[monitorIndex].top - Monitors.rcMonitors[monitorIndex].bottom)
  								   << ")" << std::endl;
  		std::wcout << "-----------------------------------------------------" << std::endl;
  	}
  }

The previous code can be also found under here_.

Conclusion
~~~~~~~~~~
This post introduced a small example of how to retrieve the coordinates and dimensions of the connected monitors using C++ on Windows in the case of a multi-monitors setup.
The retrieved coordinates can then be used in capturing the screens content using the snippets from the previous blogs  (`Capturing the screen on Windows in C++ using OpenCV`_ \& `Capturing the screen on Windows in C++ using GDI+`_)

Share this blog
~~~~~~~~~~~~~~~~

.. raw:: html

  <div id="share">
    <a class="facebook" href="https://www.facebook.com/share.php?u=https://superkogito.github.io/blog/2020/09/28/loop_monitors_details_in_cplusplus.html&title=How%20to%20loop%20over%20monitors%20and%20get%20their%20coordinates%20on%20Windows%20in%20C++?"                target="blank"><i class="fa fa-facebook"></i></a>
    <a class="twitter"  href="https://twitter.com/intent/tweet?url=https://superkogito.github.io/blog/2020/09/28/loop_monitors_details_in_cplusplus.html&text=How%20to%20loop%20over%20monitors%20and%20get%20their%20coordinates%20on%20Windows%20in%20C++?"                 target="blank"><i class="fa fa-twitter"></i></a>
    <a class="linkedin" href="https://www.linkedin.com/shareArticle?mini=true&url=https://superkogito.github.io/blog/2020/09/28/loop_monitors_details_in_cplusplus.html&title=How%20to%20loop%20over%20monitors%20and%20get%20their%20coordinates%20on%20Windows%20in%20C++?" target="blank"><i class="fa fa-linkedin"></i></a>
    <a class="reddit"   href="http://www.reddit.com/submit?url=https://superkogito.github.io/blog/2020/09/28/loop_monitors_details_in_cplusplus.html&title=How%20to%20loop%20over%20monitors%20and%20get%20their%20coordinates%20on%20Windows%20in%20C++?"                    target="blank"><i class="fa fa-reddit"></i></a>
  </div>


.. update:: 8 Apr 2022

   👨‍💻 edited and review were on 08.04.2022

References and Further readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- EnumDisplayMonitors function (winuser.h), Microsoft, https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors
- Enumeration and Display Control, Microsoft, https://docs.microsoft.com/en-us/windows/win32/gdi/enumeration-and-display-control
- Multi-monitor Screenshots only 2 monitors in C++ with WinApi, Stackoverflow, https://stackoverflow.com/questions/37132196/multi-monitor-screenshots-only-2-monitors-in-c-with-winapi


.. _`Capturing the screen on Windows in C++ using OpenCV` : https://superkogito.github.io/blog/CaptureScreenUsingOpenCv.html
.. _`Capturing the screen on Windows in C++ using GDI+` : https://superkogito.github.io/blog/CaptureScreenUsingGdiplus.html
.. _`Comparing screen capturing using GDI+ and OpenCV on Windows in C++` : https://superkogito.github.io/blog/CaptureSceenshotUsingGdiplusVSCaptureSceenshotUsingOpenCV.html
.. _`Win32 API` : https://docs.microsoft.com/en-us/windows/win32/
.. _here : https://gist.github.com/SuperKogito/c31c0c0f9e69e484a1740b67a207a5c1
