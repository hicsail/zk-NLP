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
source "amazon-ebs" "sieve_ta1" {
  ami_name      = "sieve_ta1 ${local.timestamp}"
  instance_type = "t2.micro"
  region        = "us-east-1"
  source_ami_filter {
    filters = {
      name = "amzn2-ami-hvm-*-x86_64-gp2"
    }
    most_recent = true
    # Indicate that only an ami from Amazon should be used
    owners = ["137112412989"]
  }
  ssh_username = "ec2-user"
}

# a build block invokes sources and runs provisioning steps on them.
# https://www.elastic.co/guide/en/beats/metricbeat/current/setup-repositories.html
build {
  sources = ["source.amazon-ebs.sieve_ta1"]

  # Packaging necessary modules into tar file
  provisioner "shell-local" {
    inline = [
      "echo 'Removing existing ../tmp-mini'",
      "rm -rf ../tmp-mini",
      "rm -rf ../tmp-mini.tar.gz",
      "git clone git@github.mit.edu:sieve-all/TA1.git ../tmp-mini",
      "echo 'checking tmp-mini directory'",
      "ls -l ../tmp-mini",
      "echo 'checking tmp-generation directory'",
      "ls -l ../tmp-mini/testcase-generation",
      "echo 'Creating tarball'",
      "tar -zcf ../tmp-mini.tar.gz ../tmp-mini",
      ""
    ]
  }

  provisioner "file" {
    source      = "../tmp-mini.tar.gz"
    destination = "/tmp/"
  }

  provisioner "shell" {
    inline = [
      "cd /tmp",
      "tar -zxvf tmp-mini.tar.gz",
      "sudo yum -y update",
      "sudo yum -y install python3-pip",
      "cd /tmp/tmp-mini",
      "pip3 install /tmp/tmp-mini/ --no-cache-dir",
      "pip3 install https://github.com/gxavier38/pysnark/archive/8a2a571bef430783adf8fe28cb8bb0b0bf8a7c94.zip",
      "echo 'Running generate_statements'",
      "python3 /tmp/tmp-mini/testcase-generation/generate_statements_ta1 /tmp/tmp-mini/testcase-generation/config_ta1.json",
      "echo 'checking IRs generated'",
      "ls -l /tmp/tests",
      ""
    ]
  }
}