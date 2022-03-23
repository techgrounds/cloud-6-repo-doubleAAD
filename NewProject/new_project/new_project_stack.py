from itertools import count
from msilib.schema import Environment
from multiprocessing import Event
from operator import countOf
from cdk_iam_floyd import Events, Iam
from constructs import Construct
import boto3
import socket

from aws_cdk import (
    
    Duration,
    RemovalPolicy,
    Stack,
    CfnOutput,
    
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_kms as kms,
    aws_backup as backup,
    aws_events as events,
    aws_iam as iam,
    Tags
    
       
)
from cdk_ec2_key_pair import KeyPair
from aws_cdk.aws_s3_assets import Asset
  
class NewProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #####     Parameters    ##########
        myenvironment=self.node.try_get_context("myenvironment")

         ###     VPC parameters    ########
        vpcenv=myenvironment.get("vpc_s")
        vpc1_id=vpcenv.get("vpc1_id")
        vpc1_max_az= vpcenv.get("vpc1_max_az")
        vpc1_subnet_name= vpcenv.get("vpc1_subnet_name")
        vpc1_cidr_range=vpcenv.get("vpc1_cidr_range")
        vpc2_id=vpcenv.get("vpc2_id")
        vpc2_max_az=vpcenv.get("vpc2_max_az")
        vpc2_subnet_name= vpcenv.get("vpc2_subnet_name")
        vpc2_cidr_range=vpcenv.get("vpc2_cidr_range")
        ## Peering #####
        peering_id= vpcenv.get("peering_id")
        peering_region= vpcenv.get("peering_region")
        vpc1_route_id = vpcenv.get("vpc1_route_id")
        vpc2_route_id = vpcenv.get("vpc2_route_id")
         ##### server security grp parameters ###
        SecurityGp=myenvironment.get("SecurityGp")
        mgsg_id=SecurityGp.get("mgsg_id")
        mgsg_name=SecurityGp.get("mgsg_name")
        mgsg_peer= SecurityGp.get("mgsg_peer")
        websg_id=SecurityGp.get("websg_id")
        websg_name=SecurityGp.get("websg_name")
        ##### Instances######
        Servers=myenvironment.get("Servers")
        web_instance_id=Servers.get("web_instance_id")
        web_instance_type= Servers.get("web_instance_type")
        web_volume_size =Servers.get("web_volume_size")
        mgmt_instance_id=Servers.get("mgmt_instance_id")
        mgmt_instance_type= Servers.get("mgmt_instance_type")
        mgmt_volume_size =Servers.get("mgmt_volume_size")
        #######  Backup jobs #######
        BackupServers=myenvironment.get("BackupServers")    
        hour1=BackupServers.get("hour1")  
        minute1=BackupServers.get("minute1")
        day1=BackupServers.get("day1")
        month1=BackupServers.get("month1")
        year1=BackupServers.get("year1")
        duration1=BackupServers.get("duration1")  
        hour2=BackupServers.get("hour2")  
        minute2=BackupServers.get("minute2")
        day2=BackupServers.get("day2")
        month2=BackupServers.get("month2")
        year2=BackupServers.get("year2")
        duration2=BackupServers.get("duration2")  
        ####### VPC ( for web server )###############
       
        self.vpc = ec2.Vpc(self,vpc1_id,
                           max_azs=vpc1_max_az,
                           cidr=vpc1_cidr_range,
                            subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name=vpc1_subnet_name,
                                  )
                            ]
                             )
            
        CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)

         #### VPC 2 settings for management server  ####

        self.vpc2 = ec2.Vpc(self, vpc2_id,
                           max_azs=vpc2_max_az,
                           cidr=vpc2_cidr_range,
                            subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name=vpc2_subnet_name
                                  )
                            ]
                            )
        CfnOutput(self, "Output1",
                       value=self.vpc2.vpc_id)
         

      #### VPC Peering ######

        self.VPCPeering = ec2.CfnVPCPeeringConnection(
            self,
            peering_id,
            peer_vpc_id=self.vpc.vpc_id,
            vpc_id=self.vpc2.vpc_id,
            peer_region= peering_region
            )
         
         
   
        for i in range(0,1):                          
                           self.cfn_Route = ec2.CfnRoute(self, vpc1_route_id,
                           route_table_id=self.vpc.public_subnets[i].route_table.route_table_id,
                           destination_cidr_block=self.vpc2.vpc_cidr_block,
                           vpc_peering_connection_id=self.VPCPeering.ref)
        for j in range(0,1):              
                           self.cfn_Route = ec2.CfnRoute(self, vpc2_route_id,
                           route_table_id=self.vpc2.public_subnets[j].route_table.route_table_id,
                           destination_cidr_block=self.vpc.vpc_cidr_block,
                           vpc_peering_connection_id=self.VPCPeering.ref)                               

        
        

       ######### AMI linux    ############         
                     
        amzn_linux = ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                    )

         ### Role ####
        role1= iam.Role(self,"keyrole1",
                              assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                           )
        role1.add_managed_policy(
                                 iam.ManagedPolicy.from_aws_managed_policy_name
                                 ("AmazonSSMFullAccess")
                                 )
        ### Key Pair
        key = KeyPair(self,"KeyPair",
                        name="WebServerKey",
                        store_public_key=True
                     )
        
        key.grant_read_on_private_key(role1)
        key.grant_read_on_public_key(role1)
        ##### User Data for web server launch ######
        with open("./Bucket/userdata.sh") as f:
                    user_data = f.read()

        ##### Security Group for Management Server  ###########

        MgmtSG=ec2.SecurityGroup(self,mgsg_id,
                                 vpc= self.vpc2,
                                 description="MgmtSecurityGp",
                                 allow_all_outbound=True,
                                 security_group_name=mgsg_name)
        MgmtSG.add_ingress_rule(ec2.Peer.ipv4(mgsg_peer),
                                    ec2.Port.tcp(22),
                                    "SSH Connecton")
        MgmtSG.add_ingress_rule(ec2.Peer.ipv4(mgsg_peer),
                                    ec2.Port.tcp(80),
                                    "HTTP")
        MgmtSG.add_ingress_rule(ec2.Peer.ipv4(mgsg_peer),
                                    ec2.Port.tcp(443),
                                    "HTTPS")
        ##### Security Group for web server ###########
        
        webSG=ec2.SecurityGroup(self,websg_id,vpc= self.vpc,
                                  description="WebSecurityGp",
                                 allow_all_outbound=True,
                                    security_group_name=websg_name)
        webSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                 ec2.Port.tcp(80),
                                    "http traffic")
        webSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                 ec2.Port.tcp(443),
                                    "https traffic")
        webSG.add_ingress_rule(ec2.Peer.security_group_id(MgmtSG.security_group_id), 
                                    ec2.Port.tcp(22),
                                       "ssh")
                                      
       # webSG.add_ingress_rule(ec2.Peer.any_ipv4(),
        #                         ec2.Port.tcp(socket.IPPROTO_ICMP),
         #                           "ping")



       
        ######## Launch web server( EC2 Instance )   ########

        instance1 = ec2.Instance(self, web_instance_id,
                                    instance_type=ec2.InstanceType(web_instance_type),
                                    machine_image=amzn_linux,
                                    vpc = self.vpc,
                                     block_devices= [
                                        ec2.BlockDevice(
                                       device_name="/dev/xvda", 
                                       volume=ec2.BlockDeviceVolume.ebs(
                                          volume_size= web_volume_size,
                                          volume_type=ec2.EbsDeviceVolumeType.GP2,
                                          encrypted=True
                                          ),
                                     mapping_enabled= True
                                       ) 
                                                ],
                                # user_data=ec2.UserData.custom(user_data),
                                 role=role1,
                                  security_group = webSG,
                                  key_name=key.key_pair_name
                                 )
        instance1.connections.allow_from_any_ipv4(
                                             port_range=ec2.Port.tcp(80),
                                             description="Allow Web Traffic"
                                                )

        
        
        CfnOutput(self,"ip", value=str(instance1.instance_private_ip))
       
        assets = Asset(
                  self,
                  "Assets",
                  path="./Bucket/userdata.sh"
                     )
        
        path = instance1.user_data.add_s3_download_command(
                     bucket=assets.bucket,
                     bucket_key=assets.s3_object_key,
                     region="us-east-1",
        )

        instance1.user_data.add_execute_file_command(
            file_path=path
        )

        assets.grant_read(instance1.role)
        
         ### Key Pair for mgmt server ####

        key1 = KeyPair(self,"KeyPair2",
                        name="MgmtServerKey",
                        store_public_key=True
                     )
        
        key1.grant_read_on_private_key(role1)
        key1.grant_read_on_public_key(role1)
       
      #### Nacl ########
       
        aclcidr1= ec2.AclCidr.any_ipv4()
        nacl=ec2.NetworkAcl(self,"mynacl",vpc=self.vpc2)
        nacl.add_entry("id",cidr=aclcidr1,rule_number=100,
               traffic=ec2.AclTraffic.all_traffic(),direction=ec2.TrafficDirection.EGRESS,
                  network_acl_entry_name="myentry",rule_action=ec2.Action.ALLOW)
   
    ######## Launch Management server( EC2 Instance )   ########
        
        instance2 = ec2.Instance(self, mgmt_instance_id,
                    instance_type=ec2.InstanceType(mgmt_instance_type),
                    machine_image=amzn_linux,
                    vpc = self.vpc2,
                    block_devices= [ec2.BlockDevice(
                                device_name="/dev/xvda", 
                                volume=ec2.BlockDeviceVolume.ebs(
                                 volume_size= mgmt_volume_size,
                                volume_type=ec2.EbsDeviceVolumeType.GP2,
                                encrypted=True
                    ),
                    mapping_enabled= True
                     )],
       
        role=role1,
        security_group = MgmtSG,
        key_name=key1.key_pair_name
        )
       
        ## server Tags ###
        Tags.of(instance1).add(key="webs",value="webbackup")
        Tags.of(instance2).add(key="mgmt",value="mgmtbackup")

        #### Back up Web Server ####
        WebBackupkey = kms.Key(
            self,
            "BackupkeyWebServer",
            removal_policy=RemovalPolicy.DESTROY
            )
        vault1= backup.BackupVault(self,"WebServerVault",
                                    backup_vault_name="WebServerVault",
                                    encryption_key=WebBackupkey,
                                    removal_policy=RemovalPolicy.DESTROY
                                    )
        backup_plan1 = backup.BackupPlan(self,"Backup1",
                                          backup_plan_name="webserverBackup"
                                          )
        backup_plan1.add_selection("ec2web",resources=[
                                    backup.BackupResource.from_tag(key="webs",value="webbackup")
                                             ]
                                                            )

        backup_plan1.add_rule(backup.BackupPlanRule(
                              backup_vault=vault1,
                              rule_name="WebRule",
                              schedule_expression=events.Schedule.cron
                                 (hour=hour1 ,minute=minute1,day=day1, month=month1,year=year1),
                              delete_after=Duration.days(duration1),
                              completion_window=Duration.hours(2),
                              start_window=Duration.hours(1)
                               ))           
                              
        #### Back up Management Server ####
        Mgmtbackupkey = kms.Key(
            self,
            "BackupkeyMgmtServer",
            removal_policy=RemovalPolicy.DESTROY
            )
        vault2= backup.BackupVault(self,"MgmtServerVault",
                                  backup_vault_name="MgmtServerVault",
                                  encryption_key=Mgmtbackupkey,
                                 removal_policy=RemovalPolicy.DESTROY)
        backup_plan2 = backup.BackupPlan(self,"Backup2",backup_plan_name="MgmtserverBackup")
        backup_plan2.add_selection("ec2mgmt",resources=[
                                          backup.BackupResource.from_tag(key="mgmt",value="mgmtbackup")
                                          ]
                                                            )

        backup_plan2.add_rule(backup.BackupPlanRule(
                              backup_vault=vault2,
                              rule_name="mgmtRule",
                              schedule_expression=events.Schedule.cron(
                                    hour=hour2 ,minute=minute2,day=day2, month=month2,year=year2
                                                ),
                              delete_after=Duration.days(duration2),
                              completion_window=Duration.hours(2),
                              start_window=Duration.hours(1)
                               ))                       
       

    
        
        

                           
        

       
        
        
   
        
     
    