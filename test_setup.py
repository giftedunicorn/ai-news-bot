#!/usr/bin/env python3
"""
Test script to verify AI News Bot setup

This script checks that all required components are properly configured.
"""
import os
import sys
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (requires 3.8+)")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required = ["anthropic", "requests", "dotenv", "yaml"]
    all_installed = True

    for package in required:
        try:
            if package == "dotenv":
                __import__("dotenv")
            elif package == "yaml":
                __import__("yaml")
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (not installed)")
            all_installed = False

    return all_installed


def check_config_files():
    """Check if configuration files exist"""
    print("\nChecking configuration files...")
    files = {
        "config.yaml": "Configuration file",
        ".env": "Environment variables (optional)",
    }

    all_exist = True
    for filename, description in files.items():
        if Path(filename).exists():
            print(f"  ✓ {filename} - {description}")
        else:
            if filename == ".env":
                print(f"  ⚠ {filename} - {description} (not found, using environment)")
            else:
                print(f"  ✗ {filename} - {description} (not found)")
                all_exist = False

    return all_exist


def check_env_variables():
    """Check environment variables"""
    print("\nChecking environment variables...")

    # Try to load .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

    required = {
        "ANTHROPIC_API_KEY": "Anthropic API key (required)",
    }

    optional = {
        "NOTIFICATION_METHODS": "Notification methods",
        "SMTP_USER": "Email configuration",
        "WEBHOOK_URL": "Webhook configuration",
    }

    all_set = True

    print("\n  Required:")
    for var, description in required.items():
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"    ✓ {var} = {masked}")
        else:
            print(f"    ✗ {var} - {description} (not set)")
            all_set = False

    print("\n  Optional:")
    for var, description in optional.items():
        value = os.getenv(var)
        if value:
            if "URL" in var or "PASSWORD" in var:
                masked = "***"
            else:
                masked = value[:20] + "..." if len(value) > 20 else value
            print(f"    ✓ {var} = {masked}")
        else:
            print(f"    ⚠ {var} - {description} (not set)")

    return all_set


def check_project_structure():
    """Check project structure"""
    print("\nChecking project structure...")
    required_dirs = [
        "src",
        "src/notifiers",
    ]

    required_files = [
        "main.py",
        "src/__init__.py",
        "src/config.py",
        "src/logger.py",
        "src/news_generator.py",
        "src/notifiers/__init__.py",
        "src/notifiers/email_notifier.py",
        "src/notifiers/webhook_notifier.py",
    ]

    all_exist = True

    for directory in required_dirs:
        if Path(directory).is_dir():
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ (not found)")
            all_exist = False

    for filename in required_files:
        if Path(filename).is_file():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} (not found)")
            all_exist = False

    return all_exist


def main():
    """Run all checks"""
    print("=" * 60)
    print("AI News Bot - Setup Verification")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Configuration Files", check_config_files),
        ("Environment Variables", check_env_variables),
        ("Project Structure", check_project_structure),
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n  ✗ Error during {name} check: {str(e)}")
            results[name] = False

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")

    all_passed = all(results.values())

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Ensure ANTHROPIC_API_KEY is set")
        print("  2. Configure notification methods")
        print("  3. Run: python main.py")
    else:
        print("✗ Some checks failed. Please review the errors above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Copy .env.example to .env and fill in values")
        print("  - Ensure all source files are present")

    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
