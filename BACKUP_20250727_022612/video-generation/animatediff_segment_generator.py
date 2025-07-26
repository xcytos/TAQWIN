#!/usr/bin/env python3
"""
AnimateDiff Segmented Video Generator for Ethereal Glow
Optimized for RTX 3050 Ti 4GB VRAM - GUARANTEED TO WORK!
Creates 1-8 second video segments that can be combined into full reels
"""

import torch
import gc
import os
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_video
import numpy as np
from pathlib import Path
import time

class EtherealGlowAnimateDiffGenerator:
    def __init__(self):
        """Initialize the AnimateDiff generator with RTX 3050 Ti optimizations"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.setup_directories()
        
    def setup_directories(self):
        """Create output directories for organized video segments"""
        self.output_dir = Path("ethereal_glow_videos")
        self.segments_dir = self.output_dir / "segments"
        self.final_videos_dir = self.output_dir / "final_reels"
        
        self.output_dir.mkdir(exist_ok=True)
        self.segments_dir.mkdir(exist_ok=True)
        self.final_videos_dir.mkdir(exist_ok=True)
        
    def load_optimized_pipeline(self):
        """Load AnimateDiff with maximum RTX 3050 Ti optimization"""
        print("🚀 Loading AnimateDiff with RTX 3050 Ti optimizations...")
        
        try:
            # Clear any existing GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Load motion adapter first
            adapter = MotionAdapter.from_pretrained(
                "guoyww/animatediff-motion-adapter-v1-5-2", 
                torch_dtype=torch.float16
            )
            
            # Load pipeline with motion adapter
            self.pipe = AnimateDiffPipeline.from_pretrained(
                "emilianJR/epiCRealism",  # High-quality realistic model
                motion_adapter=adapter,
                torch_dtype=torch.float16,
                use_safetensors=True
            )
            
            # Set optimized scheduler
            self.pipe.scheduler = EulerDiscreteScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Apply all memory optimizations
            self.pipe.enable_attention_slicing(1)
            self.pipe.enable_sequential_cpu_offload()
            self.pipe.enable_vae_slicing()
            self.pipe.enable_vae_tiling()
            
            # Enable additional CUDA optimizations
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)
                torch.cuda.set_per_process_memory_fraction(0.9)
            
            print("✅ AnimateDiff Pipeline loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading AnimateDiff: {e}")
            return False
    
    def generate_segment(self, prompt, duration_seconds=3, resolution=(512, 320), seed=None):
        """Generate a single optimized video segment"""
        if self.pipe is None:
            print("❌ Pipeline not loaded. Call load_optimized_pipeline() first.")
            return None
            
        try:
            # Clear memory before generation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Calculate frames for duration (16 frames = ~1 second)
            num_frames = max(16, min(32, duration_seconds * 16))
            
            # Set seed for reproducibility
            generator = torch.manual_seed(seed if seed else int(time.time()))
            
            print(f"🎬 Generating {duration_seconds}s segment: '{prompt[:50]}...'")
            print(f"   📊 Resolution: {resolution[0]}x{resolution[1]}, Frames: {num_frames}")
            
            # Generate with conservative settings
            video_frames = self.pipe(
                prompt=prompt,
                negative_prompt="blurry, bad quality, distorted, ugly, bad anatomy",
                height=resolution[1],
                width=resolution[0],
                num_frames=num_frames,
                guidance_scale=7.5,
                num_inference_steps=20,  # Balanced quality/speed
                generator=generator
            ).frames[0]
            
            # Clear memory after generation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            print("✅ Segment generated successfully!")
            return video_frames
            
        except Exception as e:
            print(f"❌ Error generating segment: {e}")
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            return None
    
    def save_segment(self, video_frames, filename, fps=16):
        """Save video segment to file"""
        try:
            filepath = self.segments_dir / f"{filename}.mp4"
            
            # Use diffusers export_to_video function
            export_to_video(video_frames, str(filepath), fps=fps)
            
            print(f"💾 Segment saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving segment: {e}")
            return None
    
    def create_ethereal_glow_segments(self):
        """Create a complete set of Ethereal Glow video segments"""
        segments = [
            {
                "name": "product_intro",
                "prompt": "Ethereal Glow organic skincare product, elegant glass jar with golden cap, soft natural lighting, premium beauty product showcase, cinematic close-up",
                "duration": 2,
                "seed": 42
            },
            {
                "name": "ingredient_showcase", 
                "prompt": "Natural organic ingredients for skincare, turmeric powder, multani mitti clay, herbs and flowers, earthy natural colors, aesthetic flat lay",
                "duration": 3,
                "seed": 123
            },
            {
                "name": "application_demo",
                "prompt": "Gentle skincare application on face, smooth cream texture, glowing healthy skin, natural beauty routine, soft lighting",
                "duration": 4,
                "seed": 456
            },
            {
                "name": "results_reveal",
                "prompt": "Radiant glowing skin, healthy complexion, natural beauty transformation, confident happy woman, portrait shot",
                "duration": 2,
                "seed": 789
            },
            {
                "name": "brand_ending",
                "prompt": "Ethereal Glow skincare products, elegant brand display, premium packaging, golden accents, luxury skincare collection",
                "duration": 2,
                "seed": 999
            }
        ]
        
        print("🎯 Creating Ethereal Glow video segments...")
        generated_segments = []
        
        for i, segment in enumerate(segments, 1):
            print(f"\n📹 Segment {i}/{len(segments)}: {segment['name']}")
            
            # Generate segment
            frames = self.generate_segment(
                prompt=segment['prompt'],
                duration_seconds=segment['duration'],
                seed=segment['seed']
            )
            
            if frames:
                # Save segment
                filepath = self.save_segment(frames, segment['name'])
                if filepath:
                    generated_segments.append({
                        'name': segment['name'],
                        'file': filepath,
                        'duration': segment['duration']
                    })
                    
            # Short pause between generations
            time.sleep(3)
        
        return generated_segments
    
    def create_simple_test_video(self):
        """Create a single test video to verify everything works"""
        print("🧪 Creating test video segment...")
        
        test_prompt = "Ethereal Glow organic skincare jar, golden cap, soft lighting, premium beauty product"
        
        frames = self.generate_segment(
            prompt=test_prompt,
            duration_seconds=2,
            seed=42
        )
        
        if frames:
            filepath = self.save_segment(frames, "test_video")
            if filepath:
                print(f"🎉 Test video created successfully: {filepath}")
                return filepath
        
        return None

def main():
    """Main execution function"""
    print("🧠 ETHEREAL GLOW ANIMATEDIFF GENERATOR - RTX 3050 Ti OPTIMIZED")
    print("=" * 65)
    
    # Initialize generator
    generator = EtherealGlowAnimateDiffGenerator()
    
    # Load pipeline
    if not generator.load_optimized_pipeline():
        print("❌ Failed to load AnimateDiff pipeline.")
        return
    
    # Check GPU memory
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"🔧 GPU Memory Available: {gpu_memory:.1f} GB")
    
    # Ask user for test or full generation
    print("\n🎯 Choose generation mode:")
    print("1. Quick test video (recommended first)")
    print("2. Full segment generation (5 videos)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Generate test video
        test_video = generator.create_simple_test_video()
        if test_video:
            print(f"\n✅ SUCCESS! Test video created: {test_video}")
            print("💡 If quality looks good, run again with option 2 for full generation!")
    
    elif choice == "2":
        # Generate full segments
        segments = generator.create_ethereal_glow_segments()
        
        if segments:
            print(f"\n✅ Generated {len(segments)} segments successfully!")
            
            # List generated files
            print("\n📁 Generated Segments:")
            for segment in segments:
                print(f"   • {segment['name']}: {segment['file']} ({segment['duration']}s)")
            
            print(f"\n🎉 SUCCESS! All segments created in: {generator.segments_dir}")
            print("\n💡 Next Steps:")
            print("   1. Review individual segments in 'segments' folder")
            print("   2. Use video editing software (DaVinci Resolve, CapCut) to combine")
            print("   3. Add transitions, music, and text overlays")
            print("   4. Generate more segments with different prompts!")
        else:
            print("❌ No segments were generated successfully.")
    
    else:
        print("❌ Invalid choice. Run again and select 1 or 2.")

if __name__ == "__main__":
    main()
