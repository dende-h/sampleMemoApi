
# ====================
#
# ALB
#
# ====================
resource "aws_lb" "terraform_alb" {
  name               = var.alb_name
  internal           = false //外部のインターネットに向けたロードバランサ
  load_balancer_type = "application"
  security_groups    = [var.alb_sec_group_id]
  subnets            = [var.public_subnet1_id, var.public_subnet2_id]

  enable_deletion_protection = false //ロードバランサの削除保護無効

  tags = {
    Name = var.alb_name
  }
}


# ====================
#
# ターゲットグループ
#
# ====================
resource "aws_lb_target_group" "terraform_target_group" {
  name     = var.alb_target
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    interval            = 30
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    healthy_threshold   = 5
    unhealthy_threshold = 2
    matcher             = "200"
  }

  tags = {
    Name = var.alb_target
  }
}

resource "aws_lb_target_group_attachment" "alb-attach" {
  count            = 2
  target_group_arn = aws_lb_target_group.terraform_target_group.arn
  target_id        = var.target_ec2
  port             = 80
}

# ====================
#
# リスナー
#
# ====================
resource "aws_lb_listener" "listener_resource" {
  load_balancer_arn = aws_lb.terraform_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}


# ====================
#
# Listner
#
# ====================
resource "aws_lb_listener" "for_webserver" {
  load_balancer_arn = aws_lb.terraform_alb.arn
  port              = "443"
  protocol          = "HTTPS"
  #certificate_arn   = aws_acm_certificate.example.arn #証明書
  ssl_policy        = "ELBSecurityPolicy-2016-08"
 
  default_action { //ロードバランサーが受信したトラフィックをどのように処理するかを指定
    type             = "forward"
    target_group_arn = aws_lb_target_group.terraform_target_group.arn
  }
}
 
#パスによってリスナーを振り分けるルールの設定
# resource "aws_lb_listener_rule" "forward" {
#   listener_arn = aws_lb_listener.for_webserver.arn
#   priority     = 99
 
#   action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.for_webserver.arn
#   }
 
#   condition {
#     path_pattern {
#       values = ["/*"]
#     }
#   }
# }


## 独自ドメインで使用する場合は下記リソースを利用してSSL証明書をリクエストする

# # ====================
# #
# # Route53
# #
# # ====================
# data "aws_route53_zone" "example" {
#   name = "登録したドメイン"
# }
 
# resource "aws_route53_record" "example" {
#   zone_id = data.aws_route53_zone.example.zone_id
#   name    = data.aws_route53_zone.example.name
#   type    = "A"
 
#   alias {
#     name                   = aws_lb.for_webserver.dns_name
#     zone_id                = aws_lb.for_webserver.zone_id
#     evaluate_target_health = true
#   }
# }
# # ====================
# #
# # ACM
# #
# # ====================
# resource "aws_acm_certificate" "example" {
#   domain_name               = aws_route53_record.example.name
#   subject_alternative_names = []
#   validation_method         = "DNS"
 
#   lifecycle {
#     create_before_destroy = true
#   }
# }
 
# # 検証用DNSレコード
# resource "aws_route53_record" "example_certificate" {
#   name    = aws_acm_certificate.example.domain_validation_options[0].resource_record_name
#   type    = aws_acm_certificate.example.domain_validation_options[0].resource_record_type
#   records = [aws_acm_certificate.example.domain_validation_options[0].resource_record_value]
#   zone_id = data.aws_route53_zone.example.id
#   ttl     = 60
# }
 
# # SSL証明書の検証
# resource "aws_acm_certificate_validation" "example" {
#   certificate_arn         = aws_acm_certificate.example.arn
#   validation_record_fqdns = [aws_route53_record.example_certificate.fqdn]
# }
 
# # ====================
# #
# # Output
# #
# # ====================
# output "domain_name" {
#   value = aws_route53_record.example.name
# }