#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <fstream>

#include <QDebug>
#include <QDir>
#include <QFile>
#include <QImage>
#include <QRgb>
#include <QStringList>
#include <QTextCodec>
#include <QXmlStreamReader>

#include <sys/stat.h>

QString
makeFilename(const QString &outputDir, const QString &s, int instance)
{
  QString s2 = s;
  if (s == ":")
    s2 = "COLON";
  else if (s == ".")
    s2 = "POINT";
  else if (s == " ")
    s2 = "SPACE";
  else if (s == "/")
    s2 = "SLASH";
  else if (s == "*")
    s2 = "STAR";

  const QString filename = s2 + "_" + QString("%1").arg(instance, 2, 10, QChar('0')) + ".png";
  return QDir(outputDir).filePath(filename);
}

class FontImageExtractor
{
public:

  void extractImages(const QString &filepath, const QString &outputDirectory);

private:
  void processCharacterFromXml(const QString &outputDirectory, const QString &s, QXmlStreamReader &reader);
  QImage processCharacterDataFromXml(QXmlStreamReader &reader);

};

void
FontImageExtractor::extractImages(const QString &filepath, const QString &outputDirectory)
{
  //B:TODO:UGLY: errors are not checked correctly ! What if file is corrupt ?

  QFile file(filepath);
  const bool ok = file.open(QFile::ReadOnly);
  if (!ok) {
    std::cerr<<"ERROR: unable to open font file: "<<filepath.toStdString()<<"\n";
    return;
  }
  
  QDir dir(outputDirectory);
  if (! dir.exists()) {
    std::cerr<<"ERROR: output directory does not exist: "<<outputDirectory.toStdString()<<"\n";
    return;
  }

  QXmlStreamReader reader(&file);

  //Reading font from xml
  while (!reader.atEnd()) {
    if (reader.name() == "font" &&
        reader.tokenType() == QXmlStreamReader::StartElement) {
      //font->setName(reader.attributes().value(QStringLiteral("name")).toString());

      while (!(reader.tokenType() == QXmlStreamReader::EndElement &&
               reader.name() == "font") &&
             !reader.atEnd()) {
        QXmlStreamReader::TokenType token = reader.readNext();
        if (reader.name() == "letter" &&
            token == QXmlStreamReader::StartElement) {
          const QString s = reader.attributes().value(QStringLiteral("char")).toString();
	  processCharacterFromXml(outputDirectory, s, reader);
        }
      }
    }
    reader.readNext();
  }
  //reading from xml finished

  file.close();

}

void
FontImageExtractor::processCharacterFromXml(const QString &outputDir, const QString &s, QXmlStreamReader &reader)
{
  int count = 0;

  while (!(reader.tokenType() == QXmlStreamReader::EndElement &&
           reader.name() == "letter") &&
         !reader.atEnd()) {
    QXmlStreamReader::TokenType tokenMain = reader.readNext();

    if (reader.name() == "anchor" &&
        tokenMain == QXmlStreamReader::StartElement) {

      reader.readNext();
      while (!(reader.tokenType() == QXmlStreamReader::EndElement &&
               reader.name() == "anchor") &&
             !reader.atEnd()) {
        QXmlStreamReader::TokenType token = reader.readNext();
        if (token == QXmlStreamReader::StartElement) {
          if (reader.name() == "upLine") {
            reader.readNext();
          }
          if (reader.name() == "baseLine") {
            reader.readNext();
          }
          if (reader.name() == "leftLine") {
            reader.readNext();
          }
          if (reader.name() == "rightLine") {
            reader.readNext();
          }
        }
      }
    }
    if (reader.name() == "picture" &&
        tokenMain == QXmlStreamReader::StartElement) {
      const QImage img = processCharacterDataFromXml(reader);
      

      ++count;
      const QString filename = makeFilename(outputDir, s, count);

      struct stat sb;   
      stat(filename.toStdString().c_str(), &sb);
      if ((sb.st_mode & S_IFMT) == S_IFREG) {
	std::cerr<<"WARNING: "<<filename.toStdString()<<" already exists !!!\n";
	std::cerr<<"   The output directory was not empty or the letter: "<<s.toStdString()<<" is probably duplicated in the font file\n";
      }
  
      const bool writeOk = img.save(filename);
      if (! writeOk) {
	std::cerr<<"ERROR: unable to save "<<filename.toStdString()<<"\n";
	std::cerr<<"++"<<s.toStdString()<<"++\n";
      }

    }
  }

}

QImage
FontImageExtractor::processCharacterDataFromXml(QXmlStreamReader &reader)
{
  int imgWidth = 0, imgHeight = 0, format = 0;
  QString pixelsData;

  //const int id = reader.attributes().value(QStringLiteral("id")).toString().toInt();

  while (!(reader.tokenType() == QXmlStreamReader::EndElement &&
           reader.name() == "imageData") &&
         !reader.atEnd()) {
    QXmlStreamReader::TokenType token = reader.readNext();
    if (token == QXmlStreamReader::StartElement) {
      if (reader.name() == "width") {
        reader.readNext();
        imgWidth = reader.text().toString().toInt();
      }
      if (reader.name() == "height") {
        reader.readNext();
        imgHeight = reader.text().toString().toInt();
      }
      if (reader.name() == "format") {
        reader.readNext();
        format = reader.text().toString().toInt();
      }
      if (reader.name() == "data") {
        reader.readNext();
        pixelsData = reader.text().toString();
      }
    }
  }

  QImage img(imgWidth, imgHeight, static_cast<QImage::Format>(format));

  QStringList pixels = pixelsData.split(QStringLiteral(","));
  assert(pixels.size() == imgWidth * imgHeight);
  QStringList::const_iterator it = pixels.constBegin();

  if (img.format() == QImage::Format_ARGB32) {
    for (int y = 0; y < imgHeight; ++y) {
      QRgb *d = (QRgb *)img.scanLine(y);
      for (int x = 0; x < imgWidth; ++x) {
        d[x] = it->toUInt(); //B: conversion from QString to UInt !
        ++it;
      }
    }
  } else {
    for (int y = 0; y < imgHeight; ++y) {
      for (int x = 0; x < imgWidth; ++x) {
        img.setPixel(x, y, it->toUInt()); //B: conversion from QString to UInt !
        ++it;
      }
    }
  }

  return img;
}


int
main(int argc, char *argv[])
{
  if (argc != 3) {
    std::cerr<<"Usage: "<<argv[0]<<" fontFilename outputDirectory\n"; 
    return 1;
  }

  QString fontFilename = argv[1];
  QString outputDirectory = argv[2];

  FontImageExtractor().extractImages(fontFilename, outputDirectory);

  return 0;
}
