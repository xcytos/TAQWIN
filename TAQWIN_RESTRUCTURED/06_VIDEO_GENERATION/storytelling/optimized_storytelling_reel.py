#!/usr/bin/env python3
"""
ULTRA-OPTIMIZED ETHEREAL GLOW STORYTELLING REEL GENERATOR
Specifically designed for RTX 3050 Ti 4GB VRAM
Maximum memory efficiency with aggressive optimizations
"""

import torch
import gc
import os
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_video
import numpy as np
from pathlib import Path
import time

class UltraOptimizedStorytellingReel:
    def __init__(self):
        """Initialize with maximum memory efficiency"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.setup_directories()
        
    def setup_directories(self):
        """Create output directories"""
        self.output_dir = Path("ethereal_glow_optimized_reel")
        self.segments_dir = self.output_dir / "segments"
        
        self.output_dir.mkdir(exist_ok=True)
        self.segments_dir.mkdir(exist_ok=True)
        
    def aggressive_memory_cleanup(self):
        """Aggressive memory cleanup"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        gc.collect()
        
    def load_ultra_optimized_pipeline(self):
        """Load with maximum memory efficiency"""
        print("🚀 Loading ULTRA-OPTIMIZED Pipeline for RTX 3050 Ti...")
        
        try:
            self.aggressive_memory_cleanup()
            
            # Set environment variable for memory allocation
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
            
            adapter = MotionAdapter.from_pretrained(
                "guoyww/animatediff-motion-adapter-v1-5-2", 
                torch_dtype=torch.float16
            )
            
            self.pipe = AnimateDiffPipeline.from_pretrained(
                "emilianJR/epiCRealism",
                motion_adapter=adapter,
                torch_dtype=torch.float16,
                use_safetensors=True
            )
            
            # Maximum memory optimizations
            self.pipe.enable_attention_slicing(1)
            self.pipe.enable_sequential_cpu_offload()
            self.pipe.enable_vae_slicing()
            self.pipe.enable_vae_tiling()
            
            # Ultra-conservative memory settings
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)
                torch.cuda.set_per_process_memory_fraction(0.7)  # Even more conservative
            
            self.aggressive_memory_cleanup()
            
            print("✅ Ultra-Optimized Pipeline loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            return False
    
    def generate_ultra_optimized_segment(self, prompt, negative_prompt, duration_seconds=2, seed=None):
        """Generate segment with maximum memory efficiency"""
        if self.pipe is None:
            return None
            
        try:
            self.aggressive_memory_cleanup()
            
            # Ultra-conservative settings for RTX 3050 Ti
            num_frames = min(16, duration_seconds * 8)  # Lower frame rate
            generator = torch.manual_seed(seed if seed else int(time.time()))
            
            print(f"🎬 Generating {duration_seconds}s segment (ULTRA-OPTIMIZED)...")
            print(f"   📊 Resolution: 384x384, Frames: {num_frames}")
            
            # Generate with minimal memory usage
            video_frames = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                height=384,  # Lower resolution
                width=384,   # Lower resolution  
                num_frames=num_frames,
                guidance_scale=6.0,  # Lower guidance
                num_inference_steps=15,  # Fewer steps
                generator=generator
            ).frames[0]
            
            self.aggressive_memory_cleanup()
            
            print("✅ Segment generated successfully!")
            return video_frames
            
        except Exception as e:
            print(f"❌ Error generating segment: {e}")
            self.aggressive_memory_cleanup()
            return None
    
    def save_segment(self, video_frames, filename, fps=8):
        """Save video segment"""
        try:
            filepath = self.segments_dir / f"{filename}.mp4"
            export_to_video(video_frames, str(filepath), fps=fps)
            print(f"💾 Segment saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving segment: {e}")
            return None

    def create_optimized_storytelling_reel(self):
        """Create storytelling reel with ultra-optimization"""
        
        # SIMPLIFIED STORY SEGMENTS (5 segments instead of 9)
        story_segments = [
            {
                "name": "01_hook_and_problem",
                "duration": 3,
                "script": "Tired of harsh chemicals? Ancient beauty secrets await...",
                "prompt": "Beautiful Indian woman with natural skincare ingredients, turmeric, clay mask, traditional wooden bowls, warm golden lighting, serene expression",
                "negative_prompt": "synthetic products, plastic, harsh lighting, blurry, distorted",
                "seed": 100
            },
            {
                "name": "02_ethereal_glow_intro",
                "duration": 2,
                "script": "Ethereal Glow - Where tradition meets transformation",
                "prompt": "Ethereal Glow skincare jar, elegant glass container, golden cap, premium packaging, soft studio lighting, luxury beauty product",
                "negative_prompt": "cheap packaging, plastic, harsh lighting, blurry",
                "seed": 200
            },
            {
                "name": "03_application_demo",
                "duration": 3,
                "script": "Watch natural ingredients transform your skin",
                "prompt": "Gentle skincare application, natural face mask, smooth texture, hands applying cream, spa setting, soft movements, healthy skin",
                "negative_prompt": "harsh application, synthetic textures, aggressive movements, artificial",
                "seed": 300
            },
            {
                "name": "04_results_showcase",
                "duration": 2,
                "script": "Experience radiance from within",
                "prompt": "Woman with glowing healthy skin, confident smile, natural lighting, radiant complexion, peaceful expression, beauty portrait",
                "negative_prompt": "heavy makeup, artificial skin, harsh lighting, fake smile",
                "seed": 400
            },
            {
                "name": "05_brand_call_to_action",
                "duration": 2,
                "script": "Ethereal Glow - Your journey starts now",
                "prompt": "Ethereal Glow products display, premium arrangement, natural lighting, elegant presentation, brand showcase",
                "negative_prompt": "cluttered, poor lighting, cheap appearance, plastic",
                "seed": 500
            }
        ]
        
        print("🎯 Creating ULTRA-OPTIMIZED Storytelling Reel...")
        print("📖 Story: 'Ancient Wisdom Meets Modern Beauty'")
        print(f"📹 Total Segments: {len(story_segments)} (Optimized)")
        print(f"⏱️ Total Duration: {sum(seg['duration'] for seg in story_segments)} seconds")
        
        generated_segments = []
        
        for i, segment in enumerate(story_segments, 1):
            print(f"\n{'='*50}")
            print(f"📹 SEGMENT {i}/{len(story_segments)}: {segment['name']}")
            print(f"📝 Script: \"{segment['script']}\"")
            print(f"⏱️ Duration: {segment['duration']} seconds")
            
            # Generate segment with ultra-optimization
            frames = self.generate_ultra_optimized_segment(
                prompt=segment['prompt'],
                negative_prompt=segment['negative_prompt'],
                duration_seconds=segment['duration'],
                seed=segment['seed']
            )
            
            if frames:
                filepath = self.save_segment(frames, segment['name'])
                if filepath:
                    generated_segments.append({
                        'name': segment['name'],
                        'file': filepath,
                        'duration': segment['duration'],
                        'script': segment['script']
                    })
                    print(f"✅ Segment {i} completed successfully!")
                else:
                    print(f"❌ Failed to save segment {i}")
            else:
                print(f"❌ Failed to generate segment {i}")
                
            # Extended cooling pause
            print("🧊 Cooling GPU memory...")
            time.sleep(5)
            self.aggressive_memory_cleanup()
        
        return generated_segments

def main():
    """Main execution function"""
    print("🧠 ULTRA-OPTIMIZED ETHEREAL GLOW STORYTELLING REEL")
    print("=" * 60)
    print("🎬 Story: 'Ancient Wisdom Meets Modern Beauty'")
    print("⏱️ Total Duration: 12 seconds (5 optimized segments)")
    print("🎯 Ultra-Optimized for: RTX 3050 Ti 4GB VRAM")
    print("📊 Resolution: 384x384 (memory-efficient)")
    
    # Initialize generator
    generator = UltraOptimizedStorytellingReel()
    
    # Load pipeline
    if not generator.load_ultra_optimized_pipeline():
        print("❌ Failed to load ultra-optimized pipeline.")
        return
    
    # Check GPU memory
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"🔧 GPU Memory Available: {gpu_memory:.1f} GB")
        print("💡 Memory allocation: EXPANDABLE_SEGMENTS enabled")
    
    print("\n🎯 Ready to generate ultra-optimized storytelling reel!")
    print("⚠️  This will take approximately 15-20 minutes")
    
    proceed = input("\nProceed with ultra-optimized generation? (y/n): ").strip().lower()
    
    if proceed == 'y':
        segments = generator.create_optimized_storytelling_reel()
        
        if segments:
            print(f"\n🎉 SUCCESS! Generated {len(segments)} segments!")
            
            print("\n📁 Generated Segments:")
            total_duration = 0
            for segment in segments:
                print(f"   • {segment['name']}: {segment['duration']}s")
                print(f"     Script: \"{segment['script']}\"")
                total_duration += segment['duration']
            
            print(f"\n⏱️ Total Reel Duration: {total_duration} seconds")
            print(f"📂 All files saved in: {generator.segments_dir}")
            
            print("\n💡 Next Steps:")
            print("   1. Review generated segments")
            print("   2. Use video editing software to combine and upscale")
            print("   3. Add text overlays and music")
            print("   4. Export as final reel")
            
        else:
            print("❌ Generation failed. Try restarting and running again.")
    
    else:
        print("👍 Generation cancelled.")

if __name__ == "__main__":
    main()
