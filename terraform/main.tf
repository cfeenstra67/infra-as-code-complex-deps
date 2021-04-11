
variable "aws_region" {
  default = "us-east-1"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "test" {
  key_name = "test"
  public_key = file("${path.module}/../iac-test-key.pub")
}

resource "aws_security_group" "test" {
  name_prefix = "test"
  description = "This is used to restrict access to my instance. Managed by Terraform."

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_instance" "test" {
  ami = "ami-07d02ee1eeb0c996c"
  instance_type = "t2.micro"
  key_name = aws_key_pair.test.key_name
  vpc_security_group_ids = [aws_security_group.test.id]
  user_data = "#"
}

output "instance_ip" {
  value = aws_instance.test.public_ip
}
