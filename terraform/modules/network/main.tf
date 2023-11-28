data "aws_availability_zones" "available" {
  state = "available"
}

# ====================
#
# VPC
#
# ====================
resource "aws_vpc" "terraform_vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = var.vpc_name
  }
}

# ====================
#
# IGW
#
# ====================
resource "aws_internet_gateway" "terraform_igw" {
  vpc_id = aws_vpc.terraform_vpc.id
  tags = {
    Name = var.igw_name
  }
}

# ====================
#
# Route Table（パブリックサブネット用）
#
# ====================
resource "aws_route_table" "terraform_public_subnet_route_table" {
  vpc_id = aws_vpc.terraform_vpc.id
  tags = {
    Name = var.public_subnet_route_table_name
  }
}

# ====================
#
# パブリックサブネット
#
# ====================
resource "aws_subnet" "terraform_public_subnet1" {
  vpc_id                  = aws_vpc.terraform_vpc.id
  cidr_block              = var.public_subnet1_cidr_block
  map_public_ip_on_launch = true
  availability_zone       = element(data.aws_availability_zones.available.names, 0)
  tags = {
    Name = var.public_subnet1_name
  }
}

resource "aws_subnet" "terraform_public_subnet2" {
  vpc_id                  = aws_vpc.terraform_vpc.id
  cidr_block              = var.public_subnet2_cidr_block
  map_public_ip_on_launch = true
  availability_zone       = element(data.aws_availability_zones.available.names, 1)
  tags = {
    Name = var.public_subnet2_name
  }
}

resource "aws_route_table_association" "terraform_associate_route_table_for_public_subnet1" {
  subnet_id      = aws_subnet.terraform_public_subnet1.id
  route_table_id = aws_route_table.terraform_public_subnet_route_table.id
}

resource "aws_route_table_association" "terraform_associate_route_table_for_public_subnet2" {
  subnet_id      = aws_subnet.terraform_public_subnet2.id
  route_table_id = aws_route_table.terraform_public_subnet_route_table.id
}

resource "aws_route" "terraform_public_subnet_route" {
  route_table_id         = aws_route_table.terraform_public_subnet_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.terraform_igw.id
}

# ====================
#
# Route Table（パブリックサブネット用）
#
# ====================
resource "aws_route_table" "terraform_private_subnet_route_table1" {
  vpc_id = aws_vpc.terraform_vpc.id

  tags = {
    Name = var.private_subnet_route_table_name1
  }
}

resource "aws_route_table" "terraform_private_subnet_route_table2" {
  vpc_id = aws_vpc.terraform_vpc.id

  tags = {
    Name = var.private_subnet_route_table_name2
  }
}

# ====================
#
# プライベートサブネット
#
# ====================
resource "aws_subnet" "terraform_private_subnet1" {
  cidr_block              = var.private_subnet1_cidr_block
  vpc_id                  = aws_vpc.terraform_vpc.id
  map_public_ip_on_launch = false
  availability_zone       = element(data.aws_availability_zones.available.names, 0)

  tags = {
    Name = var.private_subnet1_name
  }
}

resource "aws_subnet" "terraform_private_subnet2" {
  cidr_block              = var.private_subnet2_cidr_block
  vpc_id                  = aws_vpc.terraform_vpc.id
  map_public_ip_on_launch = false
  availability_zone       = element(data.aws_availability_zones.available.names, 1)

  tags = {
    Name = var.private_subnet2_name
  }
}

resource "aws_route_table_association" "terraform_associate_route_table_for_private_subnet1" {
  subnet_id      = aws_subnet.terraform_private_subnet1.id
  route_table_id = aws_route_table.terraform_private_subnet_route_table1.id
}

resource "aws_route_table_association" "terraform_associate_route_table_for_private_subnet2" {
  subnet_id      = aws_subnet.terraform_private_subnet2.id
  route_table_id = aws_route_table.terraform_private_subnet_route_table2.id
}



# Assuming you have defined the VPC, route table, and AWS region as variables or resources in your Terraform code
# If not, you need to define resources for aws_vpc and aws_route_table or use appropriate variable references.




