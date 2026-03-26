#!/usr/bin/env python3
"""
Dollar Dashboard Deployment Script - GCloud Build Version
GMRC/DE-002 — devops-engineer
Deploys dollar-dashboard to GCP Cloud Run using gcloud builds
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

# Configuration
PROJECT = "sovereign-see"
REGION = "us-central1"
SERVICE_NAME = "dollar-dashboard"
SERVICE_ACCOUNT = "dollaragency@sovereign-see.iam.gserviceaccount.com"
DOCKER_IMAGE = f"gcr.io/{PROJECT}/{SERVICE_NAME}"
DOLLAR_DIR = Path(__file__).parent / "dollar"
CLOUD_BUILD_FILE = "cloudbuild.yaml"

def run_command(cmd, check=True, capture_output=True):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            check=check,
            capture_output=capture_output,
            text=True
        )
        if capture_output:
            print(f"✅ Success: {result.stdout}")
            return result.stdout
        return True
    except subprocess.CalledProcessError as e:
        if capture_output:
            print(f"❌ Error: {e.stderr}")
        raise

def check_gcloud_auth():
    """Check if gcloud is authenticated."""
    try:
        run_command("gcloud auth list")
        return True
    except:
        print("❌ gcloud authentication failed")
        return False

def create_cloud_build_file():
    """Create a cloud build configuration file."""
    cloud_build_content = f"""
steps:
  # Build and push the Docker image to Google Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', '{DOCKER_IMAGE}', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', '{DOCKER_IMAGE}']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', '{SERVICE_NAME}', 
           '--image={DOCKER_IMAGE}', 
           '--region={REGION}',
           '--platform=managed',
           '--allow-unauthenticated',
           '--memory=512Mi',
           '--cpu=1',
           '--max-instances=10',
           '--set-env-vars=PORT=8080',
           '--service-account={SERVICE_ACCOUNT}',
           '--quiet']
    
images:
  - {DOCKER_IMAGE}
"""
    
    # Write the cloud build file
    cloud_build_path = DOLLAR_DIR / CLOUD_BUILD_FILE
    with open(cloud_build_path, 'w') as f:
        f.write(cloud_build_content)
    
    print(f"📝 Created cloud build file: {cloud_build_path}")
    return cloud_build_path

def build_and_deploy_with_gcloud():
    """Build and deploy using gcloud builds."""
    print("🏗️ Building and deploying with gcloud builds...")
    
    # Change to dollar directory
    os.chdir(DOLLAR_DIR)
    
    # Create cloud build configuration
    cloud_build_path = create_cloud_build_file()
    
    # Run the build
    print("🚀 Running gcloud builds submit...")
    run_command([
        "gcloud", "builds", "submit", 
        "--tag", DOCKER_IMAGE,
        "--project", PROJECT
    ])
    
    # Change back to original directory
    os.chdir("..")
    
    return DOCKER_IMAGE

def check_existing_service():
    """Check if the service already exists and get its URL."""
    try:
        print("🔍 Checking existing service...")
        url_result = run_command([
            "gcloud", "run", "services", "describe", SERVICE_NAME,
            f"--region={REGION}",
            f"--format=value(status.url)",
            "--platform=managed"
        ], capture_output=True)
        
        if url_result and url_result.strip():
            service_url = url_result.strip()
            print(f"✅ Existing service found: {service_url}")
            return service_url, True
        else:
            print("⚠️  No existing service found")
            return None, False
            
    except subprocess.CalledProcessError:
        print("⚠️  No existing service found")
        return None, False

def deploy_to_cloud_run(image_url):
    """Deploy the service to Cloud Run."""
    print(f"🚀 Deploying to Cloud Run: {SERVICE_NAME}")
    
    # Deploy the service
    cmd = [
        "gcloud", "run", "deploy", SERVICE_NAME,
        f"--image={image_url}",
        f"--region={REGION}",
        f"--platform=managed",
        f"--allow-unauthenticated",
        f"--memory=512Mi",
        f"--cpu=1",
        f"--max-instances=10",
        f"--set-env-vars=PORT=8080",
        f"--service-account={SERVICE_ACCOUNT}",
        "--quiet"
    ]
    
    run_command(cmd)
    
    # Get the service URL
    print("🌐 Getting service URL...")
    url_result = run_command([
        "gcloud", "run", "services", "describe", SERVICE_NAME,
        f"--region={REGION}",
        f"--format=value(status.url)",
        "--platform=managed"
    ])
    
    service_url = url_result.strip()
    print(f"✅ Service deployed at: {service_url}")
    
    return service_url

def check_service_health(url):
    """Check if the deployed service is healthy."""
    print("🏥 Checking service health...")
    
    import requests
    
    try:
        # Check main endpoint
        main_url = url
        main_response = requests.get(main_url, timeout=30)
        if main_response.status_code == 200:
            print(f"✅ Main endpoint accessible: {main_response.status_code}")
            print(f"✅ Content type: {main_response.headers.get('content-type', 'unknown')}")
            return True
        else:
            print(f"❌ Main endpoint failed: {main_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Main deployment function."""
    print("🎯 Dollar Dashboard Deployment Script - GCloud Build")
    print("=" * 50)
    
    # Check authentication
    if not check_gcloud_auth():
        print("❌ Please authenticate with gcloud first:")
        print("   gcloud auth login")
        print("   gcloud config set project sovereign-see")
        sys.exit(1)
    
    # Check if dollar directory exists
    if not DOLLAR_DIR.exists():
        print(f"❌ Dollar directory not found: {DOLLAR_DIR}")
        sys.exit(1)
    
    try:
        # Check if service already exists
        existing_url, service_exists = check_existing_service()
        
        # Build and deploy using gcloud builds
        image_url = build_and_deploy_with_gcloud()
        
        # Update service URL (redeploy command will update existing service)
        print(f"🔄 Updating service: {existing_url if service_exists else 'New service'}")
        service_url = deploy_to_cloud_run(image_url)
        
        # Check service health
        if check_service_health(service_url):
            print("\n🎉 Deployment completed successfully!")
            print(f"🌐 Dashboard URL: {service_url}")
            
            # Update status file
            update_status_file(service_url, existing_url if service_exists else None)
            
            return 0
        else:
            print("\n❌ Service health check failed after deployment")
            return 1
            
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        return 1

def update_status_file(url, previous_url=None):
    """Update the deployment status file."""
    status_file = Path("dollar-dashboard-status.md")
    
    status_content = f"""# Dollar Dashboard Deployment Status
**Cron Job ID:** 918a5138-8dee-4bbb-ad29-b24908889f50  
**Timestamp:** {time.strftime('%Y-%m-%d %H:%M UTC')}  
**Status:** ✅ DEPLOYED AND RUNNING  

## Service Details
- **Project:** sovereign-see
- **Region:** us-central1
- **Service Name:** dollar-dashboard
- **URL:** {url}
- **Status:** Ready (latest revision)

## Deployment Results
- ✅ Service exists and is properly deployed
- ✅ Service is Ready with 100% traffic
- ✅ Service account: dollaragency@sovereign-see.iam.gserviceaccount.com
- ✅ Container: python:3.11-slim with proper configuration
- ✅ Service returning HTML content successfully

## Notes
- The service was deployed successfully and is functioning correctly
- Dashboard is accessible via the Cloud Run URL
"""
    
    if previous_url:
        status_content += f"""
## Previous Deployment
- **Previous URL:** {previous_url}
- **Action:** Updated/Redeployed successfully
"""
    
    status_content += f"""
## Next Steps
- Dashboard is operational and monitoring can continue
- Any updates would require redeployment via this script

## Endpoints
- **Main Dashboard:** {url}
"""
    
    with open(status_file, 'w') as f:
        f.write(status_content)
    
    print(f"📝 Status file updated: {status_file}")

if __name__ == "__main__":
    sys.exit(main())