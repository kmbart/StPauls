#PledgeCompare:
#  Parse Pledge-Giving data export; reformat to put name+pledge+giving on single line;
#    count ahead/behind/on target units on a pro-rated basis.
#
#  Read in Pledge-Giving data
#  
#  For each line in file
#    If line is Break row (eleven commas)
#      If name not blank
#        diff = giving - (pledge * pro-rating percentage)
#        If diff < 0
#          add 1 to ahead count
#          add diff to ahead amount
#        Elif diff > 0
#          add 1 to behind count
#          add diff to behind amount
#        Else
#          add 1 to ontarget count
#
#        print giving unit #, name, pledge amount, giving amount, percentage
#
#        reset giving unit #, name, pledge amount, giving amount, percentage
#
#    If line is Giver row (giving unit # and name)
#      store giving unit # and name
#
#    If line is Account row (one comma, an account (three-digit number + space + hyphen + title, <empty>, amount-per-period,
#                            frequency, annualized-pledge amount, given-to-date amount, prior-giving amount, given+prior amount,
#                            <empty>, over-under amount, percentage given)
#      sum pledge amount, giving amount
#
#    If line is Totals row (five commas and four double-quoted amounts)
#      skip line
#    
#  Print ahead/on target/behind counts and amounts


import re

reAcct = re.compile(r'^\,\d\d\d - ')
reAmts = re.compile(r'("\d,|"\d\d,)?(\d|\d\d|\d\d\d)(.\d\d)(")?,')
reUnit = re.compile(r'^\"?(\d|\d\d|\d\d\d)( - )(.*)')

amtAhead     = 0
amtBehind    = 0
amtTarget    = 0
cntAhead     = 0
cntBehind    = 0
cntGivers    = 0
cntLines     = 0
cntPledgers  = 0
cntTarget    = 0
cntUnpledged = 0
isPledger    = False
sumGiven     = 0
sumPledged   = 0
totGiven     = 0
totPledged   = 0
totUnpledged = 0
unitName     = ''
unitNumber   = ''

PGfile = open(r"C:\\Users\keith\OneDrive\Documents\St. Paul's\Pledging\Pledges2019.txt")
linelist = PGfile.readlines()
PGfile.close()

for line in linelist:
#    print ('Line:',line [0:len(line) - 1])

    cntLines += 1
#    if cntLines > 55: break
    
#    If line is Break row (eleven commas)
    if line [0:11] == ',,,,,,,,,,,':
        if unitName != '':
            
            cntGivers += 1
            if isPledger:
#                print (unitName)
                cntPledgers += 1
                diff = sumGiven - (sumPledged * 32/52)   #2019-09-09
                
                totGiven   += sumGiven
                totPledged += sumPledged

                if diff > 0:
                    cntAhead += 1
                    amtAhead += diff
                elif diff < 0:
                    cntBehind += 1
                    amtBehind += diff
                else:
                    cntTarget += 1

                print (unitName,'(',unitNumber,'), Pledged:',sumPledged,',Given:',sumGiven)

            else:       # not a Pledger
                cntUnpledged += 1
                totUnpledged += sumGiven

                print (unitName,'(',unitNumber,'), Unpledged:', sumGiven)

            isPledger  = False
            sumGiven   = 0
            sumPledged = 0
            unitName   = ''
            unitNumber = ''

#    If line is Giver row (giving unit #, hyphen, and name)
#      SPLIT the line and check the first elt for <up to 3 digits> - <name>
#      store the unit # and name

    elt0 = line.split(',')[0]
    moUnit = reUnit.search(elt0)
    if moUnit != None:
#        print ('Giver row:',moUnit.group(1),moUnit.group(2),moUnit.group(3))
        unitNumber = int(moUnit.group(1))
        unitName   = moUnit.group(3)
    
#    If no giving unit as yet, skip the rest of the parsing

    if unitNumber == '':
#        print ('skipping line:',line [0:22])
        continue

    
#    If line is Account row (one comma, an account (three-digit number + space + hyphen + title, <empty>, amount-per-period,
#                            frequency, annualized-pledge amount, given-to-date amount, prior-giving amount, given+prior amount,
#                            <empty>, over-under amount, percentage given)
#      split line into various amounts
#      add to pledged count and/or given count
#      sum pledged amount, given amount

    moAcct = reAcct.search(line)
    if moAcct != None:
#        print ('found acct', moAcct.group())

        moAmts = reAmts.findall(line)
        if moAmts != []:
            lenTuple = len(moAmts)
#            print ('len of tuple:',lenTuple)
            for tupleIx in range (lenTuple):
                amtTuple = moAmts [tupleIx]
                if amtTuple [0] == '':
                    num1 = ''
                else:
                    num1 = amtTuple [0].lstrip('"')
                    num1 = num1.rstrip(',')
                numFull = float(num1 + amtTuple [1] + amtTuple [2])
#                print ('numFull=', numFull)
                if lenTuple > 2:
                    if tupleIx == 1:
                        isPledger  = True
                        sumPledged += numFull
                    elif tupleIx == 4:
                        sumGiven += numFull
                elif lenTuple == 2:
                    if tupleIx == 1:
                        sumGiven += numFull
#                print ('pledged=', sumPledged,',given=',sumGiven)
                
#   If any other row (including total amounts line = five commas, four amounts) then skip

#  Show the counts and amounts
print ()
print ()
print ('Number of Givers:    ',cntGivers)
print ('Number of Pledgers:  ',cntPledgers)
print ('Number of Unpledged: ',cntUnpledged)
print ()
print ('Count Ahead:         ',cntAhead,', Amount Ahead: ',amtAhead)
print ('Count Behind:        ',cntBehind,', Amount Behind:',amtBehind)
print ('Count on Target:     ',cntTarget,', Amount Target:',amtTarget)
print ()
diff = amtAhead + amtBehind
print ('Net of Pledges:      ',diff)
print ('Pledged Amount:      ',totPledged)
print ('Pledged Given Amount:',totGiven)
print ('Unpledged Amount:    ',totUnpledged)
