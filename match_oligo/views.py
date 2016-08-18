from django.shortcuts import render
from django import forms
import xlrd
from Bio.Seq import Seq
import urllib.request
import re

from .forms import UploadFileForm, RefForm, ChrLocForm
#Access forms from forms.py

def import_excel_view(request):
#define function called 'import_excel_view'
    new_line_char = "--"
    new_line = 0
    #Adds a new line character between uploaded file information when new_line > 0

    if request.method == "POST":
    #if there is data to be submitted continue with script
        form1 = UploadFileForm(request.POST, request.FILES)
        form2 = RefForm(request.POST)
        form3 = ChrLocForm(request.POST)
        #handles assigned to user submitted data for each form.
        ValidForm1 = False
        #Grants entry into oligo search loop if True

        if form1.is_valid() and (form2.is_valid() or form3.is_valid()):
        #Validates user input for oligo files and at least one reference

            check = (form2.is_valid()), (form3.is_valid())
            if form1.is_valid() and all(check):
                raise forms.ValidationError('OOPS! You submitted two types of reference data. Either paste your reference or identify a chromosome location.')
                #Raises error if there is user input for both references

            #SUBMITTED DATA: OLIGO FILE
            if form1.is_valid():
                oligo_input =  request.FILES.getlist('file')
                #Accesses 'file' from match_oligo/forms.py and uses .getlist to access all items in the MultiValueDict
                name_match_list = []
                sheet_info_list = []
                reference_info = []
                #creates empty  list where  matches from all files will be stored
                ValidForm1 = True
                #Grants entry into oligo search loop if True

            #SUBMITTED DATA: REFERENCE PASTE
            if form2.is_valid():
                reference = form2.cleaned_data['reference']
                #accesses validated form input
                    #reference = request.POST['reference']
                    #access unvalidated form input
                reference_upper = reference.upper().replace(" ", "")
                ref_seq = Seq(reference_upper)
                #uses biopython to convert reference into Seq object
                ref_rev_comp = Seq.reverse_complement(ref_seq)
                #uses biopython to create a reverse compliment of the submitted reference data
                ref_length = str(len(ref_seq))
                reference_info.extend(("The following number of nucleotides were searched: {}".format(ref_length),))
                chr_input_seq = ''
                chr_input_rev_seq = ''
                #create empty list of UCSC das url reference variables to prevent error in oligo search loop

            #SUBMITTED DATA: UCSC DAS URL REFERENCE
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
                    chr_input_caps = chr_input_strip.upper().replace(" ", "")
                    #remove all non-sequence text between <>, remove newline, and convert to all caps
                    chr_input_seq = Seq(chr_input_caps)
                    #use biopython to create sequence object out of url text
                    chr_input_rev_seq = Seq.reverse_complement(chr_input_seq)
                    #use biopython to create reverse compiment of sequence
                    reference_info.extend(("Chromosome {}: {}-{}".format(chrom,loc_start,loc_stop),))
                    ref_seq = ''
                    ref_rev_comp = ''
                    #create empty list of paste reference variables to prevent error in oligo search loop

        if ValidForm1:
        #ValidForm1 is True if form1 (excel oligo input) is valid
            for xlsfile in oligo_input:
            #iterates through user uploaded files
                if new_line > 0:
                    name_match_list.extend((new_line_char,))
                    #adds new line character if a file already had a match (new_line > 0)
                new_line = 0
                #reset- if a file does not have a match a new line character will not be added for next file
                saw_file = 0
                #reset- if first time seeing a file (saw_file = 0) name of file will be displayed
                oligo_row = 0
                oligo_col = 2
                name_col = 0
                #variables assigned to row and columns of excel input and needs to be reset for each file

                book = xlrd.open_workbook(file_contents=xlsfile.read())
                #Uses xlrd package to open and read submitted file as excel sheet.
                #Creates string from 'ExcelInMemoryUploadedFile' with read() function.
                sheet = book.sheet_by_index(0)
                #identifies which sheet in the excel file to use
                nrows = sheet.nrows
                #sets handle to number of rows in identified excel sheet

                sheet_info_list.extend(("{}".format(xlsfile),))
                sheet_info_list.extend(("Sheet: {}".format(sheet.name),))
                sheet_info_list.extend(("Total number of oligos searched: {}".format(sheet.nrows),))
                sheet_info_list.extend((new_line_char,))
                #displays each of the excel file's information

                for oligo in range(sheet.nrows):
                #iterates through items in identified file/sheet
                    cell = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
                    #using above variables, sets handle to the cell in the current sheet/file where match search will begin


                    #OLIGO MATCH SCRIPT: add +1 to oligo_row until reach nrows (ie the total number of rows in the sheet)
                    if oligo_row < nrows:
                        oligo_caps = cell.upper().replace(" ", "")
                        oligo_find = ref_seq.find(oligo_caps)
                        oligo_rev_find = ref_rev_comp.find(oligo_caps)
                        oligo_find_url = chr_input_seq.find(oligo_caps)
                        oligo_rev_find_url = chr_input_rev_seq.find(oligo_caps)
                        #uses biopython to look for oligo in reference and reverse compliment of reference
                        if oligo_find == -1 and oligo_find_url == -1 and oligo_rev_find == -1 and oligo_rev_find == -1 or cell == '':
                            oligo_row += 1
                            #if there is no match (-1), go to next row (add +1 to oligo_row)
                        elif oligo_find != -1 or oligo_find_url != -1 or oligo_rev_find != -1 or oligo_rev_find_url != -1:
                        #if there is a match (not -1, any other number is the index of the match), set handle to that cell name
                            name = sheet.cell_value(rowx=oligo_row, colx=name_col)
                            #assign handle to cell with match
                            name_match = str(name)
                            #create string from cell name
                            if saw_file < 1:
                                xls_match_file_name = "%s:" % xlsfile
                                name_match_list.extend((xls_match_file_name,))
                                name_match_list.extend((name_match,))
                                #if first time seeing a match in file (saw_file = 0) name of file and match will be displayed
                            else:
                                name_match_list.extend((name_match,))
                                #if file already has a match (saw_file > 0) match will be be displayed
                            saw_file += 1
                            oligo_row += 1
                            new_line += 1

            return render(request, 'match_oligo/output.html', {'var': name_match_list, 'search_param': sheet_info_list, 'ref_info': reference_info})

    else:
        form1 = UploadFileForm()
        form2 = RefForm()
        form3 = ChrLocForm()

    return render(request, 'match_oligo/user_input.html', {'form1': form1, 'form2': form2, 'form3':form3})
