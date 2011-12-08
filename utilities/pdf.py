#!/usr/bin/env python
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
import StringIO
import sys

def pdf_to_text(file_pointer):
    # debug option
    debug = 0
    
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFDocument.debug = debug
    PDFParser.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug

    pagenos = set()
    password = ''
    maxpages = 0
    codec = 'utf-8'
    laparams = LAParams()
    rsrcmgr = PDFResourceManager()
    outfp = StringIO.StringIO()
    
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    
    process_pdf(rsrcmgr, device, file_pointer, pagenos, maxpages=maxpages, password=password)

    text_string = outfp.getvalue()
    
    outfp.close()
    device.close()
    
    return text_string
