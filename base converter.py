from tkinter import Tk, ttk, Entry, Button, StringVar

ERRORMSG = 'invalid arguements'

# function convert takes a number as a string in any base 
# from 2 to 16 and converts it to any other of those bases
def convert(original: str, srcBase: int, tgtBase: int) -> str:

    if not validateBases(srcBase, tgtBase, 2, 16):
        return ERRORMSG

    # ensure that the original string can be the source base, 
    # ie '123.45' cannot be a base lower than 6
    if not validateOriginal(original, srcBase):
        return ERRORMSG

    if srcBase == tgtBase:
        return original

    target = ''

    # if original string is fractional, split it up to deal with 
    # the parts before and after the decimal point separately;
    # convert to base 10, and then to target base
    if '.' in original:
        split = original.split('.')
        beforeDecimal = split[0]
        afterDecimal = split[1]
        baseTen = getBaseTen(beforeDecimal, srcBase, True) + \
            getBaseTen(afterDecimal, srcBase, False)

        split = str(baseTen).split('.')
        beforeDecimal = int(split[0])
        for ix in range(5): # 5 decimal places
            afterDecimal = int(split[1]) / (10 ** len(split[1]))
            # round because of Python's weird thing with long numbers
            baseTen = round((afterDecimal * tgtBase), 5)
            split = str(baseTen).split('.')
            target += split[0]
        target = getTarget(beforeDecimal, tgtBase) + '.' + target

    else:
        baseTen = getBaseTen(original, srcBase, True)
        target = getTarget(baseTen, tgtBase)

    return target

def validateBases(srcBase: int, tgtBase: int, lower: int, upper: int) -> bool:
    return (type(srcBase) == int and type(tgtBase) == int) and\
            (srcBase >= lower and srcBase <= upper) and\
            (tgtBase >= lower and tgtBase <= upper)
        

def validateOriginal(original: str, srcBase: int) -> bool:
    numPeriods = 0
    for digit in original:
        if digit == '.':
            numPeriods += 1
            if numPeriods > 1:
                return False
        elif srcBase < 11 and digit in ['a', 'b', 'c', 'd', 'e', 'f']:
            return False
        else:
            try:
                intDigit = int(digit)
                if intDigit >= srcBase:
                    return False
            except ValueError:
                if digit == '.' or (srcBase == 11 and digit == 'a') or\
                (srcBase == 12 and digit in ['a', 'b']) or\
                (srcBase == 13 and digit in ['a', 'b', 'c']) or\
                (srcBase == 14 and digit in ['a', 'b', 'c', 'd']) or\
                (srcBase == 15 and digit in ['a', 'b', 'c', 'd', 'e']) or\
                (srcBase == 16 and digit in ['a', 'b', 'c', 'd', 'e', 'f']):
                    pass
                else:
                    return False
    return True

def getBaseTen(original: str, srcBase: int, beforeDecimal: bool) -> int:
    if beforeDecimal:
        exponent = len(original)
    else:
        exponent = 0
    baseTen = 0
    for digit in original:
        values = {'a':10, 'b':11, 'c':12, 'd':13, 'e':14, 'f':15}
        if digit in values:
            value = values[digit]
        else:
            value = int(digit)
        exponent -= 1
        baseTen += value * (srcBase ** exponent)
    return baseTen

def getTarget(baseTen, tgtBase):
    if tgtBase == 10:
        return str(baseTen)
    else:
        remainders = []
        while baseTen > 0:
            remainders.append(baseTen % tgtBase)
            baseTen //= tgtBase

        target = ''
        for remainder in reversed(remainders):
            values = {10:'a', 11:'b', 12:'c', 13:'d', 14:'e', 15:'f'}
            if remainder in values:
                target += values[remainder]
            else:
                target += str(remainder)
        return target

def testConvert():
    print('Testing Convert Function...')
    # testing with base 10
    assert(convert('101', 2, 10) == '5')
    assert(convert('1000', 3, 10) == '27')
    assert(convert('87', 10, 2) == '1010111')
    assert(convert('35', 10, 16) == '23')
    # other bases below 10
    assert(convert('0', 3, 3) == '0')
    assert(convert('32', 4, 9) == '15')
    assert(convert('77', 8, 6) == '143')
    assert(convert('11', 2, 13) == '3')
    # bases above 10
    assert(convert('1785', 15, 13) == '2405')
    assert(convert('17a', 11, 16) == 'd0')
    assert(convert('13f4b', 16, 8) == '237513')
    assert(convert('299', 14, 12) == '37b')
    assert(convert('444', 5, 12) == 'a4')
    # different errors
    assert(convert('101', 0, 10) == ERRORMSG)
    assert(convert('101', 2, 0) == ERRORMSG)
    assert(convert('120', 2, 10) == ERRORMSG)
    assert(convert('101', 2, 17) == ERRORMSG)
    assert(convert('101', 2, 7.5) == ERRORMSG)
    assert(convert('101', 2.2, 10) == ERRORMSG)
    assert(convert('32b', 11, 3) == ERRORMSG)
    assert(convert('ab4f2', 15, 16) == ERRORMSG)
    assert(convert('hello world', 4, 4) == ERRORMSG)
    assert(convert('2.2.2', 10, 9) == ERRORMSG)
    # fractional numbers
    assert(convert('123.45', 10, 16) == '7b.73333')
    assert(convert('2.3', 4, 10) == '2.75000')
    assert(convert('20.4', 10, 6) == '32.22222')
    assert(convert('44.32', 5, 9) == '26.61064')
    assert(convert('587.33', 9, 2) == '111100100.01011')
    assert(convert('6.a', 11, 10) == '6.90909')
    assert(convert('5b.e3', 15, 7) == '152.64246')
    assert(convert('f.a1', 16, 3) == '120.12122')
    assert(convert('0.97', 12, 5) == '.34440')

    print('Yay!!! Passed test!')

def run(): #(non gui)
    cont = 'y'
    while cont.lower() == 'y' or cont.lower() == 'yes':
        original = input('\nWhat number would you like to convert? ')
        srcBase = input('What base is your number? ')
        tgtBase = input('What bases would you like to convert to? ')
        try:
            srcBase = int(srcBase)
            tgtBase = int(tgtBase)
            converted = convert(original, srcBase, tgtBase)
        except ValueError:
            converted = ERRORMSG
        if converted == ERRORMSG:
            print('Sorry, your numbers and/or bases are invalid.')
        else:
            print(original, 'in base', srcBase, 'is', 
                    converted, 'in base', tgtBase)
        cont = input('Do you want to convert another number? ')


def gui():
    root = Tk()
    root.title('Base Converter')
    width = 400
    height = 250
    font1 ='Calibri 12'
    font2 = 'Calibri 14'
    backgroundColor = 'azure2'
    borderColor = 'gray50'
    root.geometry(str(width) + 'x' + str(height))
    root.configure(bg = backgroundColor, highlightbackground = borderColor,\
        highlightthickness = 2, relief = 'sunken', borderwidth = 2)
        
    srcBase = ttk.Combobox(root, width = 5, font = font1)
    srcBase.place(relx = (0.6), rely = (0.2))
    srcBase['values'] = list(range(2,17))
    srcBase.state(['readonly'])
    srcBaseStr = StringVar()
    srcBase['textvariable'] = srcBaseStr

    tgtBase = ttk.Combobox(root, width = 5, font = font1)
    tgtBase.place(relx = (0.6), rely = (0.45))
    tgtBase['values'] = list(range(2,17))
    tgtBase.state(['readonly'])
    tgtBaseStr = StringVar()
    tgtBase['textvariable'] = tgtBaseStr

    entry = Entry(root, width = 12, font = font2, justify = 'center')
    entry.place(relx = (0.2), rely = (0.2))
    entryStr = StringVar()
    entry['textvariable'] = entryStr

    answer = Entry(root, width = 12, font = font2, justify = 'center')
    answer.place(relx = (0.2), rely = (0.45))
    answerStr = StringVar()
    answer['textvariable'] = answerStr
    
    def doConvert():
        if srcBase.get() != '' and tgtBase.get() != '':
            target = convert(entry.get(),\
            int(srcBase.get()), int(tgtBase.get()))
            if target == ERRORMSG:
                answerStr.set('invalid')
            else:
                answerStr.set(target)

    convertBtn = Button(root, text = 'convert', default = 'active',\
                command = doConvert, font = font1)
    convertBtn.place(relx = (0.6), rely = (0.7))
    root.bind('<Return>', lambda event: doConvert()) # enter converts input

    def clear():
        entryStr.set('')
        srcBaseStr.set('')
        tgtBaseStr.set('')
        answerStr.set('')

    clearBtn = Button(root, text = 'clear', default = 'active',\
                command = clear, font = font1)
    clearBtn.place(relx = (0.3), rely = (0.7))
    root.bind('<Delete>', lambda event: clear()) # delete clears all

    root.bind('<Escape>', lambda event: root.destroy()) # escape closes window

    root.mainloop()


if __name__ == '__main__':
    # testConvert()
    # run()
    gui()