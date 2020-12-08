import os
import sys
import re

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press Enter key to exit.")
    sys.exit(-1)

def getEntries(textList):
    """takes a compiled file and returns a list of individual text entries
    """
    lines = textList.splitlines()
    result = []
    entry = ""
    textID = ""
    definition = None
    newEntry = True
    lineIndex = 0
    for line in lines:
        l = line.strip()
        lineIndex += 1
        if newEntry: #new text entry
            if l == "":
                next
            else:
                matchobj = re.match("^#\s*(0x[0-9a-fA-F]+)\s*(\w+)?$",l,re.M|re.I)
                assert matchobj, "Error at line " + str(lineIndex) + ' - "' + l + '":\nEntries must begin with the format "#0xtextID optional_definition"'
                textID = matchobj.group(1)
                definition = matchobj.group(2)
                newEntry = False
                # entry += line
        elif l[-3:] == "[X]": #ends in x
            entry += (line + "\n")
            tmp = (entry, textID, definition)
            result.append(tmp)
            entry = ""
            definition = None
            newEntry = True
        else:
            entry += (line + "\n")
    return result


def assemble(filepath, depth=0):
    if depth > 500:
        print("Warning: #include depth exceeds 500. Check for circular inclusion.\nCurrent file: " + filepath)
        return None
    result = ""
    with open(filepath, 'r') as f:
        lines = f.readlines() #each line is added to the list
    for line in lines:
        matchobj = re.match("^#include\s+(.+)",line.strip(),re.M|re.I)
        if matchobj:
            includee = matchobj.group(1).strip()
            if (includee[0] == '"'):
                includee = includee.strip('"')
            tmp = assemble(includee, depth+1)
            if tmp:
                result += tmp
            else:
                return None
        else:
            result += line
    return result + "\n"

def main():
    sys.excepthook = show_exception_and_exit

    path = sys.argv[1]
    (cwd, inputFile) = os.path.split(path)
    try:
        os.chdir(cwd)
    except Exception:
        pass

    textList = assemble(inputFile)
    if textList:
        defpath = "Text Definitions.event"
        datapath = "Install Text Data.event"

        definitionsheader = """//Definitions generated by TextProcess.exe
#ifndef TEXT_DEFINITIONS
    #define TEXT_DEFINITIONS
#endif


"""
        dataheader = """//Data installer generated by TextProcess.exe

#include "Tools/Tool Helpers.txt"
#include "Text Definitions.event"

"""

        #create the files
        with open(datapath,'w') as f:
            f.write(dataheader)
        with open(defpath,'w') as f:
            f.write(definitionsheader)

        textEntries = getEntries(textList)
        subdirectory = "_textentries"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        for entry in textEntries: #create separate files for each text entry
            content = entry[0]
            textID = entry[1]
            definition = entry[2]
            with open(os.path.join(subdirectory, textID + ".txt"), 'w') as f:
                f.write(content)
            with open(datapath, 'a') as f:
                f.write("TxtData" + textID + ":\n")
                f.write('#incext ParseFile "'+ os.path.join(subdirectory, textID + ".txt") +'"\n')
                f.write("setText(" + textID + "," + "TxtData" + textID +")\n\n")
            if definition:
                with open(defpath, 'a') as f:
                    f.write("#define " + definition + " " + textID + "\n")
        print("...success!\n")
    else:
        print("No data written to output.\n")
    input("Press Enter to continue")

if __name__ == '__main__':
  main()
