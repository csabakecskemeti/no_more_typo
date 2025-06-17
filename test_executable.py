#!/usr/bin/env python3
"""
Quick test script to verify the executable works
"""

import subprocess
import time
import os

def test_executable():
    """Test that the executable starts and imports work correctly."""
    print("🧪 Testing Standalone Executable")
    print("=" * 40)
    
    # Check if executable exists
    exe_path = "dist/no_more_typo"
    if not os.path.exists(exe_path):
        print("❌ Executable not found at dist/no_more_typo")
        return False
    
    print(f"✅ Executable found: {exe_path}")
    
    # Get file size
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"📦 Size: {size_mb:.1f} MB")
    
    # Test that it can be executed (will show startup screen)
    print("\n🚀 Testing executable startup...")
    print("Note: This will show the startup screen and then we'll stop it")
    print("-" * 40)
    
    try:
        # Start the process
        process = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a few seconds to start and show output
        time.sleep(3)
        
        # Terminate the process
        process.terminate()
        
        # Get output
        stdout, stderr = process.communicate(timeout=5)
        
        print("STDOUT:")
        print(stdout[:1000] + "..." if len(stdout) > 1000 else stdout)
        
        if stderr:
            print("\nSTDERR:")
            print(stderr[:500] + "..." if len(stderr) > 500 else stderr)
        
        # Check if it started properly
        if "Enhanced processor ready" in stdout or "no_more_typo" in stdout:
            print("\n✅ Executable started successfully!")
            print("   The application appears to be working correctly.")
            return True
        else:
            print("\n⚠️  Executable started but output unexpected")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Process took too long to respond")
        process.kill()
        return False
    except Exception as e:
        print(f"❌ Error testing executable: {e}")
        return False

def create_release_info():
    """Create release information."""
    print("\n📋 Creating Release Information")
    print("=" * 40)
    
    exe_path = "dist/no_more_typo"
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    
    release_info = f"""# no_more_typo - Standalone Release

## Download
- **File**: `no_more_typo` 
- **Size**: {size_mb:.1f} MB
- **Platform**: macOS (ARM64)

## Quick Start
1. Download the `no_more_typo` executable
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. Run the executable:
   ```bash
   ./no_more_typo
   ```
4. Use Ctrl+Shift+Z to process clipboard content
5. Use Ctrl+Shift+X to exit

## Command Examples
- `"Hello world <#translate to spanish>"` → Translation
- `"def func(): pass <#complete>"` → Code completion  
- `"Complex topic <#explain simply>"` → Simple explanation
- `"Buggy code <#fix errors>"` → Fix issues
- `"Regular text"` → Typo fixing (backward compatible)

## Requirements
- macOS (tested on macOS 15.5+)
- OpenAI API key
- No Python installation required!

## Notes
- The executable is self-contained with all dependencies
- First run may take a few seconds to initialize
- Console output shows processing status and examples
"""
    
    with open("RELEASE_INFO.md", "w") as f:
        f.write(release_info)
    
    print("✅ Created RELEASE_INFO.md")
    print("\n📦 Release Ready!")
    print(f"   Executable: dist/no_more_typo ({size_mb:.1f} MB)")
    print("   Documentation: RELEASE_INFO.md")

if __name__ == "__main__":
    success = test_executable()
    if success:
        create_release_info()
        print("\n🎉 Executable is ready for distribution!")
    else:
        print("\n❌ Executable needs investigation")