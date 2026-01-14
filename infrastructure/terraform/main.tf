# Terraform AWS Infrastructure

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "worldtree-ai"
}

# SageMaker endpoint for model hosting
resource "aws_sagemaker_model" "worldtree_model" {
  name               = "${var.project_name}-model"
  execution_role_arn = aws_iam_role.sagemaker_role.arn

  primary_container {
    image = "placeholder-ecr-image-url"
  }
}

# IAM role for SageMaker
resource "aws_iam_role" "sagemaker_role" {
  name = "${var.project_name}-sagemaker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      }
    ]
  })
}
