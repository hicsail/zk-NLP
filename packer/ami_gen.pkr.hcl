# Create an image
# [reference documentation](https://www.packer.io/docs/templates)

# Execution:
# AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
# AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
# packer build ami_gen.pkr.hcl


locals { timestamp = regex_replace(timestamp(), "[- TZ:]", "") }

# source blocks configure your builder plugins; your source is then used inside
# build blocks to create resources. A build block runs provisioners and
# post-processors on an instance created by the source.
source "amazon-ebs" "example" {
  ami_name      = "sieve_ami_example_basic ${local.timestamp}"
  instance_type = "t2.micro"
  region        = "us-east-1"
  source_ami_filter {
    filters = {
      name                = "amzn2-ami-hvm-*-x86_64-gp2"
    }
    most_recent = true
    # Indicate that only an ami from Amazon should be used
    owners      = ["137112412989"]
  }
  ssh_username = "ec2-user"
}

# a build block invokes sources and runs provisioning steps on them.
# https://www.elastic.co/guide/en/beats/metricbeat/current/setup-repositories.html
build {
  sources = ["source.amazon-ebs.example"]

  provisioner "shell" {
    inline = [
      "sleep 30",
      
      # Setup elastic stack
      "echo '[elastic-7.x]' > elastic.repo",
      "echo 'name=Elastic repository for 7.x packages' >> elastic.repo",
      "echo 'baseurl=https://artifacts.elastic.co/packages/oss-7.x/yum' >> elastic.repo",
      "echo 'gpgcheck=1' >> elastic.repo",            
      "echo 'gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch' >> elastic.repo",      
      "echo 'enabled=1' >> elastic.repo",      
      "echo 'autorefresh=1' >> elastic.repo",      
      "echo 'type=rpm-md' >> elastic.repo",
      "sudo mv elastic.repo /etc/yum.repos.d/elastic.repo",
      "sudo yum update -y",
      "sudo yum install -y metricbeat",
      "sudo yum install -y filebeat",
      
    ]
  }  
  
  
}