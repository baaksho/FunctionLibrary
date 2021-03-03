#Please have ATI installed in your computer
#Add the following line in your program
#folder_name = input('Please enter the folder path: \n')
#For any feedback/questions, please contact: rkhan19@ford.com [Rahat H Khan]
#Thank you!

def AskFileExtension():
    import pdb
    import re
    import glob
    import sys, os
    import datetime
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    from pathlib import Path 
    from win32com.client import Dispatch
    wShell = Dispatch("WScript.Shell")
    #print ("Purpose: This function will ask user for the valid file extension.\n")
    #print ("This function requires the following as input parameter/s.\n")
    #print ("None \n")
    #-------------------------------------------------------------------
    boltrue = True
    while boltrue:
        file_ext_input = input("\nPlease enter your desired file extension........[Sample Format: .rec] : ")
        if file_ext_input == ".rec":
            file_ext = file_ext_input  #or you can set this to '.rec' directly 
            print ("\nScripTech is searching for desired file type with that extension...... \n")
            break
        else:
            print ("____Currently we do not support " + file_ext_input + " format. Please try again____")
    return file_ext


def GenerateSignalLibrary(folder_name, file_ext):
    import pdb
    import re
    import glob
    import sys, os
    import datetime
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    from pathlib import Path 
    from win32com.client import Dispatch
    wShell = Dispatch("WScript.Shell")
    #-------------------------------------------------------------------
    #file_ext = ".rec"
    #AskFileExtension() #----------------|||||||||||||||<><><><><>FUNCTION<><><><><><>|||||||||||||||||
    SigHead = []
    RefSigHead = []

    #folder_name = input('Please enter the folder path: \n')
    #folder_name = "C:\Users\rkhan19\Downloads\Python201\VisionFileReaderScript\shorttest"
    folder = Path(folder_name)
    file_in_folder = folder.iterdir()
    for items in file_in_folder:
        #print (items.suffix)
        if items.suffix == file_ext: #rec type for now
            file_path1 = folder_name + '/' + items.name
            RecFile1 = Dispatch("Vision.RecorderFile") #----------------------THIS MAY FIX same data repeat--------:-|
            RecFile1.OpenRecorderFile(file_path1)
            print(file_path1)
            #GenerateSignalLibrary(file_path1)
    
    

        for i in range(1,len(RecFile1.Channels)):
            Signalname = RecFile1.Channels(i).Name
            #print (Signalname)
            SigHead.append(Signalname)
        SigHead.sort()

        if RefSigHead == []: #make the first one as a reference 
            RefSigHead = SigHead
            #RefSigHead.sort()

        list_diff = []
        if SigHead != RefSigHead:
            for item in SigHead:
                if item not in RefSigHead:
                    list_diff.append(item)
        #print ("Printing the differences only...")
        #print(list_diff)
        RefSigHead = RefSigHead + list_diff
        RefSigHead.sort()

        #print(RefSigHead)
        #import re
        
        #for sig in RefSigHead:
        #    if re.findall(keyentry, sig) != []:
        #        print(sig)
        print("Signal Database is created.\n")
    return RefSigHead


def KeyWordSearchEntryWOR(RefSigHead): #Without Reference - Quicker!
    import pdb
    import re
    import glob
    import sys, os
    import datetime
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    from pathlib import Path 
    from win32com.client import Dispatch
    wShell = Dispatch("WScript.Shell")
    #-------------------------------------------------------------------
    while True:
        try:
            usersigcount = input("\nPlease enter the ----<<< Number >>>---- of the signals you want to analyze [100 max] : ")
            usersigcnt = int(usersigcount)    
            if type(usersigcnt) == int:
                if usersigcnt < 100 and usersigcnt > 0:
                    sigcnt = usersigcnt
                    #return print("Valid input entered : " + str(sigcnt))
                    break
            #return print("Valid input entered : " + str(sigcnt))
        except ValueError:
            print("Please enter only a valid positive integer and try again. ")
            continue
            
    #----------------------------------Signal count ends
    cnt = 0
    usersiglist = []
    while cnt < sigcnt:
        keyentry = input("Please enter a _____[[[[[__Keyword__]]]]]_____ to search related signals: \n")
        for sig in RefSigHead:
            if re.findall(keyentry, sig) != []:
                print(sig)
        userinput = input("\nPlease enter/copy-paste your a Signal name from the list [or type '0' (zero) to skip]: \n")
        
        if userinput.strip() == '0'or userinput.strip() == 'o':
            cnt = cnt + 1
            print("Signal entry skipped! \n")
        else:
            usersiglist.append(userinput.strip())
                    
            cnt = cnt + 1
            cntstr = str(cnt)
            leftover = sigcnt - cnt
            leftoverstr = str(leftover)
            print("Signal left to entry : " + leftoverstr)
            
    return usersiglist




        
def ATISignalFinder(usersiglist, folder_name, file_ext): #usersiglist, folder, file_ext,.... SigHead
    import pdb
    import re
    import glob
    import sys, os
    import datetime
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    from pathlib import Path 
    from win32com.client import Dispatch
    wShell = Dispatch("WScript.Shell")
    print("Please make sure ATI Vision is installed on your system.")
    #------------------------------------------------------------------------------ 
    
    #folder_name = input('Welcome to ScripTech! This tool will gather info. from you and generate desired analysis. Please enter the folder path: \n')
    folder = Path(folder_name)
    
    #file_ext = '.rec'
    #usersiglist = ['htipm_b_ntm_fail', 'htipm_b_prk_fail', 'EPRK_DC_LIN_SENS1']
    #folder
    allfiles = folder_name + '/' + 'Overalldata.txt'
    summaryfile = folder_name + '/' + 'OverallSummary.txt'
    #Open the text file for writing
    allfile = open(allfiles, 'w')   
    sumfile = open(summaryfile, 'w')
    cnt = 0
    file_count = 0
    userInput = 0
    max_file_size = 0
    index = []
    RecList = []
    RecListall = []
    DepthCh = []
    #usersiglist = []
    txtfilelist = []
    
    files_in_folder = folder.iterdir()
    for item in files_in_folder:
        if len(usersiglist) == 0:
            print("Your entry is null.")
            break
        if item.is_file():

            if item.suffix == file_ext:
                file_count = file_count + 1
                file_name = item.name
                file_path = folder_name + '/' + item.name
                file_core = os.path.splitext(item.name)[0]
                file_corestr = str(file_core)

                print ("\nCurrently Viewing the following .rec file........ ")
                sumfile.write("\nCurrently Viewing the following .rec file........ \n")
                print (str(file_corestr) + ".rec ") #------------------------------> Success
                sumfile.write(str(file_corestr) + ".rec ")
                                  
                file_size_Bytes = os.path.getsize(file_path)
                filesizeKB = file_size_Bytes/1000.0
                filesizeMB = filesizeKB/1000.
                
                print ("File Size is : " + str(filesizeKB) + " KB") # or " + str(filesizeMB) + " MB." )
                sumfile.write("File Size is : " + str(filesizeKB) + " KB or " + str(filesizeMB) + " MB.\n" )
                #RecFile = 0
                RecFile = Dispatch("Vision.RecorderFile") #----------------------THIS MAY FIX same data repeat--------:-|
                RecFile.OpenRecorderFile(file_path)
                #LenRecData = len(RecFile.Channels(1).GetData2()) #------------------------May remove this-----------:(

                txtfile = folder_name + '/'+ file_corestr +'.'+'txt'
                file = open(txtfile, 'w') #----------------------------------------SECOND file got stuck here
                #file.write(str(usersiglist) + "\n") #from user inputs
                
                txtfilelist.append(txtfile)
                
                SigLength = len(RecFile.Channels)
                totsigcnt = len(RecFile.Channels)
                print ("Total number of signals in this file is : " + str(totsigcnt))
                sumfile.write("File Size is : " + str(filesizeKB) + " KB or " + str(filesizeMB) + " MB. \n")

                recdatalist = []  
                #z = ((0,0))
                z = [(0,0)]

                index.clear()
                for userinp in usersiglist: #inputs saved in a string
                    for i in range (1, len(RecFile.Channels)): #looping through all the channels
                        recsig = str(RecFile.Channels(i).Name).strip()
                        usersig = userinp.strip()
                        #usersig = userinp
                        if recsig == usersig: #---------------------------------------signal found
                            #print (recsig)
                            print ("Signal: " + str(recsig) + " exists and the signal number is : " + str(i))
                            sumfile.write("Signal: " + str(recsig) + " exists and the signal number is : " + str(i) +"\n")
                            #print (i)
                            index.append(i) #let's say 95th signal is that 

                sDatatest2 =""
                #tStamp = ""
                num1 = 0
                num2 = 0
                #print ("Data appended to the list")
                print ("Index to the signals are :" + str(index))
                sumfile.write("Index to the signals are :" + str(index) + "\n")
                if len(index) == 0:
                    print("OOPS! Your requested signal(s) couldn't be found in this file! Sorry!! :(")
                    sumfile.write("OOPS! Your requested signal(s) couldn't be found in this file! Sorry!! :( \n")
                #for i in index: #2, 4
                    #RecCh[i] = RecFile.Channels(index[i]).GetData2()
                    #sDatatest2 = sDatatest2 + RecCh[i]
                #dt1 = 0 
                #dt2 = 0
                maxlenindex = 0
                DepthCh.clear()
                nom = 0
                for i in index: #lets say 5 channels

                    RecList.clear()
                    chlen = len(RecFile.Channels(i).GetData2())

                    #file.write("======================================================================================\n" + str(usersiglist[nom]) + "\t" + "Time" + "\n" + "\n")
                    #allfile.write("======================================================================================\n" + str(usersiglist[nom]) + "\t" + "Time"  + "\t From file : " + file_corestr + ".txt" + "\n" + "\n")
                    file.write(str(usersiglist[nom]) + "\t" + "Time" + "\n")
                    allfile.write(str(usersiglist[nom]) + "\t" + "Time"  + "\t From file : " + file_corestr + ".txt" + "\n")
                    
                    #file.write(str(usersiglist[nom]) + "\n" + "\n") #from user inputs
                    #allfile.write(str(usersiglist[nom]) + "\n" + "\n") #from user inputs

                    #print (str(usersiglist[nom]))
                    nom = nom + 1
                    for d in range(0, chlen):

                        RecCh = RecFile.Channels(i).GetData2()
                        sData = str(RecCh[d]) #-----------------------------------------with time stamp
                        #sData = [j[0] for j in sData0]
                        #sData = (' '.join(sData0))
                        #sData = str(RecCh[d][0]) #---------------------------------------without time stamp
                        file.write(sData + "\n")
                        allfile.write(sData + "\n")

                #plotq = input("Would you like to plot the signals ? Please respond 'y' for Yes and 'n' for No. ")
                #-----------------------------------------------------type the request
                #df = pd.read_csv(txtfile, sep='\t')
                #df.plot()

                #imagefilename = folder_name + '/'+ file_corestr +'.'+'png'
                #plt.savefig(imagefilename, dpi = 500)
                #file.close()        


            #Close the file
                print ("Conversion, analysis, etc... completed.\n")
                print ("Total files analyzed: " + str(file_count))
                sumfile.write("Conversion, analysis, etc... completed.\n\n")                      
                
                file.close()
    allfile.close()
    #ConclusionTruckImg(usersiglist, file_count)
    sumfile.close()
    return txtfilelist


def BasicSignalPlotter(txtfilelist, folder_name): #RefSigHead, folder_name
    import pdb
    import re
    import glob
    import sys, os
    import datetime
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    import matplotlib
    import matplotlib.pyplot as plt
    import csv
    from pathlib import Path 
    from win32com.client import Dispatch
    # if using a Jupyter notebook, include:
    %matplotlib inline
    wShell = Dispatch("WScript.Shell")
    
    #print ("Purpose: This function will ask user for the valid folder location.\n")
    #print ("This function requires the following as input parameter/s.\n")
    #print ("None \n")
    #-------------------------------------------------------------------
    timestr = 'Time'
    x = []
    y = []
    plotlabel = ''
    imagefilename = ''
    imgfilecnt = 0
    plotlabellist = []
    imagefilelist = []
    #folder_name = input('Please enter the folder path for plotting: \n')
    #os.chdir(folder_name)
    folder = Path(folder_name)
    file_txt = '.txt'
    imagefilelist = []
    txtfile_count = 0
    files_in_folder = folder.iterdir()
    for item in files_in_folder:
        if item.is_file():
            if item.suffix == file_txt: #check for txt file or csv
                txtfile_count = txtfile_count + 1
                file_name = item.name
                #print(file_name) #-------------------------------------------------use this 
                file_path = folder_name + '/' + item.name
                file_core = os.path.splitext(item.name)[0]
                file_corestr = str(file_core)
                txtfilename = folder_name + '/'+ file_corestr +'.'+'txt'
                for filez in txtfilelist:
                    if filez == txtfilename:
                        imgfilecnt = imgfilecnt + 1                        
                        imagefilename = folder_name + '/'+ file_corestr +'.'+'png'
                        pngfile = file_corestr +'.'+'png'
                        imagefilelist.append(imagefilename)
                        x.clear()
                        y.clear()
                        plotlabel = ''
                        with open(file_name,'r') as csvfile:
                            plots = csv.reader(csvfile, delimiter=',')
                            #next(plots)
                            for row in plots:
                                if any('Time' in s for s in row) or any('=' in s for s in row):
                                    print(row)
                                    plotlabel = plotlabel + str(row)
                                    #plotlabel = row
                                    plotlabellist.append(row)
                                    #a = x
                                    #b = y
                                    #x.clear()
                                    #y.clear()
                                else:
                                    y.append((row[0]))
                                    x.append((row[1]))


                        plt.plot(x,y)

                        plt.xlabel('x values')
                        plt.ylabel('y values')
                        plt.title(plotlabel)
                        plt.legend(['line 1'])


                        # save the figure
                        plt.savefig(pngfile, dpi=300, bbox_inches='tight')


                        plt.show()
                        #-----------------------------------
                        
                        #plt.plot(x,y, label= plotlabel)
                        #plt.plot(x,y, label= plotlabellist)
                        #plt.xlabel('x')
                        #plt.ylabel('y')
                        #plt.title(plotlabel)
                        #plt.legend()

                        #plt.grid()
                        #plt.show()
                        #fig.savefig("test.png")  
                        #plt.savefig("test1.png", dpi = 500)
                        #-------------------------------------
                        #fig.savefig(imagefilename)  
                        #fig.savefig(file + plotlabel + '.png')

                        #plt.savefig(imagefilename)
                        #plt.savefig(pngfile, dpi = 500)
                        #plt.close()
                        
                        
    print("Total plot files:" + str(imgfilecnt))
    return imagefilelist


def BasicSignalPlotterWOFileList(): #Assumes all the txt file is data file in the folder, remove anyother txt files
    import pdb
    import re
    import glob
    import sys, os
    import datetime
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    import matplotlib
    import matplotlib.pyplot as plt
    import csv
    from pathlib import Path 
    from win32com.client import Dispatch
    # if using a Jupyter notebook, include:
    %matplotlib inline
    wShell = Dispatch("WScript.Shell")
    
    #print ("Purpose: This function will ask user for the valid folder location.\n")
    #print ("This function requires the following as input parameter/s.\n")
    #print ("None \n")
    #-------------------------------------------------------------------
    timestr = 'Time'
    x = []
    y = []
    plotlabel = ''
    imagefilename = ''
    imgfilecnt = 0
    plotlabellist = []
    imagefilelist = []
    folder_name = input('Please enter the folder path for plotting: \n')
    #os.chdir(folder_name)
    folder = Path(folder_name)
    file_txt = '.txt'
    imagefilelist = []
    txtfile_count = 0
    files_in_folder = folder.iterdir()
    for item in files_in_folder:
        if item.is_file():
            if item.suffix == file_txt: #check for txt file or csv
                txtfile_count = txtfile_count + 1
                file_name = item.name
                #print(file_name) #-------------------------------------------------use this 
                file_path = folder_name + '/' + item.name
                file_core = os.path.splitext(item.name)[0]
                file_corestr = str(file_core)
                txtfilename = folder_name + '/'+ file_corestr +'.'+'txt'
                
                imgfilecnt = imgfilecnt + 1                        
                imagefilename = folder_name + '/'+ file_corestr +'.'+'png'
                pngfile = file_corestr +'.'+'png'
                imagefilelist.append(imagefilename)
                x.clear()
                y.clear()
                plotlabel = ''
                with open(file_name,'r') as csvfile:
                    plots = csv.reader(csvfile, delimiter=',')
                    #next(plots)
                    for row in plots:
                        if any('Time' in s for s in row) or any('=' in s for s in row):
                            print(row)
                            plotlabel = plotlabel + str(row)
                            #plotlabel = row
                            plotlabellist.append(row)
                            #a = x
                            #b = y
                            #x.clear()
                            #y.clear()
                        else:
                            y.append((row[0]))
                            x.append((row[1]))


                plt.plot(x,y)

                plt.xlabel('x values')
                plt.ylabel('y values')
                plt.title(plotlabel)
                plt.legend(['line 1'])


                # save the figure
                plt.savefig(pngfile, dpi=300, bbox_inches='tight')


                plt.show()
                #-----------------------------------

                       
                        
    print("Total plot files:" + str(txtfile_count))
    return imagefilelist


