- divide an image using opencv in multiple blocks
- divide an image using gdiplus in mutliple blocks
- benchmark tests to compare both approaches


code:
-----




/*
 * author Ayoub malek
 * date   July 2020
 *
 * divide image experiment using OpenCv.
 *
 */

#include <Windows.h>
#include <minmax.h>
#include <gdiplus.h>
#include <SDKDDKVer.h>
#pragma comment(lib,"gdiplus.lib")
#include "atlimage.h"

#include <opencv2/opencv.hpp>
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include <opencv2/core/utils/filesystem.hpp>
#include "stdafx.h"

using namespace std;
using namespace cv;


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
	else if (dataFormat.compare("png") == 0) {
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
					std::cout << "[postShotsProc] Cannot save block_" << std::to_string(x0) << "_" << std::to_string(y0) << "to png" << std::endl;

				// update starting coordinates
				x0 = x0 + blockWidth;

				// append to vec
				blocks.push_back(pngbytes);
		}
		// update starting coordinates
		y0 = y0 + blockHeight;
	}
}


int divideImage(const cv::Mat& img, const int blockWidth, const int blockHeight, std::vector<cv::Mat>& blocks)
{
	int imgWidth = img.cols;
	int imgHeight = img.rows;

	/* Checking if the image was passed correctly */
	if (!img.data || img.empty())
	{
		std::wcout << "Image Error: Cannot load image to divide." << std::endl;
		exit(1);
	}

	std::wcout << "IMAGE SIZE: " << "(" << imgWidth << "," << imgHeight << ")" << std::endl;

	// init block dimensions
	int bwSize;
	int bhSize;

	int y0 = 0;
	while (y0 < imgHeight)
	{
		bhSize = ((y0 + blockHeight) > imgHeight) * (blockHeight - (y0 + blockHeight - imgHeight)) + ((y0 + blockHeight) <= imgHeight) * blockHeight;

		int x0 = 0;
		while (x0 < imgWidth)
		{
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


/** Small dumb tool (de)compressing cin to cout. It holds all input in memory,
  * so don't use it for huge files. */
int main()
{
	// init vars
	const int blockw = 128;
	const int blockh = 128;
	std::vector<cv::Mat> blocks;

	// read png
	Mat image = cv::imread("Lenna.png", IMREAD_UNCHANGED);
	cv::imshow("Display window", image);

	// divide image into multiple blocks
	int divideStatus = divideImage(image, blockw, blockh, blocks);

	// debug: save blocks
	cv::utils::fs::createDirectory("outputDir");

	for (int j = 0; j < blocks.size(); j++)
	{
		std::string blockId = std::to_string(j);
		std::string blockImgName = "outputDir/block#" + blockId + ".png";
		imwrite(blockImgName, blocks[j]);
	}




	// Gdiplus method

	// initilialize GDI+
	CoInitialize(NULL);
	ULONG_PTR token;
	Gdiplus::GdiplusStartupInput tmp;
	Gdiplus::GdiplusStartup(&token, &tmp, NULL);

	std::vector<std::vector<BYTE>> imgblocks;

	// load img
	Gdiplus::Bitmap* bitmap = Gdiplus::Bitmap::FromFile(L"Lenna.png");

	// divide img
	int divstatus = gdiplusDivideImage(bitmap, blockw, blockh, imgblocks);

	// save blocks
	if (!CreateDirectory(L"outputDir2", NULL))
	{
		std::wcout << "Directory Error: Cannot create directory for blocks." << std::endl;
		return 1;
	}

	for (int j = 0; j < imgblocks.size(); j++)
	{
		std::string blockId = std::to_string(j);
		std::string blockImgName = "outputDir2/block#" + blockId + ".png";

		// write from memory to file for testing:
		std::ofstream fout(blockImgName, std::ios::binary);
		fout.write((char*)imgblocks[j].data(), imgblocks[j].size());
	}


	return 0;
}
