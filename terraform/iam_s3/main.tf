# IAM Role that API Gateway can assume
resource "aws_iam_role" "this" {
  name = var.s3_integration_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "://amazonaws.com" }
    }]
  })
}

# Policy allowing API Gateway to put objects in your specific bucket
resource "aws_iam_role_policy" "this" {
  name = var.s3_integration_policy_name
  role = aws_iam_role.this.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:PutObject"]
      Resource = ["arn:aws:s3:::${var.s3_bucket_name_traget}/*"]
    }]
  })
}

