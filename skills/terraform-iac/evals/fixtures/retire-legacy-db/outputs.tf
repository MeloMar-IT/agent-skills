output "orders_endpoint" {
  value = aws_db_instance.orders.endpoint
}

output "legacy_endpoint" {
  value = aws_db_instance.legacy.endpoint
}
