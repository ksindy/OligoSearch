from django.shortcuts import render
from django import forms
import xlrd
import urllib.request
import re

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

from .forms import UploadFileForm, RefForm, ChrLocForm, ColumnDropForm
#Access forms from match_oligo/forms.py

def import_excel_view(request):
    new_line_char = "--"
    new_line = 0
    #Adds a new line character between uploaded file information when new_line > 0

    if request.method == "POST":
    #if there is data to be submitted continue with script
        form1 = UploadFileForm(request.POST, request.FILES)
        form2 = RefForm(request.POST)
        form3 = ChrLocForm(request.POST)
        form4 = ColumnDropForm(request.POST)
        #handles for user submitted data.
        ValidForm1 = False
        #Grants entry into oligo search loop
        if form1.is_valid() and (form4.is_valid()) and (form2.is_valid() or form3.is_valid()):
        #Validates user input for oligo files and at least one reference
            check = (form2.is_valid()), (form3.is_valid())
            if form1.is_valid() and all(check):
                raise forms.ValidationError('OOPS! You submitted two types of reference data. Either paste your reference or identify a chromosome location.')
                #Raises error if there is user input for both references
            if form1.is_valid():
                oligo_input =  request.FILES.getlist('file')
                #Accesses 'file' from match_oligo/forms.py and uses .getlist to access all items in the MultiValueDict
                oligo_column_input = request.POST['oligo_column']
                name_column_input = request.POST['name_column']
                name_match_list = []
                sheet_info_list = []
                reference_info = []
                #creates empty  list where  matches from all files will be stored
                ValidForm1 = True
                #Grants entry into oligo search loop if True
            if form2.is_valid():
                reference = (form2.cleaned_data['reference']).upper().replace(" ","")
                #accesses validated form input
                #reference = request.POST['reference'] #access unvalidated form input
                rc_reference = reverse_complement(reference)
                ref_length = str(len(reference))
                reference_info.extend(("The following number of nucleotides were searched: {}".format(ref_length),))
            elif form3.is_valid():
                    chrom = request.POST['chr']
                    loc_start = request.POST['loc_start']
                    loc_stop = request.POST['loc_stop']
                    #access user input for chromsome location
                    url = "http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment=chr{}:{},{}".format(chrom, loc_start, loc_stop)
                    chr_url = urllib.request.urlopen(url)
                    chr_url_read = chr_url.read()
                    chr_url_decode = chr_url_read.decode('utf-8')
                    #open, read, and decode text from the UCSC das url
                    chr_input = re.sub('<.+>', '', chr_url_decode)
                    chr_input_strip = chr_input.replace('\n','')
                    reference = chr_input_strip.upper().replace(" ", "")
                    rc_reference = reverse_complement(reference)
                    #remove all non-sequence text between <>, remove newline, and convert to all caps
                    reference_info.extend(("Chromosome {}: {}-{}".format(chrom,loc_start,loc_stop),))
                    reference_info.extend(("url: {}".format(url),))
        if ValidForm1:
        #ValidForm1 is True if form1 (excel oligo input) is valid
            for xlsfile in oligo_input:
                if new_line > 0:
                    name_match_list.extend((new_line_char,))
                    #adds new line character if a file already had a match (new_line > 0)
                new_line = 0
                #reset- if a file does not have a match a new line character will not be added for next file
                saw_file = 0
                #reset- if first time seeing a file (saw_file = 0) name of file will be displayed
                book = xlrd.open_workbook(file_contents=xlsfile.read())
                #Uses xlrd package to open and read submitted file as excel sheet.
                #Creates string from 'ExcelInMemoryUploadedFile' with read() function.
                sheet = book.sheet_by_index(0)
                #identifies which sheet in the excel file to use
                sheet_info_list.extend(("{}".format(xlsfile),))
                sheet_info_list.extend(("Sheet: {}".format(sheet.name),))
                sheet_info_list.extend(("Total number of oligos searched: {}".format(sheet.nrows),))
                sheet_info_list.extend((new_line_char,))
                #displays each of the excel file's information
                for i in range(sheet.nrows):
                    oligo = (sheet.cell_value(
                                rowx=i,
                                colx=int(oligo_column_input))
                                .upper().replace(" ",""))
                    if i < sheet.nrows and oligo != "" and ((oligo in reference) or (oligo in rc_reference)):
                        name = sheet.cell_value(rowx=i, colx=int(name_column_input))
                        name_match = str(name)
                        if saw_file < 1:
                                xls_match_file_name = "{}:".format(xlsfile)
                                name_match_list.extend((xls_match_file_name,))
                                name_match_list.extend((name_match,))
                                saw_file += 1
                                #if first time seeing a match in file (saw_file = 0) name of file and match will be displayed
                        else:
                            name_match_list.extend((name_match,))
                            #if file already has a match (saw_file > 0) match will be be displayed
                            new_line += 1
            return render(request, 'match_oligo/output.html', {'var': name_match_list, 'search_param': sheet_info_list, 'ref_info': reference_info})
    else:
        form1 = UploadFileForm()
        form2 = RefForm()
        form3 = ChrLocForm()
        form4 = ColumnDropForm()
    return render(request, 'match_oligo/user_input.html', {'form1': form1, 'form2': form2, 'form3':form3, 'form4':form4, })
