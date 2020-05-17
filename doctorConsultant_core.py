#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 16:01:54 2020
@author: GROUP085
"""
import array
import os
import traceback

#Initialize Patient id prefix 
index = 1000

class PatientRecord:
    def __init__(self, age, name, Pid):
        #Patient Record data structure
        self.Patid = str(Pid) + str(age)
        self.name = name
        self.age = age
        self.left = None
        self.right = None

class PatientRecordInDoublyLinkedList:

    def __init__(self):
        self.head = None

    def Pid(self):
        #Generate Patient id prefix and return in response 
        global index
        index += 1
        return index

    def registerPatient(self, age, name):
        #register Patient record
        if self.head is None :
            # register when no patient previously registered
            self.left = None
            new_node = PatientRecord(age, name, self.Pid())
            self.head = new_node
        else:
            # register when a patient already registered
            new_node = PatientRecord(age, name, self.Pid())
            current_node = self.head
            while current_node.right :
                current_node = current_node.right
            current_node.right = new_node
            new_node.left = current_node
            new_node.right = None
        return str(self.Pid())+age

    def _dequeuePatient(self,id):
        # deregister patient 
        current_node = self.head
        while current_node:
            if current_node.Patid.strip() == str(id) and current_node == self.head:
                 # deregister patient when it is first in doublylinked list
                if not current_node.right:
                    current_node = None
                    self.head = None
                    return
                else:
                    nxt = current_node.right
                    current_node.right = None
                    current_node.left = None
                    current_node = None
                    self.head = nxt
                    return
            elif current_node.Patid.strip() == str(id):
                # deregister patient when it is in middle of doublylinked list
                if current_node.right:
                    pre = current_node.left
                    post = current_node.right
                    pre.right = post
                    post.left = pre
                    current_node.left = None
                    current_node.right= None
                    current_node = None
                    return
                else:
                    # deregister patient when it is last in doublylinked list
                    pre = current_node.left
                    pre.right = None
                    current_node.left = None
                    current_node.right = None
                    current_node = None
                    return
            current_node = current_node.right

    def getPatientBasedOnAgeToAddInMaxHeap(self):
        # return patient id and age in dictionary format
        PatientDict = {}
        current_node = self.head
        while current_node:
            PatientDict[int(current_node.Patid)] = int(current_node.age)
            current_node = current_node.right
        return PatientDict

    def getPatientRecordBasedOnPID(self,id):
        # print patient id and name as per id (i.e. patient id) input
        current_node = self.head
        while current_node:
            if current_node.Patid.strip() == str(id):
                if current_node.Patid.strip() != None :
                    record_output.write(" "+current_node.Patid.strip())
                    record_output.write(",")
                    record_output.write(current_node.name.strip())
                    record_output.write("\n ")
                return
            current_node = current_node.right

    def heapify(self,arr, n, i):
        largest = i # Initialize largest as root
        l = 2 * i + 1     # left = 2*i + 1
        r = 2 * i + 2     # right = 2*i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i],arr[largest] = arr[largest],arr[i] # swap
            patientRecord.heapify(arr, n, largest)
    
    def heapSort(self,arr):
        # Max heap sort with heapify
        n = len(arr)
        for i in range(n, -1, -1):
            patientRecord.heapify(arr, n, i)
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i] # swap
            patientRecord.heapify(arr, i, 0)
    
    def enqueuePatient(self):
        #return array of sorted patient queue
        arr = array.array('i',[])
        for i in patientRecord.getPatientBasedOnAgeToAddInMaxHeap().keys():
            arr.append(i)
        patientRecord.heapSort(arr)
        return arr
    
    def _len_enqueuePatient(self):
        #return length of array of sorted patient queue
        arr = patientRecord.enqueuePatient()
        size = len(arr)
        return size
    
    def printenqueuePatient(self):
        #print sorted patient queue details 
        arr = patientRecord.enqueuePatient()
        n = len(arr)
        record_output.write("\nRefreshed queue: \n ")
        for i in range(n):
            patientRecord.getPatientRecordBasedOnPID(arr[i])
    
    
    def get_patient_id_next_for_Consultation(self,val):
        #return max patient id who will be next patient 
        for key, value in patientRecord.getPatientBasedOnAgeToAddInMaxHeap().items():
            if str(val).strip() == str(key).strip():
                return key
        return "key doesn't exist"
    
    def nextPatient(self):
        #return patient details of who will be next patient 
        arr = patientRecord.enqueuePatient()
        record_output.write("\nNext patient for consultation is:")
        patientRecord.getPatientRecordBasedOnPID(patientRecord.get_patient_id_next_for_Consultation(str(arr[-1])))
        patientRecord._dequeuePatient(patientRecord.get_patient_id_next_for_Consultation(str(arr[-1])))
    

patientRecord = PatientRecordInDoublyLinkedList()
try:
    with open("outputPS5.txt","w+") as record_output:

        os.chmod("outputPS5.txt", 0o777)
        # read patient details who are available for consultation from inputPS5a.txt 
        with open("InputPS5a.txt",'r') as first_set_of_registrations:
            n=first_set_of_registrations.readlines()
            if n!= 0:                
                for i in n:
                    if ',' in i:
                        name,age = i.split(',')
                        patientRecord.registerPatient(age, name)                    
                record_output.write("\n-------------initial queue----------------\n ")
                record_output.write("\nNo of patients added:"+ str(len(patientRecord.getPatientBasedOnAgeToAddInMaxHeap())))
                patientRecord.enqueuePatient()
                patientRecord.printenqueuePatient()
                record_output.write("\n------------------------------------------\n ")
            else:
                record_output.write("\nInitial input file is blank !")

        # read next patient details who are available for consultation from inputPS5b.txt and has newPatient tag in it 
        with open("InputPS5b.txt",'r') as new_set_of_registrations:
            n=new_set_of_registrations.readlines()
            if n!=0 :               
                record_output.write("\n-----------new patient entered---------\n ")
                for i in n:
                    if ',' in i and i.startswith('newPatient:'):
                        patientDetailWithTag = i.strip()
                        namewithTag,age = patientDetailWithTag.split(',')
                        name = namewithTag.split(':')[1]
                        newRegisteredPatientId = patientRecord.registerPatient(age, name)
                        record_output.write("\n Patient details: " + name + "," +age + "," + newRegisteredPatientId )
                patientRecord.enqueuePatient()
                patientRecord.printenqueuePatient()
                record_output.write("\n------------------------------------------\n ")
            else:
                record_output.write("\nNew patient input file is blank !")            

        # read promptsPS5.txt for nextPatient prompt  
        with open("promptsPS5.txt",'r') as next_patient_for_ConsultationPromt:
            n=next_patient_for_ConsultationPromt.readlines()
            if n!=0 :               
                for i in n:
                    if 'nextPatient' in i:
                        sizeOfEnqueue = patientRecord._len_enqueuePatient()
                        if sizeOfEnqueue != 0 :
                            record_output.write("\n-----------next patient-------- \n ")
                            patientRecord.nextPatient()
                            record_output.write("\n------------------------------------------\n ")
                            patientRecord.enqueuePatient()
                            patientRecord.printenqueuePatient()
                        else:
                            record_output.write("\nNo Patient is Waiting outside .. wait to get them enrolled in Queue ")
                    else:
                        record_output.write("\nWaiting for next Patient prompt ! \n------------------------------------------\n")
            else:
                record_output.write("\nNext patient prompt input file is blank !")

except FileNotFoundError:
    print("Place input files named as InputPS5a.txt , InputPS5b.txt and promptsPS5.txt identical to this app in order to run the application")
except Exception:
    traceback.print_exc()
finally:
    first_set_of_registrations.close()
    new_set_of_registrations.close()
    next_patient_for_ConsultationPromt.close()
    record_output.close()