Since Transaction_Master is compulsory for running MIA:

Store scripts outside Training and Scoring folder (cml, mapping, utils and connection) at one location. Run connection.R before running anything

For Training Folder

	Check: If Event Table is present --> Run code in Event Folder
		Check: If Customer Table is also present --> Run code in Customer Folder inside the Event Folder
	Else: Run code in Trans Folder
		Check: If Customer Table is also present --> Run code in Customer Folder inside the Trans Folder

Whatever logic works for Training, will be followed for Scoring Folder also

Note:

1. High_Convertors_Primary and High_Convertors_Secondary should always run back to back for code to work properly
2. Scoring code should only start after Training code is over
3. Scoring codes will store data into 4 different tables (assuming Customer table is also present). These tables will have to be combined to give Master View