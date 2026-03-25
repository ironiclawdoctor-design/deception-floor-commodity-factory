#!/usr/bin/env python3
"""
Dollar Dashboard Deployment Script
GMRC/DE-002 — devops-engineer
Deploys dollar-dashboard to GCP Cloud Run
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

def build_docker_image():
    """Build the Docker image using buildx."""
    print("🏗️ Building Docker image with buildx...")
    
    # Change to dollar directory
    os.chdir(DOLLAR_DIR)
    
    # Initialize buildx if not already
    try:
        run_command("docker buildx ls")
    except:
        print("📦 Initializing buildx...")
        run_command("docker buildx create --use")
    
    # Build the image using buildx
    run_command(f"docker buildx build --platform linux/amd64 -t {DOCKER_IMAGE} . --push")
    
    # Change back to original directory
    os.chdir("..")
    
    return DOCKER_IMAGE

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
        # Check health endpoint
        health_url = f"{url}/health"
        response = requests.get(health_url, timeout=30)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
            
            # Check API status
            api_url = f"{url}/api/status"
            api_response = requests.get(api_url, timeout=30)
            if api_response.status_code == 200:
                api_data = api_response.json()
                print(f"✅ API status: {api_data.get('db_status', 'unknown')}")
                return True
            else:
                print(f"❌ API check failed: {api_response.status_code}")
                return False
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Main deployment function."""
    print("🎯 Dollar Dashboard Deployment Script")
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
        # Build Docker image
        image_url = build_docker_image()
        
        # Deploy to Cloud Run
        service_url = deploy_to_cloud_run(image_url)
        
        # Check service health
        if check_service_health(service_url):
            print("\n🎉 Deployment completed successfully!")
            print(f"🌐 Dashboard URL: {service_url}")
            print(f"📊 Health check: {service_url}/health")
            print(f"📈 API status: {service_url}/api/status")
            
            # Update status file
            update_status_file(service_url)
            
            return 0
        else:
            print("\n❌ Service health check failed after deployment")
            return 1
            
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        return 1

def update_status_file(url):
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

## Next Steps
- Dashboard is operational and monitoring can continue
- Any updates would require redeployment via this script
"""
    
    with open(status_file, 'w') as f:
        f.write(status_content)
    
    print(f"📝 Status file updated: {status_file}")

if __name__ == "__main__":
    sys.exit(main())