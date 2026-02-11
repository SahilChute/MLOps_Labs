cat > README.md << EOF
# Terraform Beginner Lab Submission

## Overview

This Terraform configuration creates a simple AWS infrastructure:

- A **VPC** (\`lab-vpc\`)  
- A **subnet** (\`lab-subnet\`) inside the VPC  
- An **EC2 instance** (\`lab-ec2-instance\`) inside the subnet  

It demonstrates creating, modifying, and managing AWS resources using Terraform.

## How to Use

1. **Initialize Terraform**:
\`\`\`bash
terraform init
\`\`\`

2. **Plan the changes**:
\`\`\`bash
terraform plan
\`\`\`

3. **Apply the configuration**:
\`\`\`bash
terraform apply
\`\`\`

4. **View outputs** (resource IDs):
\`\`\`bash
terraform output
\`\`\`

5. **Destroy resources** after testing:
\`\`\`bash
terraform destroy
\`\`\`

## Notes

- The EC2 instance uses a **Free Tier eligible t3.micro** instance type.  
- The outputs provide IDs for the EC2 instance, subnet, and VPC to verify creation.  
- No Terraform state or provider binaries are included in this submission.
EOF