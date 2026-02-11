provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "lab_vpc" {
  cidr_block = "10.1.0.0/16"

  tags = {
    Name = "lab-vpc"
  }
}

resource "aws_subnet" "lab_subnet" {
  vpc_id     = aws_vpc.lab_vpc.id
  cidr_block = "10.1.1.0/24"

  tags = {
    Name = "lab-subnet"
  }
}

resource "aws_instance" "lab_ec2" {
  ami           = "ami-08d70e59c07c61a3a" # Amazon Linux 2 (us-west-2)
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.lab_subnet.id

  tags = {
    Name = "lab-ec2-instance"
  }
}