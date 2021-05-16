******************************
CS3510 TSP Project Readme File
******************************

Contributers: Tucker von Holter, Tim Slanschek
Emails: tmvh3@gatech.edu, t.slanschek@gatech.edu
Date of submission: 04/17/2020

Files submitted:
 - readme.txt       Readme file
 - tsp-3510.py    Python code, contains all code of the project.
 - output.txt       Output file of the run of mat-test.txt
 - algorithm.pdf    Pdf file describing how our algorithm works
 - Tests folder     Folder with all the tests to run, also contains the original mat-test.txt that was provided

 How to run the program:
 A sample command to run the algorithm could look like this
python tsp-3510.py c:/CS3510-TSP/Tests/mat-test.txt c:/CS3510-TSP/output.txt 180

Please make sure to specify the full path and the correct file name, otherwise the input file might not be found 
or the output stored somewhere unpredictable.

Known limitations and bugs:
We do not currently know the limitations of our code, neither in the number of nodes nor in the maximum time it can run until something
unexpected might happen. 
Sadly, with the algorithm we've chosen to implement, the number of nodes plays a large impact on time required to run. 1000 nodes takes
a lot longer than expected (although still within polynomial time).

Average over 10 values: 27639.5
