#!/usr/bin/env python3
# Quick Test - CPU Optimized
import torch
from diffusers import StableDiffusionPipeline
import os

def quick_cpu_test():
    print("🧪 Quick CPU Test - Ethereal Glow AI System")
    print("="*50)
    
    print("🔍 System Info:")
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    
    try:
        print("\n📥 Loading lightweight model for CPU...")
        
        # Use smaller, CPU-friendly model
        model_id = "runwayml/stable-diffusion-v1-5"
        
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,  # CPU uses float32
            use_safetensors=True
        )
        
        # CPU optimizations
        pipe.safety_checker = None  # Disable safety checker to save memory
        pipe.requires_safety_checker = False
        
        print("✅ Model loaded successfully!")
        
        # Quick test generation
        print("\n🎨 Generating test image...")
        prompt = "Beautiful glowing skin, luxury skincare, professional photography"
        
        image = pipe(
            prompt,
            width=256,  # Smaller size for CPU
            height=256,
            num_inference_steps=10,  # Fewer steps for speed
            guidance_scale=7.5
        ).images[0]
        
        # Save test image
        os.makedirs("test_output", exist_ok=True)
        image.save("test_output/cpu_test.png")
        
        print("✅ Test image generated successfully!")
        print("📁 Saved: test_output/cpu_test.png")
        print("\n🎉 CPU-based AI image generation is WORKING!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 This may be due to model download or memory constraints")
        return False

if __name__ == "__main__":
    quick_cpu_test()
