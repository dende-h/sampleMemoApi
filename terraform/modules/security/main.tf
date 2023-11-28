

# ====================
#
# ALB用セキュリティグループ
#
# ====================
resource "aws_security_group" "terraform_sec_gp_for_alb" {
  name        = var.alb_sec_group_name
  description = var.alb_sec_group_description
  vpc_id      = var.vpc_id

  # HTTPのトラフィックを許可するためのイングレスルール
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPSのトラフィックを許可するための別のイングレスルール
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  } 

  tags = {
    Name = var.alb_sec_group_name
  }
}

# ====================
#
# EC2用セキュリティグループ
#
# ====================
resource "aws_security_group" "terraform_sec_gp_for_ec2" {
  name        = var.ec2_sec_group_name
  description = var.ec2_sec_group_description
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.ec2_sec_group_name
  }
}

resource "aws_security_group_rule" "security_group_ingress_for_ec2" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.terraform_sec_gp_for_ec2.id
}

resource "aws_security_group_rule" "ingress_for_ec2_from_alb_http" {
  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  security_group_id        = aws_security_group.terraform_sec_gp_for_ec2.id
  source_security_group_id = aws_security_group.terraform_sec_gp_for_alb.id
}

resource "aws_security_group_rule" "ingress_for_ec2_from_alb_https" {
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.terraform_sec_gp_for_ec2.id
  source_security_group_id = aws_security_group.terraform_sec_gp_for_alb.id
}

resource "aws_security_group_rule" "egress_alb_for_ec2_http" {
  type                     = "egress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  security_group_id        = aws_security_group.terraform_sec_gp_for_alb.id
  source_security_group_id = aws_security_group.terraform_sec_gp_for_ec2.id
}

resource "aws_security_group_rule" "egress_alb_for_ec2_https" {
  type                     = "egress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.terraform_sec_gp_for_alb.id
  source_security_group_id = aws_security_group.terraform_sec_gp_for_ec2.id
}

# ====================
#
# RDS用セキュリティグループ
#
# ====================
resource "aws_security_group" "terraform_sec_gp_for_rds" {
  name        = var.rds_sec_group_name
  description = var.rds_sec_group_description
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.terraform_sec_gp_for_ec2.id]
  }

  tags = {
    Name = var.rds_sec_group_name
  }
}

resource "aws_security_group_rule" "security_group_egress_for_rds" {
  type                     = "egress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = aws_security_group.terraform_sec_gp_for_rds.id
  source_security_group_id = aws_security_group.terraform_sec_gp_for_ec2.id
}
