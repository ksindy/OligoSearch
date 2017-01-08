from django.shortcuts import render
from django import forms
import xlrd
import urllib.request
import re

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

def mismatch (string1, string2):
    mismatches = 0
    for (nucleotide1, nucleotide2) in zip(string1, string2):
        if nucleotide1 != nucleotide2:
            mismatches += 1
    return(mismatches)

def exact_patterns(text, pattern):
    pattern_location = ''
    pattern_matches = ''
    regex_pattern = re.compile('(?={0})'.format(pattern))
    matches = regex_pattern.finditer(text)
    for match in matches:
        pattern_location += str(match.start())+','+'\t'
    return(pattern_location, pattern_matches)

def approximate_patterns(text, pattern, max_mismatches):
    text = text.upper().replace(" ","")
    pattern = pattern.upper().replace(" ","")
    regex = re.compile('[^agctuAGCTU]')
    pattern = regex.sub('', pattern)
    pattern_matches = ''
    pattern_location = ''
    pattern_end = 0
    pattern_found = False
    add_base = False
    if pattern == '':
        return ('')
    else:
        for i, base in enumerate(text):
            pattern_matches += '<i></i>'
            query_pattern = text[i:i+len(pattern)]
            add_base = False
            last_base = len(text)

            if mismatch(pattern, query_pattern) <= max_mismatches and not pattern_found and len(query_pattern)==len(pattern):
                pattern_matches += '<u><font color="red">'
                pattern_found = True
                pattern_end = i + (len(pattern)-1)
                pattern_location += str(i+1)+','+'\t'

            elif mismatch(pattern, query_pattern) <= max_mismatches and pattern_found and len(query_pattern)==len(pattern):
                pattern_end = i + (len(pattern)-1)
                pattern_location += str(i+1)+','+'\t'

            if i == pattern_end and pattern_found:
                pattern_matches += base
                pattern_matches +='</u></font>'
                pattern_end = 0
                add_base = True
                pattern_found = False

            if i == last_base-1 and pattern_found:
                pattern_matches += '</u></font>'

            if not add_base:
                pattern_matches += base

        return(pattern_location, pattern_matches )

def approximate_patterns_oligo(text, pattern, max_mismatches):
    text = text.upper().replace(" ","")
    pattern = pattern.upper().replace(" ","")
    pattern_matches = ''
    pattern_location = ''
    pattern_end = 0
    pattern_found = False
    add_base = False
    oligo_found = 0
    oligo_string = ''
    if pattern == '':
        return ('')
    else:
        for i, base in enumerate(text):
            pattern_matches += '<i></i>'
            query_pattern = text[i:i+len(pattern)]
            add_base = False
            last_base = len(text)
            if mismatch(pattern, query_pattern) <= max_mismatches and not pattern_found and len(query_pattern)==len(pattern):
                pattern_matches += '<u><font color="red">'
                pattern_found = True
                pattern_end = i + (len(pattern)-1)
                pattern_location += str(i+1)+','+'\t'
                oligo_found += 1

            elif mismatch(pattern, query_pattern) <= max_mismatches and pattern_found and len(query_pattern)==len(pattern):
                pattern_end = i + (len(pattern)-1)
                pattern_location += str(i+1)+','+'\t'
                oligo_found += 1

            if i == pattern_end and pattern_found:
                pattern_matches += base
                pattern_matches +='</u></font>'
                pattern_end = 0
                add_base = True
                pattern_found = False

            if i == last_base-1 and pattern_found:
                pattern_matches += '</u></font>'

            if not add_base:
                pattern_matches += base

        return(oligo_found)

from .forms import UploadFileForm, RefForm, ChrLocForm, ColumnDropForm, user_sequence_input, mismatch_input
#Access forms from match_oligo/forms.py

def import_excel_view(request):
    new_line_char = "--"
    new_line = 0
    #Adds a new line character between uploaded file information when new_line > 0

    if request.method == "POST":

        oligo_input =  request.FILES.getlist('file')
        # Accesses 'file' from match_oligo/forms.py and uses .getlist to access all items in the MultiValueDict
        oligo_column_input = request.POST['oligo_column']
        name_column_input = request.POST['name_column']
        mismatches_choice = int(request.POST.get('mismatches'))
        reference = request.POST['reference']
        chrom = request.POST['chr']
        loc_start = request.POST['loc_start']
        loc_stop = request.POST['loc_stop']
        user_input_oligo = request.POST['sequence']
        mismatch_form = request.POST['mismatches']

        name_match_list = []
        sheet_info_list = []
        reference_info = []
        #creates empty  list where  matches from all files will be stored

        rc_reference = reverse_complement(reference)
        if reference != '':
            ref_length = str(len(reference))
            reference_info.extend(("The following number of nucleotides were searched: {}".format(ref_length),))

        if (chrom and loc_start and loc_stop) == '':
            if reference == '':
                raise forms.ValidationError(
                    'OOPS! You need to enter at least one reference.')

        if (chrom and loc_start and loc_stop) != '':
            if reference != '':
                raise forms.ValidationError(
                    'OOPS! There are two references. Either copy and paste a reference or enter the chromosome location.')

        if (chrom and loc_start and loc_stop) != '':
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
            reference_info.extend(("{}".format(url),))

        if not oligo_input and user_input_oligo == '':
            raise forms.ValidationError(
                'OOPS! You need to enter at least one item to search. Either copy and paste an oligonucleotide or upload an excel file.')

        if oligo_input and user_input_oligo != '':
            raise forms.ValidationError(
                'OOPS! There are two oligonucleotide sources. Either manually enter a sequence or upload an excel sheet.')
        if oligo_input:
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
                    regex = re.compile('[^agctuAGCTU]')
                    oligo = regex.sub('', oligo)
                    #todo add reference location to excel output
                    if i < sheet.nrows and oligo != "" and mismatches_choice != 0:
                        name = sheet.cell_value(rowx=i, colx=int(name_column_input))
                        name_match = str(name)
                        if approximate_patterns_oligo(reference, oligo, mismatches_choice) > 0:
                            if saw_file < 1:
                                xls_match_file_name = "{}:".format(xlsfile)
                                name_match_list.extend((xls_match_file_name,))
                                name_match_list.extend((name_match,))
                                saw_file += 1
                            else:
                                name_match_list.extend((name_match,))
                                # if file already has a match (saw_file > 0) match will be be displayed
                                new_line += 1

                    elif i < sheet.nrows and oligo != "" and ((oligo in reference) or (oligo in rc_reference)):
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
            user_input_oligo = user_sequence_input()
            reference = RefForm()
            chromosome_form = ChrLocForm()
            col_drop = ColumnDropForm()
            upload = UploadFileForm()
            mismatch_form = mismatch_input()
            mismatch = mismatch_input()
            return render(request, 'match_oligo/main2excel.html', {'var': name_match_list, 'search_param': sheet_info_list, 'ref_info': reference_info, 'reference': reference, 'chromosome_form': chromosome_form,
                          'user_input_oligo': user_input_oligo, 'col_drop': col_drop, 'upload': upload, 'mismatch_form':mismatch_form, 'mismatch':mismatch})

        if user_input_oligo != '':
            bold = approximate_patterns(reference, user_input_oligo, mismatches_choice)

            reference_form = RefForm()
            chromosome_form = ChrLocForm()
            col_drop = ColumnDropForm()
            upload = UploadFileForm()
            mismatch = mismatch_input()
            user_input_oligo = user_sequence_input()
            return render(request, 'match_oligo/main2result.html',
                         {'bold': bold, 'reference_form': reference_form, 'chromosome_form': chromosome_form,
                          'user_input_oligo': user_input_oligo, 'col_drop': col_drop, 'upload': upload, 'mismatch':mismatch})
    else:
        user_input_oligo = user_sequence_input()
        reference = RefForm()
        chromosome_form = ChrLocForm()
        col_drop = ColumnDropForm()
        upload = UploadFileForm()
        mismatch = mismatch_input()


    return render(request, 'match_oligo/main2.html', {'reference': reference, 'chromosome_form': chromosome_form, 'user_input_oligo':user_input_oligo, 'col_drop':col_drop, 'upload':upload, 'mismatch':mismatch})
