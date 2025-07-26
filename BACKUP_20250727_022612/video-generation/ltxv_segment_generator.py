#!/usr/bin/env python3
"""
LTXV Segmented Video Generator for Ethereal Glow
Optimized for RTX 3050 Ti 4GB VRAM
Creates 1-8 second video segments that can be combined into full reels
"""

import torch
import gc
import os
from diffusers import LTXPipeline
import imageio
import numpy as np
from pathlib import Path
import time

class EtherealGlowLTXVGenerator:
    def __init__(self):
        """Initialize the LTXV generator with RTX 3050 Ti optimizations"""
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
        """Load LTXV with maximum RTX 3050 Ti optimization"""
        print("🚀 Loading LTXV with RTX 3050 Ti optimizations...")
        
        try:
            # Clear any existing GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Load with maximum memory optimization
            self.pipe = LTXPipeline.from_pretrained(
                "Lightricks/LTX-Video",
                torch_dtype=torch.float16,
                use_safetensors=True,
                local_files_only=False
            )
            
            # Apply all memory optimizations
            self.pipe.enable_attention_slicing(1)
            self.pipe.enable_sequential_cpu_offload()
            self.pipe.enable_vae_slicing()
            self.pipe.enable_vae_tiling()
            
            # Enable additional CUDA optimizations
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)
                torch.cuda.set_per_process_memory_fraction(0.9)  # Use 90% of VRAM max
            
            print("✅ LTXV Pipeline loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading LTXV: {e}")
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
            
            # Calculate frames for duration (assuming 8 FPS for memory efficiency)
            fps = 8
            num_frames = max(8, min(24, duration_seconds * fps))  # 1-3 seconds range
            
            # Set seed for reproducibility
            generator = torch.manual_seed(seed if seed else int(time.time()))
            
            print(f"🎬 Generating {duration_seconds}s segment: '{prompt[:50]}...'")
            print(f"   📊 Resolution: {resolution[0]}x{resolution[1]}, Frames: {num_frames}")
            
            # Generate with conservative settings
            video_frames = self.pipe(
                prompt=prompt,
                height=resolution[1],
                width=resolution[0],
                num_frames=num_frames,
                guidance_scale=3.0,  # Lower guidance saves memory
                num_inference_steps=15,  # Fewer steps for speed/memory
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
    
    def save_segment(self, video_frames, filename, fps=8):
        """Save video segment to file"""
        try:
            filepath = self.segments_dir / f"{filename}.mp4"
            
            # Convert frames to proper format
            frames_array = []
            for frame in video_frames:
                if isinstance(frame, torch.Tensor):
                    frame = frame.cpu().numpy()
                if frame.dtype != np.uint8:
                    frame = (frame * 255).astype(np.uint8)
                frames_array.append(frame)
            
            # Save with imageio
            imageio.mimsave(str(filepath), frames_array, fps=fps, quality=8)
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
                "prompt": "Ethereal Glow organic skincare product, elegant glass jar with golden cap, soft natural lighting, premium beauty product showcase",
                "duration": 2,
                "seed": 42
            },
            {
                "name": "ingredient_showcase", 
                "prompt": "Natural organic ingredients for skincare, turmeric powder, multani mitti clay, herbs and flowers, earthy natural colors",
                "duration": 3,
                "seed": 123
            },
            {
                "name": "application_demo",
                "prompt": "Gentle skincare application on face, smooth cream texture, glowing healthy skin, natural beauty routine",
                "duration": 4,
                "seed": 456
            },
            {
                "name": "results_reveal",
                "prompt": "Radiant glowing skin, healthy complexion, natural beauty transformation, confident happy woman",
                "duration": 2,
                "seed": 789
            },
            {
                "name": "brand_logo",
                "prompt": "Ethereal Glow logo, elegant typography, premium skincare branding, golden accents on white background",
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
                    
            # Short pause between generations to let GPU cool down
            time.sleep(2)
        
        return generated_segments
    
    def combine_segments(self, segment_files, output_name="ethereal_glow_reel"):
        """Combine segments into final video (basic concatenation)"""
        try:
            print(f"🎬 Combining segments into {output_name}.mp4...")
            
            all_frames = []
            for segment_file in segment_files:
                if os.path.exists(segment_file):
                    reader = imageio.get_reader(segment_file)
                    for frame in reader:
                        all_frames.append(frame)
                    reader.close()
            
            # Save combined video
            output_path = self.final_videos_dir / f"{output_name}.mp4"
            imageio.mimsave(str(output_path), all_frames, fps=8, quality=8)
            
            print(f"✅ Final video saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error combining segments: {e}")
            return None

def main():
    """Main execution function"""
    print("🧠 ETHEREAL GLOW LTXV GENERATOR - RTX 3050 Ti OPTIMIZED")
    print("=" * 60)
    
    # Initialize generator
    generator = EtherealGlowLTXVGenerator()
    
    # Load pipeline
    if not generator.load_optimized_pipeline():
        print("❌ Failed to load LTXV pipeline. Check your installation.")
        return
    
    # Check GPU memory
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"🔧 GPU Memory Available: {gpu_memory:.1f} GB")
    
    # Generate segments
    segments = generator.create_ethereal_glow_segments()
    
    if segments:
        print(f"\n✅ Generated {len(segments)} segments successfully!")
        
        # List generated files
        print("\n📁 Generated Segments:")
        for segment in segments:
            print(f"   • {segment['name']}: {segment['file']} ({segment['duration']}s)")
        
        # Combine segments
        segment_files = [seg['file'] for seg in segments]
        final_video = generator.combine_segments(segment_files)
        
        if final_video:
            print(f"\n🎉 SUCCESS! Final video created: {final_video}")
            print("\n💡 Next Steps:")
            print("   1. Review individual segments in 'segments' folder")
            print("   2. Check final combined video in 'final_reels' folder")
            print("   3. Use video editing software for advanced combining/transitions")
            print("   4. Generate more segments with different prompts!")
        
    else:
        print("❌ No segments were generated successfully.")

if __name__ == "__main__":
    main()
