module "lambda" {
  source        = "terraform-aws-modules/lambda/aws"
  version       = "8.1.2"
  function_name = var.aws_lambda_name
  handler       = "main.lambda_handler"
  runtime       = "python3.13"

  source_path = "../src"
}

