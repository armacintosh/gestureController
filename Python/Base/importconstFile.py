# Generated with SMOP  0.41
from libsmop import *
# importconstFile.m

    
@function
def importconstFile(filename=None,startRow=None,endRow=None,*args,**kwargs):
    varargin = importconstFile.varargin
    nargin = importconstFile.nargin

    #IMPORTFILE Import numeric data from a text file as a matrix.
#   CONSTFILE = IMPORTFILE(FILENAME) Reads data from text file FILENAME for
#   the default selection.
    
    #   CONSTFILE = IMPORTFILE(FILENAME, STARTROW, ENDROW) Reads data from rows
#   STARTROW through ENDROW of text file FILENAME.
    
    # Example:
#   constFile = importfile('constFile.txt', 1, 27);
    
    #    See also TEXTSCAN.
    
    # Auto-generated by MATLAB on 2018/02/02 15:38:02
    
    ## Initialize variables.
    delimiter=cellarray([',',';','=','%'])
# importconstFile.m:17
    if nargin <= 2:
        startRow=1
# importconstFile.m:19
        endRow=copy(inf)
# importconstFile.m:20
    
    ## Read columns of data as text:
# For more information, see the TEXTSCAN documentation.
    formatSpec='%s%s%s%s%[^\n\r]'
# importconstFile.m:25
    ## Open the text file.
    fileID=fopen(filename,'r')
# importconstFile.m:28
    ## Read columns of data according to the format.
# This call is based on the structure of the file used to generate this
# code. If an error occurs for a different file, try regenerating the code
# from the Import Tool.
    textscan(fileID,'%[^\n\r]',startRow(1) - 1,'WhiteSpace','','ReturnOnError',false)
    dataArray=textscan(fileID,formatSpec,endRow(1) - startRow(1) + 1,'Delimiter',delimiter,'TextType','string','ReturnOnError',false,'EndOfLine','\r\n')
# importconstFile.m:35
    for block in arange(2,length(startRow)).reshape(-1):
        frewind(fileID)
        textscan(fileID,'%[^\n\r]',startRow(block) - 1,'WhiteSpace','','ReturnOnError',false)
        dataArrayBlock=textscan(fileID,formatSpec,endRow(block) - startRow(block) + 1,'Delimiter',delimiter,'TextType','string','ReturnOnError',false,'EndOfLine','\r\n')
# importconstFile.m:39
        for col in arange(1,length(dataArray)).reshape(-1):
            dataArray[col]=concat([[dataArray[col]],[dataArrayBlock[col]]])
# importconstFile.m:41
    
    ## Close the text file.
    fclose(fileID)
    ## Convert the contents of columns containing numeric text to numbers.
# Replace non-numeric text with NaN.
    raw=repmat(cellarray(['']),length(dataArray[1]),length(dataArray) - 1)
# importconstFile.m:50
    for col in arange(1,length(dataArray) - 1).reshape(-1):
        raw[arange(1,length(dataArray[col])),col]=mat2cell(dataArray[col],ones(length(dataArray[col]),1))
# importconstFile.m:52
    
    numericData=NaN(size(dataArray[1],1),size(dataArray,2))
# importconstFile.m:54
    # Converts text in the input cell array to numbers. Replaced non-numeric
# text with NaN.
    rawData=dataArray[2]
# importconstFile.m:58
    for row in arange(1,size(rawData,1)).reshape(-1):
        # Create a regular expression to detect and remove non-numeric prefixes and
    # suffixes.
        regexstr='(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)'
# importconstFile.m:62
        try:
            result=regexp(rawData(row),regexstr,'names')
# importconstFile.m:64
            numbers=result.numbers
# importconstFile.m:65
            invalidThousandsSeparator=copy(false)
# importconstFile.m:68
            if numbers.contains(','):
                thousandsRegExp='^\d+?(\,\d{3})*\.{0,1}\d*$'
# importconstFile.m:70
                if isempty(regexp(numbers,thousandsRegExp,'once')):
                    numbers=copy(NaN)
# importconstFile.m:72
                    invalidThousandsSeparator=copy(true)
# importconstFile.m:73
            # Convert numeric text to numbers.
            if logical_not(invalidThousandsSeparator):
                numbers=textscan(char(strrep(numbers,',','')),'%f')
# importconstFile.m:78
                numericData[row,2]=numbers[1]
# importconstFile.m:79
                raw[row,2]=numbers[1]
# importconstFile.m:80
        finally:
            pass
    
    ## Split data into numeric and string columns.
    rawNumericColumns=raw(arange(),2)
# importconstFile.m:89
    rawStringColumns=string(raw(arange(),concat([1,3,4])))
# importconstFile.m:90
    ## Exclude rows with non-numeric cells
    I=logical_not(all(cellfun(lambda x=None: (isnumeric(x) or islogical(x)) and logical_not(isnan(x)),rawNumericColumns),2))
# importconstFile.m:94
    
    rawNumericColumns[I,arange()]=[]
# importconstFile.m:95
    rawStringColumns[I,arange()]=[]
# importconstFile.m:96
    ## Create output variable
    constFile=copy(raw)
# importconstFile.m:99