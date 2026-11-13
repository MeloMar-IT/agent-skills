resource "aws_db_instance" "legacy" {
  identifier                  = "billing-legacy"
  engine                      = "postgres"
  instance_class              = "db.t3.medium"
  allocated_storage           = 50
  username                    = "billing"
  manage_master_user_password = true
  skip_final_snapshot         = true
}

resource "aws_db_instance" "orders" {
  identifier                  = "orders-prod"
  engine                      = "postgres"
  instance_class              = "db.r6g.large"
  allocated_storage           = 200
  username                    = "orders"
  manage_master_user_password = true
  skip_final_snapshot         = true
  deletion_protection         = false
}

resource "aws_s3_bucket" "orders_exports" {
  bucket        = "acme-orders-exports"
  force_destroy = true
}

resource "aws_dynamodb_table" "orders_index" {
  name         = "orders-index"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }
}

resource "aws_cloudwatch_metric_alarm" "legacy_cpu" {
  alarm_name          = "billing-legacy-cpu"
  namespace           = "AWS/RDS"
  metric_name         = "CPUUtilization"
  comparison_operator = "GreaterThanThreshold"
  threshold           = 90
  evaluation_periods  = 3
  period              = 300
  statistic           = "Average"

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.legacy.identifier
  }
}
