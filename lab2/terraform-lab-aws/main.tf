provider "aws" {
  region = "us-west-2"
}

# Create a VPC
resource "aws_vpc" "lab_vpc" {
  cidr_block = "10.1.0.0/16"

  tags = {
    Name = "lab-vpc"
  }
}

# Create a subnet inside the VPC
resource "aws_subnet" "lab_subnet" {
  vpc_id     = aws_vpc.lab_vpc.id
  cidr_block = "10.1.1.0/24"

  tags = {
    Name = "lab-subnet"
  }
}

# Launch an EC2 instance inside the subnet
resource "aws_instance" "lab_ec2" {
  ami           = "ami-08d70e59c07c61a3a" # Amazon Linux 2 (us-west-2)
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.lab_subnet.id

  tags = {
    Name = "lab-ec2-instance"
  }
}

# Outputs to show resource IDs
output "ec2_instance_id" {
  value = aws_instance.lab_ec2.id
}

output "subnet_id" {
  value = aws_subnet.lab_subnet.id
}

output "vpc_id" {
  value = aws_vpc.lab_vpc.id
}