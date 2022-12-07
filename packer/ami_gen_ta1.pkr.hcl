# Create an image
# [reference documentation](https://www.packer.io/docs/templates)

# Execution:
# AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
# AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
# packer build ami_gen_example.pkr.hcl


locals { timestamp = regex_replace(timestamp(), "[- TZ:]", "") }

# source blocks configure your builder plugins; your source is then used inside
# build blocks to create resources. A build block runs provisioners and
# post-processors on an instance created by the source.
source "amazon-ebs" "example" {
  ami_name      = "sieve_ami_exampleteam_ta1 ${local.timestamp}"
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
  # this points to the base image specified above
  sources = ["source.amazon-ebs.example"]

  provisioner "shell-local" {
    inline = ["echo does_nothing_useful_but_demonstrates"]  
  }

  provisioner "shell" {
    inline = [
      "sleep 30",
      
      # Copy the necessary files and set up the prover
      "cd ~/",
      "mkdir offline_store",
      "mkdir output",
      ""
    ]
  }
  
    
  provisioner "file" {
    source = "../../testcase-generation/"
    destination = "/tmp/gen"
  }
  
  
  provisioner "shell" {
    inline = [
      
      "mv /tmp/gen/generate_statements ~/generate_statements",
      "mv /tmp/gen ~/testcase-generation",
    
      # Set permissions
      "chmod 777 ~/generate_statements",
      "chmod -R 777 ~/testcase-generation",          
      ""
    ]
  }

}