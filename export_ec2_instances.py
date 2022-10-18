import boto3
import csv

def get_all_ec2_instances():
    # This function is called to extract all ec2 instances in a given Account
    
    ec2 = boto3.resource('ec2')
    current_account_id = get_account_id() # invokes the function to get the account number that will be added to the list
    all_instances = [] # Variable where the EC2 details will be added

    for instance in ec2.instances.all():
        instance_details = {
            "Instance_id" : instance.id, 
            "Ami_id" : instance.image_id,
            "Public IP" : instance.public_ip_address,
            "Private IP" : instance.private_ip_address,
            "State" : instance.state['Name'],
            "AWS Account" : current_account_id
            }
        all_instances.append(instance_details) 

    return all_instances

def get_account_id():
    # This function is used to get the AWS Account that is currently in use.
    client = boto3.client("sts")
    return client.get_caller_identity()["Account"]

def export_instances_to_csv(instances):

    csv_columns = ["Instance_id", "Ami_id", "Public IP", "Private IP", "State", "AWS Account"]
    csv_file = "EC2_Instances.csv"
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in instances:
                writer.writerow(data)
    except IOError:
        print("IOError")

def main():
    boto3.setup_default_session(profile_name='temp_ops_sbox')
    instances = get_all_ec2_instances()
    export_instances_to_csv(instances)

if __name__ == "__main__":
    main()
   
