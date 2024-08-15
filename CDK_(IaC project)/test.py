from itertools import count
from msilib.schema import Environment
from multiprocessing import Event
from operator import countOf
from cdk_iam_floyd import ElasticloadbalancingV2, Events, Health, Iam
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
    Tags,
    aws_elasticloadbalancingv2 as elb,
    aws_elasticloadbalancingv2_targets as targets,
    aws_autoscaling as autoscaling,
    aws_certificatemanager as acm
   
       
)
from cdk_ec2_key_pair import KeyPair
from aws_cdk.aws_s3_assets import Asset
from aws_cdk.aws_elasticloadbalancingv2 import SslPolicy
  
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
        elbsg_id=SecurityGp.get("websg_id")
        elbsg_name=SecurityGp.get("websg_name")
        
   
        ####### VPC ( for web server )###############
       
        self.vpc = ec2.Vpc(self,vpc1_id,
                           max_azs=vpc1_max_az,
                           cidr=vpc1_cidr_range,
                           
                           # nat_gateways=1,
                            subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               cidr_mask=27,
                               name=vpc1_subnet_name,
                                  ),
                                  ec2.SubnetConfiguration(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                                #  cidr_mask=27,
                                  name="Private Subnet",),
                            
                            ],
                            nat_gateway_subnets=ec2.SubnetSelection(
                                     subnet_group_name=vpc1_subnet_name,
                                     #subnets=ec2.SubnetType.PUBLIC
                                     ),
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
                            ],
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

        
   
        for i in range(0,2):                          
                           self.cfn_Route = ec2.CfnRoute(self, vpc1_route_id+str(i),
                           route_table_id=self.vpc.public_subnets[i].route_table.route_table_id,
                           destination_cidr_block=self.vpc2.vpc_cidr_block,
                           vpc_peering_connection_id=self.VPCPeering.ref)
                           i=i+1
        for j in range(0,2):              
                           self.cfn_Route = ec2.CfnRoute(self, vpc2_route_id+str(j),
                           route_table_id=self.vpc2.public_subnets[j].route_table.route_table_id,
                           destination_cidr_block=self.vpc.vpc_cidr_block,
                           vpc_peering_connection_id=self.VPCPeering.ref)    
                           j=j+1
        for k in range(0,2):
                           self.cfn_Route = ec2.CfnRoute(self, "route_table_id"+str(k),
                           route_table_id=self.vpc.private_subnets[k].route_table.route_table_id,
                           destination_cidr_block=self.vpc2.vpc_cidr_block,
                           vpc_peering_connection_id=self.VPCPeering.ref)
                           k=k+1                           

        
        

       ######### AMI linux    ############         
                     
        amzn_linux = ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                    )
        ### AMI Windows
        amzn_windows = ec2.MachineImage.latest_windows(
            ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE
                           )
         ### Role ####
        role1= iam.Role(self,"keyrole1",
                              assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                           )
        role1.add_managed_policy(
                                 iam.ManagedPolicy.from_aws_managed_policy_name
                                 ("AmazonSSMManagedInstanceCore")
                                 )
           ###add this role AmazonS3ReadOnlyAccess
        ### Key Pair
        key = KeyPair(self,"KeyPair",
                        name="WebServerKey",
                        store_public_key=True
                     )
        
        key.grant_read_on_private_key(role1)
        key.grant_read_on_public_key(role1)
        ##### User Data for web server launch ######
        with open("./Bucket/userdata1.sh") as f:
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
                                    ec2.Port.tcp(3389),
                                    "SSH Connecton")
        MgmtSG.add_ingress_rule(ec2.Peer.ipv4(mgsg_peer),
                                    ec2.Port.tcp(80),
                                    "HTTP")
        MgmtSG.add_ingress_rule(ec2.Peer.ipv4(mgsg_peer),
                                    ec2.Port.tcp(443),
                                    "HTTPS")

      ### Key Pair for mgmt server ####

        key1 = KeyPair(self,"KeyPair2",
                        name="MgmtServerKey",
                        store_public_key=True
                     )
        
        key1.grant_read_on_private_key(role1)
        key1.grant_read_on_public_key(role1)
      ######## Launch Management server( EC2 Instance )   ########
        
        instance2 = ec2.Instance(self, "mgmtServer",
                    instance_type=ec2.InstanceType("t2.micro"),
                    machine_image=amzn_windows,
                    vpc = self.vpc2,
                    block_devices= [ec2.BlockDevice(
                                device_name="/dev/xvda", 
                                volume=ec2.BlockDeviceVolume.ebs(
                                 volume_size= 8,
                                volume_type=ec2.EbsDeviceVolumeType.GP2,
                                encrypted=True
                    ),
                    mapping_enabled= True
                     )],
       
                        role=role1,
                        security_group = MgmtSG,
                        key_name=key1.key_pair_name
                     )


        ##### Security Group for ELB  ###########
        
        ELBSG=ec2.SecurityGroup(self,"elbsg_id",vpc= self.vpc,
                                  description="ELBSecurityGp",
                                 allow_all_outbound=True,
                                    security_group_name=elbsg_name)
        ELBSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                 ec2.Port.tcp(80),
                                    "http traffic")
        ELBSG.add_ingress_rule(ec2.Peer.any_ipv4(),
                                 ec2.Port.tcp(80),
                                    "https traffic")
      #  ELBSG.add_ingress_rule(ec2.Peer.security_group_id(MgmtSG.security_group_id), ec2.Port.tcp(22),  "ssh")
                                    
         ##### Security Group for ASG  ###########
        ASGSG=ec2.SecurityGroup(self,"ASGSG",vpc= self.vpc,
                                  description="ASGSecurityGp",
                                 allow_all_outbound=True,
                                    security_group_name="ASGSG")
        ASGSG.add_ingress_rule(ec2.Peer.security_group_id(MgmtSG.security_group_id),
                               ec2.Port.tcp(22),"ssh")
        ASGSG.add_ingress_rule(ec2.Peer.security_group_id(ELBSG.security_group_id),
                              ec2.Port.tcp(80),"HTTP")
      #  ASGSG.add_ingress_rule(ec2.Peer.security_group_id(ELBSG.security_group_id),
       #                       ec2.Port.tcp(443),"HTTPS")
       # ASGSG.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(80),"http traffic")
       # ASGSG.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(443),"https traffic")                

        # Create Application Load Balancer
        
        
       # Create AutoScaling Group with 2 EC2 Instances.
        web_server_asg = autoscaling.AutoScalingGroup(self,
                                                       "webServerAsgId",
                                                       vpc=self.vpc,
                                                       vpc_subnets=ec2.SubnetSelection(
                                                           subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                                                       ),
                                                       instance_type=ec2.InstanceType(
                                                           "t3.nano"),
                                                       machine_image=amzn_linux,
                                                       role=role1,
                                                       security_group=ASGSG,
                                                       #associate_public_ip_address=False,
                                                       desired_capacity=1,
                                                       min_capacity=1,
                                                       max_capacity=3,
                                                       #    desired_capacity=2,
                                                       block_devices=[
                                                      autoscaling.BlockDevice(
                                                          device_name="/dev/xvda",
                                                         volume=autoscaling.BlockDeviceVolume.ebs(
                                                         volume_size=8,
                                                         volume_type=ec2.EbsDeviceVolumeType.GP2,
                                                        encrypted=True,
                                                         delete_on_termination=True,
                                                         )
                                                       )
                                                       ],
                                                       #security_group=ASGSG,
                                                       key_name=key.key_pair_name
                                                       
                                                       )
        assets = Asset(
                  self,
                  "Assets",
                  path="./Bucket/userdata1.sh"
                     )
        
        path = web_server_asg.user_data.add_s3_download_command(
                     bucket=assets.bucket,
                     bucket_key=assets.s3_object_key,
                     region="us-east-1"
        )

        web_server_asg.user_data.add_execute_file_command(
            file_path=path
        )

        assets.grant_read(web_server_asg.role)
        
        alb = elb.ApplicationLoadBalancer(
            self,
            "myAlbId",
            vpc=self.vpc,
            internet_facing=True,
            security_group=ELBSG,
            load_balancer_name="WebServerAlb",
            
        )
       
        # Add Listerner to ALB
        listener = alb.add_listener("listernerId",
                                    port=80,
                                    open=True
                                   )
        # listener connection
        listener.connections.allow_default_port_from_any_ipv4("allow")
         # Allow ALB to receive internet traffic
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80),
            description="Allow Internet access on ALB Port 80"
        )

       

        # Allows ASG Security Group receive traffic from ALB
       
        web_server_asg.connections.allow_from(alb, ec2.Port.tcp(80),
                                              description="Allows ASG Security Group receive traffic from ALB")

        # Add AutoScaling Group Instances to ALB Target Group
        listener.add_targets("listenerId", port=80, targets=[web_server_asg])

        ### Health Check
        health_check = elb.HealthCheck(
            interval=Duration.seconds(60), path="/", timeout=Duration.seconds(60)
        )
        ### Autoscaling Action
        web_server_asg.scale_on_cpu_utilization("CPUUtilization", target_utilization_percent=50)