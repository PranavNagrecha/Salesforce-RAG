# CI/CD Template

**Use Case**: CI/CD pipeline for Salesforce deployment

**Template**:

**.github/workflows/deploy.yml** (GitHub Actions):
```yaml
name: Deploy to Salesforce

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Salesforce CLI
        uses: salesforce/setup-sfdx@v1
      
      - name: Authenticate Org
        run: |
          sf org login sfdx-url \
            --sfdx-url-file ${{ secrets.SFDX_URL }}
      
      - name: Deploy
        run: |
          sf project deploy start \
            --target-org production \
            --wait 10
      
      - name: Run Tests
        run: |
          sf apex run test \
            --target-org production \
            --code-coverage \
            --wait 10
```

**Usage**:
- Store SFDX auth URL as GitHub secret
- Pipeline runs on push to main branch
- Deploys and runs tests automatically

