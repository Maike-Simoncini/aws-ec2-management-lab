import boto3
from datetime import datetime

# Inicializa o cliente EC2
ec2 = boto3.client('ec2', region_name='us-east-1')

def create_snapshots_by_tag(tag_key, tag_value):
    """
    Cria snapshots de todos os volumes EBS de instâncias 
    que possuem uma tag específica.
    """
    print(f"Buscando instâncias com a tag {tag_key}={tag_value}...")
    
    # Filtra instâncias pela Tag
    instances = ec2.describe_instances(
        Filters=[{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
    )

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            
            for mapping in instance['BlockDeviceMappings']:
                volume_id = mapping['Ebs']['VolumeId']
                description = f"Snapshot automatizado da instancia {instance_id} - {datetime.now()}"
                
                print(f"Criando snapshot para o volume {volume_id}...")
                
                response = ec2.create_snapshot(
                    VolumeId=volume_id,
                    Description=description,
                    TagSpecifications=[
                        {
                            'ResourceType': 'snapshot',
                            'Tags': [
                                {'Key': 'Name', 'Value': f"Backup-{instance_id}"},
                                {'Key': 'CreatedBy', 'Value': 'PythonAutomation'}
                            ]
                        }
                    ]
                )
                print(f"Snapshot criado: {response['SnapshotId']}")

if __name__ == "__main__":
    # Exemplo: Criar snapshots de instâncias marcadas para 'Producao'
    create_snapshots_by_tag('Env', 'Production')
