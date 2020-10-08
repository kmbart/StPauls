#  E-Giving Analysis - Parse Pledge-Giving Analysis data export to find percentage and dollar totals of E-Givers


#  Read in Pledge-Giving data
#  
#  A valid giver line is <name>,,,<pledge amount>,,<given amount>,,,,
#  Valid amounts may be enclosed in double quotes if > 999.99
#  Lesser amounts may have 0/1/2 digits to the left of the decimal point
#  All amounts have a decimal point and two digits to the right of the decimal
#
#  ValidLine (line, name, pledge amount, given amount) => boolean
#    Parse name
#    Parse pledge amount
#    Parse given amount
#
#  For each line in file
#    If not ValidLine (name,pledge amount, given amount) then continue
#
#    Add to count and total
#    Add E-Givers to E-Giver count and total pledged and total given
#
#  Display totals
#    E-Giver count
#    E-Giver total given
#    E-Giver total pledged
#
#    All givers count
#    All givers total given
#    All givers total pledged
#
#    E-Giver percentage of count
#    E-Giver percentage of total given
#    E-Giver percentage of total pledged


import csv
import re
from dataclasses import dataclass


# reAmts = re.compile(r'("\d,|"\d\d,)?(\d|\d\d|\d\d\d)(.\d\d)(")?,')
# reAmts = re.compile(r"('\d,|'\d\d,)?(\d|\d\d|\d\d\d)(.\d\d)(')?")
reAmts = re.compile(r"('\d,|'\d\d,)?((\d|\d\d|\d\d\d)(.\d\d))+(')?")
reName = re.compile(r'.+')

amtGiven        = 0
amtPledged      = 0
cntAllGivers    = 0
cntEGivers      = 0
cntENotP        = 0
cntLines        = 0
cntPNotE        = 0
cntUnpledged    = 0
donorName       = ''
eGiver          = False
totAllGiven     = 0
totAllPledged   = 0
totEGiven       = 0
totENotPGiven   = 0
totEPledged     = 0
totPNotEGiven   = 0
totPNotEPledged = 0
totUnpledged    = 0

# PGfile = open(r"C:\\Users\keith\OneDrive\Documents\St. Paul's\Pledging\Pledge-Giving Analysis- 20201002.csv")
# lineList = PGfile.readlines()
# PGfile.close()
# print('linelist=', lineList)


@dataclass
class parsedLine:
    lineText: str = ''
    lineName: str = ''
    lineGAmt: float = 0.0
    linePAmt: float = 0.0
    lineEGiver: bool = False
    lineValid: bool = False


def ValidLine (lineList) -> bool:
# If aline has name and pledge amount and given amount

    print('lineList=', lineList)
    invalidLine  = False

    aLine = parsedLine()
    aLine.lineText = lineList

    matchObj = reName.search(lineList[0])
    if matchObj != None: aLine.lineName = matchObj.group(0)
    else:                invalidLine  = True
#    print('name re=', matchObj, ',name=', name)

    matchObj = reAmts.search(lineList[3])
    if matchObj != None: aLine.linePAmt = float(matchObj.group(0).replace(',',''))
    else:                invalidLine  = True
#    print('pamt re=', matchObj, ',pamt=', pamt)

    matchObj = reAmts.search(lineList[5])
    if matchObj != None: aLine.lineGAmt = float(matchObj.group(0).replace(',',''))
    else:                invalidLine  = True
#    print('gamt re=', matchObj, ',gamt=', gamt)

    if lineList[7] == 'X': aLine.lineEGiver = True
#    print('egiver=', egiver)

    aLine.lineValid = not invalidLine

    return (aLine)


with open(r"C:\\Users\keith\OneDrive\Documents\St. Paul's\Pledging\Pledge-Giving Analysis- 20201002 + EFT.csv") as PGfile:
    csvLines = csv.reader(PGfile)

    for line in csvLines:
#    print ('Line:',line [0:len(line) - 1])

        cntLines += 1
#        if cntLines > 15: break
#        print('read line:', cntLines, '=', line)

        currLine = ValidLine (line)
        if not currLine.lineValid: continue
        print ('line=', currLine)

#    If a valid line then add to counts and amounts
        if currLine.lineEGiver:
            cntEGivers  += 1
            totEGiven   += currLine.lineGAmt
            totEPledged += currLine.linePAmt

        if currLine.linePAmt == 0:
            cntUnpledged += 1
            totUnpledged += currLine.lineGAmt

        if currLine.linePAmt == 0 and currLine.lineEGiver:
            cntENotP        += 1
            totENotPGiven   += currLine.lineGAmt

        if currLine.linePAmt != 0 and not currLine.lineEGiver:
            cntPNotE        += 1
            totPNotEGiven   += currLine.lineGAmt
            totPNotEPledged += currLine.linePAmt

        cntAllGivers  += 1
        totAllGiven   += currLine.lineGAmt
        totAllPledged += currLine.linePAmt


#  Show the counts and amounts
print ()
print ()
print ('Number of E-Givers:    ', '{:3d}'.format(cntEGivers))
print ('Given by E-Givers:     ', '${:9,.2f}'.format(totEGiven))
print ('Pledged by E-Givers:   ', '${:9,.2f}'.format(totEPledged))
print ()
print ('Number of Unpledged:   ', '{:3d}'.format(cntUnpledged))
print ('Given by Unpledged:    ', '${:9,.2f}'.format(totUnpledged))
print ()
print ('Number of Pledged not E-Giver:   ', '{:3d}'.format(cntPNotE))
print ('Given by Pledged not E-Giver:    ', '${:9,.2f}'.format(totPNotEGiven))
print ('Pledged by Pledged not E-Giver:  ', '${:9,.2f}'.format(totPNotEPledged))
print ()
print ('Number of Unpledged but E-Giver:   ', '{:3d}'.format(cntENotP))
print ('Given by Unpledged but E-Giver:    ', '${:9,.2f}'.format(totENotPGiven))
print ()
print ('Number of All Givers:  ', '{:3d}'.format(cntAllGivers))
print ('Given by All Givers:   ', '${:9,.2f}'.format(totAllGiven))
print ('Pledged by All Givers: ', '${:9,.2f}'.format(totAllPledged))
print ()
print ('Percentage of E-Givers:         ', '{:>6.2f}'.format(cntEGivers/cntAllGivers * 100))
print ('Percentage Given by E-Givers:   ', '{:>6.2f}'.format(totEGiven/totAllGiven * 100))
print ('Percentage Pledged by E-Givers: ', '{:>6.2f}'.format(totEPledged/totAllPledged * 100))
