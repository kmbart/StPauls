#GiverCount:
#  Parse Givers List for count of distinct givers and bucket by frequency and amount.
#
#  Read in Givers List data
#  
#  For each line in file
#    If line is "Giver:"
#      get giverNumber
#      get TotalAmount with or without ""
#    If giverNumber is different
#        BreakOnGiver (reset counts and amounts; put in buckets)
#        add 1 to giverCount
#      Else
#        add totalAmount to giverAmount
#    Else  # not "Giver:"
#      If line has date
#        add 1 to giftCount
#    
#  Print giverCount
#  Print cnoteCount = giftAmount > $100
#  Print dozenCount = giftCount > 12
#


import re

reAmt       = re.compile(r'(Total:..)(\d|\d\d|\d\d\d)\.(\d\d)')
reAmtQuoted = re.compile(r'(Total:..")(\d|\d\d),(\d\d\d)\.(\d\d)(")')
reDate      = re.compile(r'(\d\d)/(\d\d)/(\d\d\d\d)')
reGiverNum  = re.compile(r'\d{1,4}')

amtGiver               = 0
amtTotal               = 0
cntGivers              = 0
cntGifts               = 0
cntLines               = 0
cntNonGivers           = 0
cntOverDollarThreshold = 0
cntOverGiftThreshold   = 0
cntOverThreshold       = 0
giverNumber            = 0
oldNumber              = 0

dollarThreshold        = 30000
giftThreshold          = 99
lineLimit              = 9999

GiverFile = open(r"C:\\Users\keith\OneDrive\Documents\St. Paul's\Finance\Givers FY2019.txt")
linelist = GiverFile.readlines()
GiverFile.close()

# for each line in file
for line in linelist:
    strippedLine = line.strip()
    if strippedLine == '':
        continue

    cntLines += 1
    if cntLines > lineLimit: break
    
    if strippedLine [0:7] == 'Giver: ':
#        print ('Giver=',strippedLine [0:55])

# get giverNumber
        giverNumber = (strippedLine[7:].split('-')[0]).strip()
#        print ('#=',giverNumber)
        if not giverNumber.isnumeric():
            cntNonGivers += 1
#            print ('NonGiver=',giverNumber)
            continue
        
        if int(giverNumber) > 999:
            continue

# get Total amount
        moAmt = reAmt.search(strippedLine)
        if moAmt != None:
            amtGiver = int(moAmt.group(2)) + (int(moAmt.group(3)) / 100)
#            print ('Found amt=', amtGiver, 'for giver:', giverNumber)
        else:
            moAmt = reAmtQuoted.search(strippedLine)
            if moAmt != None:
                amtGiver = int(moAmt.group(2)) * 1000 + int(moAmt.group(3)) + (int(moAmt.group(4)) / 100)
#                print ('Found amtQ=', amtGiver, 'for giver:', giverNumber)
                

# if giverNumber is different break on Giver
        if giverNumber != oldNumber:
            cntGivers  += 1
            
#            print ('Checking amt=', amtTotal, 'for giver:', oldNumber)
            if amtTotal >= dollarThreshold:
                cntOverDollarThreshold += 1
#                print('Giver#', giverNumber, '> $', dollarThreshold, ' = ', amtTotal)
            else:
                if cntGifts >= giftThreshold:
                    print('Giver#', giverNumber, '< $', dollarThreshold, ' but more than', giftThreshold, 'gifts')
            
            if cntGifts >= giftThreshold:
                cntOverGiftThreshold += 1
                
            if (amtTotal >= dollarThreshold
            or cntGifts >= giftThreshold):
                cntOverThreshold += 1
                
            oldNumber = giverNumber
            amtTotal  = amtGiver
            cntGifts  = 0
            
        else:
            amtTotal = amtTotal + amtGiver

    else:  # Non-Giver

        moDate = reDate.search(strippedLine)
# if line has date
        if moDate != None:
#            print ('Found date=',moDate.group())
#            print ('  MM  =',moDate.group(1))
#            print ('  DD  =',moDate.group(2))
#            print ('  CCYY=',moDate.group(3))
            cntGifts += 1

# show counts and amounts
print ()
print ('Number of Lines:        ', cntLines)
print ('Number of Givers:       ', cntGivers)
print ('Number of NonGivers:    ', cntNonGivers)
print ('Count of Over $', dollarThreshold,': ', cntOverDollarThreshold)
print ('Count of Over ', giftThreshold, 'gifts: ',cntOverGiftThreshold)
print ('Count of Over Either Threshold: ', cntOverThreshold)
print ()
