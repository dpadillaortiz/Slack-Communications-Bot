# Terraform config to deploy Slack Bolt app on AWS Lambda with API Gateway

provider "aws" {
  region = "us-west-1"
  default_tags {
    tags = {
      Project     = "WindowsUpdaterSlackApp"
      Environment = "Dev"
      Owner       = "you@example.com"
    }
  }
}

############################
# 1. IAM Role for Lambda
############################
resource "aws_iam_role" "lambda_exec_role" {
  name = "slack_lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "allow_self_invoke" {
  name = "AllowSelfInvoke"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction",
          "lambda:GetFunction",
          "secretsmanager:GetSecretValue"
        ],
        Resource = "*"
      }
    ]
  })
}

############################
# 1a. Slack Secrets in Secrets Manager
############################
resource "aws_secretsmanager_secret" "windows_updater_bot_token_value" {
  name = "/slack/windows_updater_app/aws_windows_bot_token"
}

resource "aws_secretsmanager_secret_version" "windows_updater_bot_token_value" {
  secret_id     = aws_secretsmanager_secret.windows_updater_bot_token_value.id
  secret_string = var.aws_windows_slack_bot_token
}

resource "aws_secretsmanager_secret" "windows_updater_signing_secret" {
  name = "/slack/windows_updater_app/aws_windows_signing_secret"
}

resource "aws_secretsmanager_secret_version" "windows_updater_signing_secret" {
  secret_id     = aws_secretsmanager_secret.windows_updater_signing_secret.id
  secret_string = var.aws_windows_slack_signing_secret
}

############################
# 2. Lambda Function
############################
resource "aws_lambda_function" "slack_handler" {
  function_name = "slack_windows_updater"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.11"
  timeout       = 10
  memory_size = 512
  architectures = ["arm64"]
  layers = [aws_lambda_layer_version.slack_app_dependencies.arn]

  filename         = "./slack_lambda_app.zip"  # Replace with your ZIP path
  source_code_hash = filebase64sha256("./slack_lambda_app.zip")

  environment {
    variables = {
      SLACK_CANVAS          = var.SLACK_CANVAS
      TENTATIVE_SECTION     = var.TENTATIVE_SECTION
      ALT_SECTION_1         = var.ALT_SECTION_1
      ALT_SECTION_2         = var.ALT_SECTION_2
      ALT_SECTION_3         = var.ALT_SECTION_3
    }
  }
}

########################################
# 3. API Gateway and Lambda Integration
########################################
resource "aws_apigatewayv2_api" "slack_api" {
  name          = "slack-events-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.slack_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.slack_handler.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "slack_events" {
  api_id    = aws_apigatewayv2_api.slack_api.id
  route_key = "POST /slack/events"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.slack_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slack_handler.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.slack_api.execution_arn}/*/*"
}

############################
# 4. Variables for Secrets
############################
variable "aws_windows_slack_bot_token" {
  type        = string
  description = "Slack bot token (xoxb-...)"
}

variable "aws_windows_slack_signing_secret" {
  type        = string
  description = "Slack signing secret"
}

variable "SLACK_CANVAS" {
  type        = string
  description = "Canvas id"
}

variable "TENTATIVE_SECTION" {
  type        = string
  description = "section id"
}
variable "ALT_SECTION_1" {
  type        = string
  description = "section id"
}

variable "ALT_SECTION_2" {
  type        = string
  description = "section id"
}

variable "ALT_SECTION_3" {
  type        = string
  description = "section id"
}

variable "ALLOWED_USERS" {
  type        = string
  description = "list of allowed user slack ids"
}

############################
# 5. Log retention (CloudWatch)
############################
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.slack_handler.function_name}"
  retention_in_days = 14
}


############################
# 5. Output the API URL so you can paste it into Slack
############################
output "events_api_url" {
  value = "${aws_apigatewayv2_api.slack_api.api_endpoint}/slack/events"
}

############################
# 5. Create a Lambda Layer version from a local file
############################
resource "aws_lambda_layer_version" "slack_app_dependencies" {
  layer_name               = "slack-bolt-layer"
  filename                 = "./python.zip"
  compatible_runtimes      = ["python3.13"]
  compatible_architectures = ["arm64"]  # match your function's arch
  description              = "Slack Bolt + SDK + aiohttp deps"
}
