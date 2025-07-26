#!/usr/bin/env python3
"""
HIGH QUALITY 10-SECOND ETHEREAL GLOW VIDEO GENERATOR
Optimized for RTX 3050 Ti + Shared GPU Memory
Maximum quality settings for premium content
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

class HighQuality10SecGenerator:
    def __init__(self):
        """Initialize high quality generator with shared memory optimization"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.setup_directories()
        
    def setup_directories(self):
        """Create output directories"""
        self.output_dir = Path("ethereal_glow_10sec_premium")
        self.output_dir.mkdir(exist_ok=True)
        print(f"📁 Output directory: {self.output_dir}")
        
    def check_system_memory(self):
        """Check system and GPU memory"""
        if torch.cuda.is_available():
            gpu_props = torch.cuda.get_device_properties(0)
            gpu_memory_gb = gpu_props.total_memory / 1024**3
            gpu_free = torch.cuda.memory_reserved(0) / 1024**3
            
            print(f"🔧 GPU: {gpu_props.name}")
            print(f"💾 GPU Memory: {gpu_memory_gb:.1f} GB total")
            print(f"🆓 GPU Free: {gpu_free:.1f} GB")
        
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
        """Load pipeline with maximum quality settings"""
        print("🚀 Loading HIGH QUALITY Pipeline with Shared Memory Optimization...")
        
        try:
            self.extreme_memory_optimization()
            
            # Enable maximum memory utilization
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True,roundup_power2_divisions:False'
            
            # Load motion adapter
            print("📥 Loading Motion Adapter...")
            adapter = MotionAdapter.from_pretrained(
                "guoyww/animatediff-motion-adapter-v1-5-2", 
                torch_dtype=torch.float16,
                variant="fp16" if torch.cuda.is_available() else None
            )
            
            # Load main pipeline
            print("📥 Loading AnimateDiff Pipeline...")
            self.pipe = AnimateDiffPipeline.from_pretrained(
                "emilianJR/epiCRealism",
                motion_adapter=adapter,
                torch_dtype=torch.float16,
                use_safetensors=True,
                variant="fp16" if torch.cuda.is_available() else None
            )
            
            # Apply quality-focused optimizations
            print("⚙️ Applying quality optimizations...")
            self.pipe.enable_attention_slicing(1)  # Memory efficiency
            self.pipe.enable_sequential_cpu_offload()  # CPU offloading
            self.pipe.enable_vae_slicing()  # VAE memory optimization
            self.pipe.enable_vae_tiling()  # VAE tiling for large images
            
            # GPU memory settings for shared memory utilization
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)  # Flash attention
                torch.cuda.set_per_process_memory_fraction(0.95)  # Use 95% of available VRAM
                
                # Enable memory pool for better allocation
                torch.cuda.empty_cache()
            
            self.extreme_memory_optimization()
            
            print("✅ HIGH QUALITY Pipeline loaded successfully!")
            print("🎯 Ready for premium 10-second video generation!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            return False
    
    def generate_10sec_premium_video(self, prompt, negative_prompt, filename="ethereal_glow_10sec", seed=42):
        """Generate 10-second premium quality video"""
        if self.pipe is None:
            print("❌ Pipeline not loaded!")
            return None
            
        try:
            self.extreme_memory_optimization()
            
            # Premium settings for 10-second video
            duration_seconds = 10
            fps = 8  # 8 FPS for smooth motion
            num_frames = duration_seconds * fps  # 80 frames for 10 seconds
            
            # Set seed for reproducibility
            generator = torch.manual_seed(seed)
            
            print(f"\n🎬 GENERATING 10-SECOND PREMIUM VIDEO")
            print(f"{'='*50}")
            print(f"📝 Filename: {filename}")
            print(f"📊 Resolution: 768x768 (High Quality)")
            print(f"🎞️ Frames: {num_frames}")
            print(f"⏱️ Duration: {duration_seconds} seconds")
            print(f"🎯 FPS: {fps}")
            print(f"🌟 Quality: MAXIMUM")
            print(f"📝 Prompt: {prompt[:100]}...")
            
            # Start generation with premium settings
            print(f"\n🚀 Starting generation... (This may take 5-10 minutes)")
            start_time = time.time()
            
            video_frames = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                height=768,  # Higher resolution for premium quality
                width=768,   # Higher resolution for premium quality
                num_frames=num_frames,
                guidance_scale=9.0,  # Higher guidance for better prompt adherence
                num_inference_steps=35,  # More steps for superior quality
                generator=generator,
                cross_attention_kwargs={"scale": 1.0}  # Full attention for quality
            ).frames[0]
            
            generation_time = time.time() - start_time
            print(f"✅ Generation completed in {generation_time:.1f} seconds!")
            
            self.extreme_memory_optimization()
            
            # Save with high quality settings
            print("💾 Saving premium video...")
            filepath = self.output_dir / f"{filename}.mp4"
            export_to_video(video_frames, str(filepath), fps=fps)
            
            print(f"🎉 SUCCESS! Premium 10-second video saved: {filepath}")
            print(f"📊 File size: {filepath.stat().st_size / 1024 / 1024:.1f} MB")
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            print("💡 Try reducing resolution or frame count if memory issues persist")
            self.extreme_memory_optimization()
            return None

def main():
    """Main execution function"""
    print("🧠 ETHEREAL GLOW HIGH QUALITY 10-SECOND VIDEO GENERATOR")
    print("="*65)
    print("🎯 Focus: MAXIMUM QUALITY 10-second content")
    print("💾 Memory: Shared GPU + System RAM optimization")
    print("📊 Resolution: 768x768 (Premium Quality)")
    print("🎞️ Duration: 10 seconds (80 frames)")
    
    # Initialize generator
    generator = HighQuality10SecGenerator()
    
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
            "name": "ethereal_glow_brand_story_10sec",
            "prompt": "Cinematic brand story of Ethereal Glow organic skincare, elegant Indian woman applying traditional multani mitti clay mask in serene spa environment, golden hour lighting filtering through windows, slow motion product application, natural ingredients floating artistically, premium glass jar with golden cap prominently displayed, soft focus transitions, luxury beauty commercial cinematography, warm earthy tones, professional studio quality",
            "negative_prompt": "low quality, blurry, pixelated, harsh lighting, cheap packaging, plastic materials, artificial colors, fast movements, amateur photography, noise, artifacts, distorted faces, poor composition, over-saturated"
        },
        "2": {
            "name": "ingredients_to_results_10sec", 
            "prompt": "Premium transformation sequence showing natural organic ingredients morphing into glowing healthy skin, turmeric powder and multani mitti clay arranged in elegant wooden bowls, macro photography of textures, beautiful woman's face with radiant complexion, before and after skincare results, cinematic lighting transitions, professional beauty commercial, golden natural tones, high-end spa atmosphere, smooth morphing effects",
            "negative_prompt": "artificial transitions, harsh cuts, poor lighting, low resolution, fake results, plastic surgery appearance, heavy makeup, unnatural skin, cheap ingredients, poor composition"
        },
        "3": {
            "name": "ethereal_glow_product_showcase_10sec",
            "prompt": "Luxury product showcase of complete Ethereal Glow skincare line, three premium glass jars arranged on natural stone surface, soft directional lighting creating elegant shadows, slow rotating camera movement, golden caps gleaming, natural ingredients artistically placed around products, premium packaging details visible, commercial beauty photography, warm golden tones, professional studio setup, macro lens details",
            "negative_prompt": "cheap appearance, plastic packaging, harsh shadows, poor lighting, blurry details, amateur photography, cluttered composition, artificial materials, over-bright lighting"
        }
    }
    
    print(f"\n🎬 PREMIUM 10-SECOND VIDEO OPTIONS:")
    for key, prompt in premium_prompts.items():
        print(f"   {key}. {prompt['name']}")
    
    choice = input(f"\nSelect video to generate (1-3): ").strip()
    
    if choice in premium_prompts:
        selected = premium_prompts[choice]
        print(f"\n🎯 Selected: {selected['name']}")
        print("⚠️ This will take 5-10 minutes for premium quality generation")
        
        proceed = input("\nProceed with high-quality generation? (y/n): ").strip().lower()
        
        if proceed == 'y':
            filepath = generator.generate_10sec_premium_video(
                prompt=selected['prompt'],
                negative_prompt=selected['negative_prompt'],
                filename=selected['name']
            )
            
            if filepath:
                print(f"\n🎉 SUCCESS! Premium 10-second video created!")
                print(f"📁 Location: {filepath}")
                print(f"\n💡 Next Steps:")
                print("   1. Review the video quality")
                print("   2. Add professional text overlays if needed")
                print("   3. Add background music")
                print("   4. Export in your preferred format")
                print("   5. Deploy across social media platforms")
                
                # Show file info
                if filepath.exists():
                    file_size = filepath.stat().st_size / 1024 / 1024
                    print(f"📊 File Details: {file_size:.1f} MB, 10 seconds, 768x768 resolution")
            else:
                print("❌ Generation failed. Check GPU memory and try again.")
        else:
            print("👍 Generation cancelled.")
    else:
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()
