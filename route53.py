import os
import json
import re
import pdb
import time
from subprocess import check_output
# os.system('echo" " > aws_hosted_details.json')
os.system('echo "" > A.txt')
os.system('echo "" > Dns_Not_in_use.txt')
print "Now Downloading  the list hosted zone in AWS ......................"
os.system('aws route53 list-hosted-zones > aws_route53.json')
print "Now Downloading the list of network interface in AWS ......................"
os.system('aws ec2 describe-network-interfaces > network_interface.json')
print "Now Downloading the list of load balancers in AWS ......................"
os.system('aws elb describe-load-balancers > load-balancers.json')
fp = open("aws_route53.json", "r")
obj = json.load(fp)
fp.close()
a=len(obj)
# print a
number_hosted_zone=len(obj["HostedZones"])
print "Number of hosted zone in your AWS: "+ str(number_hosted_zone)
print "Please be patient, It may take about 2 minutes to give you complete results..\n"
# i=0
# while i < number_hosted_zone:
for x in range(number_hosted_zone):
	# print obj["HostedZones"]["Config"]["Id"]["Name"]
	Id= (obj["HostedZones"][x]["Id"])
	Id= re.sub('/hostedzone/','', Id)
	# print Id
	# Name= (obj["HostedZones"][x]["Name"])
	# print Name
	cmd="aws route53 list-resource-record-sets --hosted-zone-id "+Id+ " > aws_hosted_details_2.json"
	os.system(cmd)
	fp = open("aws_hosted_details_2.json", "r")
	obj1 = json.load(fp)
	fp.close()
	number_ResourceRecordSets=len(obj1["ResourceRecordSets"])
	print "Number of ResourceRecordSets: " + str(number_ResourceRecordSets)
	# print "\t"+ "Name" +"\t"+ "types" +"\t"+ "value"
	# start = time.time()
	for y in range(number_ResourceRecordSets):
		try:
			obj1["ResourceRecordSets"][y]["ResourceRecords"]
		except:
			obj1["ResourceRecordSets"][y]["AliasTarget"]
			length=len(obj1["ResourceRecordSets"][y]["AliasTarget"])
			types = obj1["ResourceRecordSets"][y]["Type"]
			DNSName=obj1["ResourceRecordSets"][y]["AliasTarget"]["DNSName"]
			Name = obj1["ResourceRecordSets"][y]["Name"]
			# print "\t"+ Name +"\t"+ types +"\t"+ DNSName
			if types == "A":
				private_ip_cmd="cat network_interface.json | grep "+DNSName+"| wc -l | xargs echo"
				public_ip_cmd="cat network_interface.json | grep "+DNSName+"| wc -l | xargs echo"
				elb_cmd="cat load-balancers.json | grep "+DNSName+" | wc -l | xargs echo"
				private_ip = check_output(private_ip_cmd, shell=True).strip()
				public_ip = check_output(public_ip_cmd, shell=True).strip()
				elb = check_output(elb_cmd, shell=True).strip()
				private_ip = int(private_ip)
				public_ip = int(public_ip)
				elb = int(elb)
				# pdb.set_trace()
				if(private_ip == 0 and public_ip == 0 and elb == 0):
					file = open("Dns_Not_in_use.txt", "a+")
					# print"open"
					file.write(DNSName+","+Name+ '\n')
					# print "wrote"
					file.close()
				file = open("A.txt", "a+")
				file.write(DNSName+","+Name+ '\n')
				file.close()
		else:
			obj1["ResourceRecordSets"][y]["ResourceRecords"]
			length=len(obj1["ResourceRecordSets"][y]["ResourceRecords"])
			types = obj1["ResourceRecordSets"][y]["Type"]
			Name = obj1["ResourceRecordSets"][y]["Name"]
			for z in range (length):
				DNSName=obj1["ResourceRecordSets"][y]["ResourceRecords"][z]["Value"]
				if types == "A":
					private_ip_cmd="cat network_interface.json | grep "+DNSName+"| wc -l | xargs echo"
					public_ip_cmd="cat network_interface.json | grep "+DNSName+"| wc -l | xargs echo"
					elb_cmd="cat load-balancers.json | grep "+DNSName+" | wc -l | xargs echo"
					private_ip = check_output(private_ip_cmd, shell=True).strip()
					public_ip = check_output(public_ip_cmd, shell=True).strip()
					elb = check_output(elb_cmd, shell=True).strip()
					private_ip = int(private_ip)
					public_ip = int(public_ip)
					elb = int(elb)
					# pdb.set_trace()
					if (private_ip == 0 and public_ip == 0 and elb == 0):
						file = open("Dns_Not_in_use.txt", "a+")
						# print "open"
						file.write(DNSName+","+Name+ '\n')
						# print "wrote"
						file.close()
					file = open("A.txt", "a+")
					file.write(DNSName+","+Name+ '\n')
					file.close()
