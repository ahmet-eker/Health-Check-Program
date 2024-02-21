def reading_the_input_file():
	global inputs
	with open("doctors_aid_inputs.txt","r") as file:
		inputs = file.read().split("\n")  #spliting line by line


def is_patient_exist(name):
	for index in range(len(all_patients_list)):
		if name in all_patients_list[index]: #searching the all_patients_list
			return True                      #returning true if patient exist and
	return False                             #otherwise returning false


def create_patient(input_line):
	informations = input_line.split(" ",1)[1]  #getting rid of command "create"
	informations_list = [i.strip() for i in informations.split(",")] 
	informations_list[1] = "{:.2f}%".format(float(informations_list[1])*100)  #adding "%"
	informations_list[5] = "{}%".format(int(float(informations_list[5])*100))
	if not is_patient_exist(informations_list[0]):
		all_patients_list.append(informations_list) #addinf patient to the list
		saving_to_the_output_file("Patient {} is recorded.".format(informations_list[0]))  #saving outputs
	else:
		saving_to_the_output_file("Patient {} cannot be recorded due to duplication.".format(informations_list[0]))


def remove_patient(input_line):
	for t,patient in enumerate(all_patients_list): #t is for finding the patients index
		if patient[0] == input_line.split(" ")[1].strip(): #checking patients name
			all_patients_list.pop(t)
			saving_to_the_output_file("Patient {} is removed.".format(input_line.split(" ")[1]))  #saving outputs
			return 0
	saving_to_the_output_file("Patient {} cannot be removed due to absence.".format(input_line.split(" ")[1]))


def printing_list():
	first_line = "{:<}{:<}{:<}{:<}{:<}{:<}".format('Patient\t','Diagnosis\t','Disease\t\t\t','Disease\t\t','Treatment\t\t','Treatment\n')
	second_line = "{:<}{:<}{:<}{:<}{:<}{:<}".format('Name\t','Accuracy\t','Name\t\t\t','Incidence\t','Name\t\t\t','Risk\n')
	third_line = "-------------------------------------------------------------------------"
	listheader = first_line+second_line+third_line
	saving_to_the_output_file(listheader)   #printing header
	for patient in all_patients_list:
		patient_name= patient[0] + (2-(len(patient[0])//4))*"\t"         #dividing with 4 is for adding tabs to the list
		diagnosis_accuracy = patient[1] + (3-(len(patient[1])//4))*"\t"
		disease_name = patient[2] + (4-(len(patient[2])//4))*"\t"
		disease_incidence = patient[3] + (3-(len(patient[3])//4))*"\t"
		treatment_risk = patient[4] + (4-(len(patient[4])//4))*"\t"
		saving_to_the_output_file(patient_name+diagnosis_accuracy+disease_name+disease_incidence+treatment_risk+patient[5])  #saving outputs


def get_the_patients_informations(name): #this helps probability and recommendation functions to getting patients information as a list
	for index,patient in enumerate(all_patients_list): #index is the index of patient and patient is a list member of all patients list
		if patient[0]==name:
			return all_patients_list[index]


def calculate_probabilty(info_list): #gets patient informations list
	diagnosis_accuracy = float("{}".format(float(info_list[1].strip("%"))/100)) #extracting diagnosis_accuracy, sick poeple, and all people
	sick_people = float(info_list[3].split("/")[0])
	all_people = float(info_list[3].split("/")[1])
	probability = sick_people /((sick_people*diagnosis_accuracy)+(all_people-sick_people)*(1-diagnosis_accuracy)) #calculating probability
	return probability

def probability(input_line):
	if is_patient_exist(input_line.split(" ")[1]): #checking patient
		info_list =  get_the_patients_informations(input_line.split(" ")[1]) #getting patients information
		probability = calculate_probabilty(info_list) #getting probability
		saving_to_the_output_file("Patient {} has a probability of {:.4g}% of having {}.".format(info_list[0],probability*100,info_list[2]))  #saving outputs
	else:
		saving_to_the_output_file("Probability for {} cannot be calculated due to absence.".format(input_line.split(" ")[1]))

def recommendation(input_line):
	if is_patient_exist(input_line.split(" ")[1]): #checking patient
		info_list = get_the_patients_informations(input_line.split(" ")[1]) #getting patients information
		if calculate_probabilty(info_list)>float(info_list[5].strip("%"))/100: #comparing probability with treatment risk
			saving_to_the_output_file("System suggests {} to have the treatment.".format(info_list[0]))  #saving outputs
		else:
			saving_to_the_output_file("System suggests {} NOT to have the treatment.".format(info_list[0]))  #saving outputs
	else:
		saving_to_the_output_file("Recommendation for {} cannot be calculated due to absence.".format(input_line.split(" ")[1]))

def saving_to_the_output_file(output):
	output_file.write(output+"\n")   #writing to the file

all_patients_list = []     #this list stores every patients information
reading_the_input_file()   #copying input as a list into the inputs
output_file = open("doctors_aid_outputs.txt","w")    #openning output file

for line in inputs:   #every member of inputs is a command
	if line.split(" ")[0] == "create":
		create_patient(line)
	elif line.split(" ")[0] == "remove":
		remove_patient(line)
	elif line.split(" ")[0] == "probability":
		probability(line)
	elif line.split(" ")[0] == "recommendation":
		recommendation(line)
	elif line.split(" ")[0] == "list":
		printing_list()

output_file.close()   # closing output file

#Ahmet Şeref Eker
#Hacettepe University Computer Engineering Department
#b2210356098
