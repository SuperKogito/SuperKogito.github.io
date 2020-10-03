[01-10-2020] Divide an image into blocks using OpenCV in C++
=============================================================

.. meta::
  :description: Divide an image into multiple blocks with fixed height and width using OpenCV in C++
  :keywords: Image divide, C++, OpenCV
  :author: Ayoub Malek

.. post:: October 01, 2020
  :tags: [C++], [OpenCV], [Windows]
  :category: C++
  :author: Ayoub Malek
  :location: Munich
  :language: English

-----------------------

Often you will need to divide an image into multiple blocks of a certain height and width to apply a certain transformation or would like to compare two images block-wise.
This blog will provide a short explanation and a C++ implementation for how to divide an image into multiple blocks with custom height and width.

| ***Keywords***:  OpenCV, C++, Windows, Divide image into blocks

Approach
--------

There are various ways of approaching this problem; most approaches out there compute the number of blocks in xy-directions and use for loops to cut the blocks.
In this blog, the dimensions of the blocks are prioritized, therefore, we will need to make sure to crop the side blocks and lower blocks correctly even if their dimensions are different from the other blocks.

To elaborate on this a bit more: if the image width = 512 px and the block width = 128 px -> we will get 512 / 128 = 4 blocks.
However if the image width = 576 px and the block width = 128 px -> we should get 4 blocks with 128 px and 1 block with width 64 px.
Therefore on each loop we need to check/ compute the block dimensions.
Moreover, to keep the code fast and optimal, we will use while loops, that will iterate over the y-coordinates (Top to bottom) then the x-coordinates (left to right).


--> The previously described steps are implemented in the following snippet:


.. code-block:: C++
  :linenos:

  #include <Windows.h>
  #include <opencv2/opencv.hpp>
  #include "opencv2/imgproc.hpp"
  #include "opencv2/highgui.hpp"
  #include <opencv2/core/utils/filesystem.hpp>


  int divideImage(const cv::Mat& img, const int blockWidth, const int blockHeight, std::vector<cv::Mat>& blocks)
  {
   // Checking if the image was passed correctly
   if (!img.data || img.empty())
   {
  		std::wcout << "Image Error: Cannot load image to divide." << std::endl;
    	return EXIT_FAILURE;
   }

   // init image dimensions
   int imgWidth = img.cols;
   int imgHeight = img.rows;
   std::wcout << "IMAGE SIZE: " << "(" << imgWidth << "," << imgHeight << ")" << std::endl;

   // init block dimensions
   int bwSize;
   int bhSize;

   int y0 = 0;
   while (y0 < imgHeight)
   {
     // compute the block height
     bhSize = ((y0 + blockHeight) > imgHeight) * (blockHeight - (y0 + blockHeight - imgHeight)) + ((y0 + blockHeight) <= imgHeight) * blockHeight;

  	 int x0 = 0;
  	 while (x0 < imgWidth)
  	 {
       // compute the block height
  	   bwSize = ((x0 + blockWidth) > imgWidth) * (blockWidth - (x0 + blockWidth - imgWidth)) + ((x0 + blockWidth) <= imgWidth) * blockWidth;

  		 // crop block
  		 blocks.push_back(img(cv::Rect(x0, y0, bwSize, bhSize)).clone());

  		 // update x-coordinate
  		 x0 = x0 + blockWidth;
  	 }

  	 // update y-coordinate
  	 y0 = y0 + blockHeight;
   }
   return EXIT_SUCCESS;
  }

The previous snippet represents a small function with an integer output reflecting the run status of the function.
:code:`divideImage()` takes in 4 inputs which are the image to divide, the blocks width, the blocks height and a vector variable to store the cropped blocks in.


The main call
-------------
Let's call the previous function in a main function and save the resulting blocks in a defined directory to visualize the results and verify, that the code is doing what it is supposed to do.
For the purpose of this test I chose to use the famous Lenna picture, that can downloaded from here_.
In code this can be done as follows:

.. code-block:: C++
  :linenos:

  int main()
  {
   // init vars
   const int blockw = 128;
   const int blockh = 128;
   std::vector<cv::Mat> blocks;

   // read png image
   Mat image = cv::imread("Lenna.png", IMREAD_UNCHANGED);
   cv::imshow("Display window", image);

   // divide image into multiple blocks
   int divideStatus = divideImage(image, blockw, blockh, blocks);

   // debug: save blocks
   cv::utils::fs::createDirectory("blocksFolder");
   for (int j = 0; j < blocks.size(); j++)
   {
     std::string blockId = std::to_string(j);
  	 std::string blockImgName = "blocksFolder/block#" + blockId + ".png";
  	 imwrite(blockImgName, blocks[j]);
   }

   return 0;
  }

The full code can be found in this `gist: DivideImageUsingOpenCv.cpp`_.

Result
--------
The resulting blocks should look something like this:

.. image:: ../_static/blog-plots/opencv/divided_lenna.png
   :align: center
   :scale: 80%

.. raw:: html

   <div class="clt">
   <center><a href="../figures/fig19.html" >Figure 19: divided image into multiple blocks </a> </center>
   </div>

Limitations
-----------
- In some cases the user might want to have equally sized blocks or a predefined number of blocks. Therefore, in such case, the dimensions of the blocks should be pre-computed if the user wants to use this snippet. However, tweaking the code for such use-case should be simple to do.
- NB: This code has only tested on Windows 10.

Conclusion
----------
To summarize, in this post we introduced a small example of how to divide an image into multiple blocks with predefined height and width using OpenCV in C++.
We also went through saving the resulting blocks to the hard drive in order to verify that the code is functional.
The code is fairly simple and supports various image encoding types(`PNG`, `JPEG` etc.) but do we need OpenCV to achieve this? can this be done differently?
The next blog should provide an answer for this.

References and Further readings
--------------------------------
.. [1] Crop a big picture into several small size pictures, Graphic design, https://graphicdesign.stackexchange.com/questions/30008/crop-a-big-picture-into-several-small-size-pictures
.. [2] Divide 256*256 image into 4*4 blocks, Matlab, Stackoverflow, https://www.mathworks.com/matlabcentral/answers/33103-divide-256-256-image-into-4-4-blocks
.. [3] Divide an image into lower regions, OpenCV, https://answers.opencv.org/question/53694/divide-an-image-into-lower-regions/

.. _`gist: DivideImageUsingOpenCv.cpp` : https://gist.github.com/SuperKogito/0d6f839a04f17999aad8e4eac87f2411
.. _here : https://en.wikipedia.org/wiki/Lenna#/media/File:Lenna_(test_image).png
