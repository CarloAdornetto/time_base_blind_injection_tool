TIME BASE BLIND ATTACK TOOL

This tool has been developed to make the "Time Base Blind Injection" attack on sites where the following information are known:
-	Request URL;
-	An existing value in the site Database end the field name that value is referred to;

The execution starts from command line launching a python3 script (“main.py” file contains the main execution flow).

Input values:
-	Request URL without the hypothetical explicit request;
-	The field name of the known value;
-	The known value;
-	The request method (POST/GET);

Output values:
-	Database information chosen by the user during the execution;

Other developed features:
-	Optimized sleep time;
-	Three possible payload formats;
-	User has the possibility to repair character mistakes/missing before every step of the attack;
-	User can decide to see all attack payloads;
-	This tool works using a number of (parallel identical) requests. 
	This number can be changed (in the file my_request.py line 6) setting the variable “number_of_threads”. 
	This feature has been developed to guarantee results robustness;

