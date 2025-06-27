#!/usr/bin/env python3
"""
AWS Deployment Script for Fire Whisper RPG
Handles Lambda deployment and AWS resource management
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Load environment variables
load_dotenv(project_root / ".env.local")

def check_aws_environment():
    """Check if AWS environment is properly configured"""
    required_vars = [
        "CLAUDE_API_KEY",
        "AWS_REGION", 
        "AWS_LAMBDA_FUNCTION_NAME"
    ]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required AWS environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    # Check AWS CLI
    try:
        result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ AWS CLI not found or not configured")
            return False
    except FileNotFoundError:
        print("❌ AWS CLI not installed")
        return False
    
    return True

def package_lambda():
    """Package the backend for Lambda deployment"""
    print("📦 Packaging Lambda function...")
    
    # Create deployment package
    deploy_dir = project_root / "aws_deploy"
    deploy_dir.mkdir(exist_ok=True)
    
    # Copy backend files
    import shutil
    backend_src = project_root / "backend"
    backend_dest = deploy_dir / "backend"
    
    if backend_dest.exists():
        shutil.rmtree(backend_dest)
    
    shutil.copytree(backend_src, backend_dest)
    
    # Install dependencies
    requirements_file = backend_dest / "requirements.txt"
    if requirements_file.exists():
        print("📥 Installing dependencies...")
        subprocess.run([
            "pip", "install", "-r", str(requirements_file), 
            "-t", str(deploy_dir)
        ], check=True)
    
    # Create deployment zip
    zip_file = project_root / "fire-whisper-lambda.zip"
    if zip_file.exists():
        zip_file.unlink()
    
    print("🗜️ Creating deployment package...")
    subprocess.run([
        "zip", "-r", str(zip_file), "."
    ], cwd=deploy_dir, check=True)
    
    print(f"✅ Lambda package created: {zip_file}")
    return zip_file

def deploy_lambda(zip_file):
    """Deploy Lambda function to AWS"""
    function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
    region = os.getenv("AWS_REGION")
    
    print(f"🚀 Deploying to AWS Lambda: {function_name}")
    
    # Check if function exists
    try:
        result = subprocess.run([
            "aws", "lambda", "get-function",
            "--function-name", function_name,
            "--region", region
        ], capture_output=True, text=True)
        
        function_exists = result.returncode == 0
    except:
        function_exists = False
    
    if function_exists:
        # Update existing function
        print("🔄 Updating existing Lambda function...")
        subprocess.run([
            "aws", "lambda", "update-function-code",
            "--function-name", function_name,
            "--zip-file", f"fileb://{zip_file}",
            "--region", region
        ], check=True)
    else:
        # Create new function
        print("🆕 Creating new Lambda function...")
        subprocess.run([
            "aws", "lambda", "create-function",
            "--function-name", function_name,
            "--runtime", "python3.9",
            "--role", f"arn:aws:iam::{get_aws_account_id()}:role/lambda-execution-role",
            "--handler", "backend.take_turn.lambda_handler",
            "--zip-file", f"fileb://{zip_file}",
            "--region", region,
            "--environment", f"Variables={{CLAUDE_API_KEY={os.getenv('CLAUDE_API_KEY')}}}"
        ], check=True)
    
    print("✅ Lambda deployment completed!")

def get_aws_account_id():
    """Get AWS account ID"""
    result = subprocess.run([
        "aws", "sts", "get-caller-identity",
        "--query", "Account",
        "--output", "text"
    ], capture_output=True, text=True)
    
    return result.stdout.strip()

def deploy_infrastructure():
    """Deploy AWS infrastructure using CloudFormation"""
    template_file = project_root / "template.yaml"
    
    if not template_file.exists():
        print("⚠️ CloudFormation template not found, skipping infrastructure deployment")
        return
    
    stack_name = "fire-whisper-game-stack"
    region = os.getenv("AWS_REGION")
    
    print(f"🏗️ Deploying infrastructure stack: {stack_name}")
    
    try:
        subprocess.run([
            "aws", "cloudformation", "deploy",
            "--template-file", str(template_file),
            "--stack-name", stack_name,
            "--capabilities", "CAPABILITY_IAM",
            "--region", region,
            "--parameter-overrides",
            f"ClaudeApiKey={os.getenv('CLAUDE_API_KEY')}"
        ], check=True)
        
        print("✅ Infrastructure deployment completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Infrastructure deployment failed: {e}")

def get_version():
    """Get current version"""
    try:
        with open(project_root / "version.json", 'r') as f:
            version_data = json.load(f)
        return version_data.get("version", "unknown")
    except:
        return "unknown"

def main():
    """Main deployment function"""
    print("🔥 Fire Whisper RPG - AWS Deployment")
    print("=" * 40)
    print(f"🏷️  Version: {get_version()}")
    print(f"🌍 Region: {os.getenv('AWS_REGION', 'not set')}")
    print(f"⚡ Function: {os.getenv('AWS_LAMBDA_FUNCTION_NAME', 'not set')}")
    print("=" * 40)
    
    if not check_aws_environment():
        print("\n💡 Configure your AWS environment in .env.local")
        return
    
    try:
        # Package Lambda
        zip_file = package_lambda()
        
        # Deploy infrastructure (optional)
        deploy_infrastructure()
        
        # Deploy Lambda
        deploy_lambda(zip_file)
        
        print("\n🎉 AWS deployment completed successfully!")
        print(f"🔗 Your Lambda function is ready: {os.getenv('AWS_LAMBDA_FUNCTION_NAME')}")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()