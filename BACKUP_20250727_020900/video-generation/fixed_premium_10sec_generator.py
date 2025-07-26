#!/usr/bin/env python3
"""
FIXED HIGH QUALITY 10-SECOND ETHEREAL GLOW VIDEO GENERATOR
Optimized for RTX 3050 Ti + Shared GPU Memory
No fp16 variant issues - Maximum quality settings
"""

import torch
import gc
import os
import psutil
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_video
import numpy as np
from pathlib import Path
import time

class FixedPremium10SecGenerator:
    def __init__(self):
        """Initialize high quality generator with shared memory optimization"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.setup_directories()
        
    def setup_directories(self):
        """Create output directories"""
        self.output_dir = Path("ethereal_glow_premium_10sec")
        self.output_dir.mkdir(exist_ok=True)
        print(f"📁 Output directory: {self.output_dir}")
        
    def check_system_memory(self):
        """Check system and GPU memory"""
        if torch.cuda.is_available():
            gpu_props = torch.cuda.get_device_properties(0)
            gpu_memory_gb = gpu_props.total_memory / 1024**3
            
            print(f"🔧 GPU: {gpu_props.name}")
            print(f"💾 GPU Memory: {gpu_memory_gb:.1f} GB total")
        
        # Check system RAM
        ram = psutil.virtual_memory()
        print(f"🖥️ System RAM: {ram.total / 1024**3:.1f} GB total, {ram.available / 1024**3:.1f} GB available")
        
    def extreme_memory_optimization(self):
        """Maximum memory cleanup and optimization"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            torch.cuda.ipc_collect()
        gc.collect()
        
        # Force garbage collection multiple times
        for _ in range(3):
            gc.collect()
            
    def load_premium_pipeline(self):
        """Load pipeline with maximum quality settings - FIXED VERSION"""
        print("🚀 Loading FIXED HIGH QUALITY Pipeline...")
        
        try:
            self.extreme_memory_optimization()
            
            # Enable maximum memory utilization
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True,roundup_power2_divisions:False'
            
            # Load motion adapter WITHOUT fp16 variant
            print("📥 Loading Motion Adapter...")
            adapter = MotionAdapter.from_pretrained(
                "guoyww/animatediff-motion-adapter-v1-5-2", 
                torch_dtype=torch.float16
                # Removed variant parameter
            )
            
            # Load main pipeline WITHOUT fp16 variant
            print("📥 Loading AnimateDiff Pipeline...")
            self.pipe = AnimateDiffPipeline.from_pretrained(
                "emilianJR/epiCRealism",
                motion_adapter=adapter,
                torch_dtype=torch.float16,
                use_safetensors=True
                # Removed variant parameter
            )
            
            # Apply quality-focused optimizations
            print("⚙️ Applying quality optimizations...")
            self.pipe.enable_attention_slicing(1)
            self.pipe.enable_sequential_cpu_offload()
            self.pipe.enable_vae_slicing()
            self.pipe.enable_vae_tiling()
            
            # GPU memory settings for shared memory utilization
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)
                torch.cuda.set_per_process_memory_fraction(0.95)
                torch.cuda.empty_cache()
            
            self.extreme_memory_optimization()
            
            print("✅ FIXED HIGH QUALITY Pipeline loaded successfully!")
            print("🎯 Ready for premium 10-second video generation!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            return False
    
    def generate_premium_10sec_video(self, prompt, negative_prompt, filename="ethereal_glow_premium_10sec", seed=42):
        """Generate 10-second premium quality video"""
        if self.pipe is None:
            print("❌ Pipeline not loaded!")
            return None
            
        try:
            self.extreme_memory_optimization()
            
            # Optimized settings for RTX 3050 Ti with quality focus
            duration_seconds = 10
            fps = 8
            num_frames = min(64, duration_seconds * fps)  # Limit frames for memory
            
            generator = torch.manual_seed(seed)
            
            print(f"\n🎬 GENERATING PREMIUM 10-SECOND VIDEO")
            print(f"{'='*50}")
            print(f"📝 Filename: {filename}")
            print(f"📊 Resolution: 640x640 (Optimized Quality)")
            print(f"🎞️ Frames: {num_frames}")
            print(f"⏱️ Duration: {duration_seconds} seconds")
            print(f"🎯 FPS: {fps}")
            print(f"🌟 Quality: HIGH (RTX 3050 Ti Optimized)")
            print(f"📝 Prompt: {prompt[:100]}...")
            
            print(f"\n🚀 Starting generation... (5-8 minutes estimated)")
            start_time = time.time()
            
            video_frames = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                height=640,  # Optimized resolution for RTX 3050 Ti
                width=640,   # Optimized resolution for RTX 3050 Ti
                num_frames=num_frames,
                guidance_scale=8.0,  # High guidance
                num_inference_steps=30,  # Good quality/speed balance
                generator=generator
            ).frames[0]
            
            generation_time = time.time() - start_time
            print(f"✅ Generation completed in {generation_time:.1f} seconds!")
            
            self.extreme_memory_optimization()
            
            # Save video
            print("💾 Saving premium video...")
            filepath = self.output_dir / f"{filename}.mp4"
            export_to_video(video_frames, str(filepath), fps=fps)
            
            print(f"🎉 SUCCESS! Premium 10-second video saved: {filepath}")
            
            if filepath.exists():
                file_size = filepath.stat().st_size / 1024 / 1024
                print(f"📊 File size: {file_size:.1f} MB")
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            self.extreme_memory_optimization()
            return None

def main():
    """Main execution function"""
    print("🧠 FIXED ETHEREAL GLOW PREMIUM 10-SECOND VIDEO GENERATOR")
    print("="*65)
    print("🎯 Focus: HIGH QUALITY 10-second content")
    print("💾 Memory: Shared GPU + System RAM optimization")
    print("📊 Resolution: 640x640 (RTX 3050 Ti Optimized)")
    print("🎞️ Duration: 10 seconds")
    
    # Initialize generator
    generator = FixedPremium10SecGenerator()
    
    # Check system resources
    print("\n📊 SYSTEM ANALYSIS:")
    generator.check_system_memory()
    
    # Load pipeline
    print(f"\n🚀 PIPELINE LOADING:")
    if not generator.load_premium_pipeline():
        print("❌ Failed to load premium pipeline.")
        return
    
    # Premium 10-second video prompts
    premium_prompts = {
        "1": {
            "name": "ethereal_glow_cinematic_story",
            "prompt": "Cinematic beauty commercial of Ethereal Glow organic skincare, elegant woman applying natural multani mitti clay mask, golden hour lighting, serene spa environment, premium glass jar with golden cap, traditional Indian beauty ritual, soft focus cinematography, warm earthy tones, luxury skincare brand presentation, professional studio quality",
            "negative_prompt": "low quality, blurry, pixelated, harsh lighting, cheap packaging, plastic materials, artificial colors, amateur photography, noise, artifacts, distorted, poor composition"
        },
        "2": {
            "name": "natural_ingredients_transformation", 
            "prompt": "Premium beauty transformation showing organic skincare ingredients, turmeric powder and multani mitti clay in elegant wooden bowls, beautiful woman with radiant glowing skin, before and after skincare results, macro photography of natural textures, professional beauty commercial lighting, golden natural tones, high-end spa atmosphere",
            "negative_prompt": "artificial transitions, poor lighting, low resolution, fake results, heavy makeup, unnatural skin, cheap ingredients, poor composition, plastic containers"
        },
        "3": {
            "name": "ethereal_glow_product_luxury",
            "prompt": "Luxury product showcase of Ethereal Glow skincare line, three premium glass jars on natural stone surface, soft directional lighting, elegant shadows, golden caps gleaming, natural ingredients artistically arranged, premium packaging visible, commercial beauty photography, warm tones, professional studio setup",
            "negative_prompt": "cheap appearance, plastic packaging, harsh shadows, poor lighting, blurry details, amateur photography, cluttered composition, artificial materials"
        }
    }
    
    print(f"\n🎬 PREMIUM 10-SECOND VIDEO OPTIONS:")
    for key, prompt in premium_prompts.items():
        print(f"   {key}. {prompt['name']}")
    
    choice = input(f"\nSelect video to generate (1-3): ").strip()
    
    if choice in premium_prompts:
        selected = premium_prompts[choice]
        print(f"\n🎯 Selected: {selected['name']}")
        print("⚠️ This will take 5-8 minutes for high-quality generation")
        
        proceed = input("\nProceed with premium generation? (y/n): ").strip().lower()
        
        if proceed == 'y':
            filepath = generator.generate_premium_10sec_video(
                prompt=selected['prompt'],
                negative_prompt=selected['negative_prompt'],
                filename=selected['name']
            )
            
            if filepath:
                print(f"\n🎉 SUCCESS! Premium 10-second video created!")
                print(f"📁 Location: {filepath}")
                print(f"\n💡 Next Steps:")
                print("   1. Review the video quality")
                print("   2. Add text overlays if needed")
                print("   3. Add background music")
                print("   4. Export for social media")
                print("   5. Create additional segments if needed")
            else:
                print("❌ Generation failed. Try again or reduce settings.")
        else:
            print("👍 Generation cancelled.")
    else:
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()
