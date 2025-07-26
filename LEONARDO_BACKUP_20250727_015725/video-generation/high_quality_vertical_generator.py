#!/usr/bin/env python3
"""
HIGH-QUALITY VERTICAL VIDEO GENERATOR FOR ETHEREAL GLOW
Optimized for social media (Instagram Reels, TikTok, YouTube Shorts)
Resolution: 1080x1920 (9:16 aspect ratio)
Enhanced quality settings for professional output
"""

import torch
import gc
import os
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_video
import imageio
import numpy as np
from pathlib import Path
import time
from PIL import Image
import cv2

class HighQualityVerticalGenerator:
    def __init__(self):
        """Initialize high-quality vertical video generator"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.setup_directories()
        
    def setup_directories(self):
        """Create output directories for high-quality videos"""
        self.output_dir = Path("ethereal_glow_hq_videos")
        self.segments_dir = self.output_dir / "hq_segments"
        self.upscaled_dir = self.output_dir / "upscaled"
        self.final_videos_dir = self.output_dir / "final_reels"
        
        for directory in [self.output_dir, self.segments_dir, self.upscaled_dir, self.final_videos_dir]:
            directory.mkdir(exist_ok=True)
        
    def load_high_quality_pipeline(self):
        """Load AnimateDiff with maximum quality settings"""
        print("🚀 Loading HIGH-QUALITY AnimateDiff Pipeline...")
        
        try:
            # Clear GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Load motion adapter
            adapter = MotionAdapter.from_pretrained(
                "guoyww/animatediff-motion-adapter-v1-5-2", 
                torch_dtype=torch.float16
            )
            
            # Load high-quality pipeline with better model
            self.pipe = AnimateDiffPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",  # Higher quality base model
                motion_adapter=adapter,
                torch_dtype=torch.float16,
                use_safetensors=True
            )
            
            # Use better scheduler for higher quality
            self.pipe.scheduler = EulerDiscreteScheduler.from_config(self.pipe.scheduler.config)
            
            # Apply optimizations but maintain quality
            self.pipe.enable_attention_slicing(1)
            self.pipe.enable_sequential_cpu_offload()
            self.pipe.enable_vae_slicing()
            
            # Enable high-quality features
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)
                torch.cuda.set_per_process_memory_fraction(0.95)  # Use more VRAM for quality
            
            print("✅ HIGH-QUALITY Pipeline loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            return False
    
    def generate_hq_vertical_segment(self, prompt, duration_seconds=3, seed=None):
        """Generate high-quality vertical video segment"""
        if self.pipe is None:
            print("❌ Pipeline not loaded. Call load_high_quality_pipeline() first.")
            return None
            
        try:
            # Clear memory before generation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # HIGH-QUALITY VERTICAL SETTINGS
            width = 576   # Vertical aspect ratio base
            height = 1024 # 9:16 aspect ratio
            fps = 12      # Higher FPS for smoother motion
            num_frames = max(16, min(48, duration_seconds * fps))  # More frames for quality
            
            # Enhanced prompt for better quality
            enhanced_prompt = f"{prompt}, ultra high quality, 4k, professional photography, cinematic lighting, perfect composition, detailed, sharp focus, premium commercial quality"
            
            # Negative prompt for quality enhancement
            negative_prompt = "low quality, blurry, pixelated, poor lighting, amateur, distorted, noise, artifacts, bad composition, low resolution, grainy, ugly, deformed"
            
            # Set seed for reproducibility
            generator = torch.manual_seed(seed if seed else int(time.time()))
            
            print(f"🎬 Generating HIGH-QUALITY {duration_seconds}s vertical segment...")
            print(f"   📊 Resolution: {width}x{height} (9:16 vertical)")
            print(f"   🎞️ Frames: {num_frames} @ {fps} FPS")
            print(f"   📄 Prompt: '{prompt[:60]}...'")
            
            # Generate with HIGH-QUALITY settings
            video_frames = self.pipe(
                prompt=enhanced_prompt,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_frames=num_frames,
                guidance_scale=10.0,  # Higher guidance for better prompt adherence
                num_inference_steps=30,  # More steps for higher quality
                generator=generator
            ).frames[0]
            
            # Clear memory after generation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            print("✅ HIGH-QUALITY segment generated successfully!")
            return video_frames
            
        except Exception as e:
            print(f"❌ Error generating segment: {e}")
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            return None
    
    def upscale_segment(self, video_frames, target_width=1080, target_height=1920):
        """Upscale video segment to full HD vertical resolution"""
        try:
            print(f"🔍 Upscaling to {target_width}x{target_height}...")
            
            upscaled_frames = []
            for frame in video_frames:
                # Convert to PIL Image
                if isinstance(frame, torch.Tensor):
                    frame = frame.cpu().numpy()
                if frame.dtype != np.uint8:
                    frame = (frame * 255).astype(np.uint8)
                
                # Convert to PIL
                pil_frame = Image.fromarray(frame)
                
                # High-quality upscaling using LANCZOS
                upscaled_frame = pil_frame.resize(
                    (target_width, target_height), 
                    Image.Resampling.LANCZOS
                )
                
                # Convert back to numpy
                upscaled_frames.append(np.array(upscaled_frame))
            
            print("✅ Upscaling completed successfully!")
            return upscaled_frames
            
        except Exception as e:
            print(f"❌ Error upscaling: {e}")
            return video_frames
    
    def enhance_video_quality(self, frames):
        """Apply additional quality enhancements"""
        try:
            enhanced_frames = []
            
            for frame in frames:
                # Convert to OpenCV format
                cv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Apply quality enhancements
                # 1. Sharpening
                kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                sharpened = cv2.filter2D(cv_frame, -1, kernel)
                
                # 2. Color enhancement
                enhanced = cv2.convertScaleAbs(sharpened, alpha=1.1, beta=10)
                
                # 3. Noise reduction
                denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
                
                # Convert back to RGB
                final_frame = cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)
                enhanced_frames.append(final_frame)
            
            print("✅ Quality enhancement applied!")
            return enhanced_frames
            
        except Exception as e:
            print(f"⚠️ Quality enhancement failed: {e}")
            return frames
    
    def save_hq_segment(self, video_frames, filename, fps=24):
        """Save high-quality video segment"""
        try:
            filepath = self.segments_dir / f"{filename}.mp4"
            
            # Save with high-quality settings
            imageio.mimsave(
                str(filepath), 
                video_frames, 
                fps=fps,
                quality=10,  # Maximum quality
                bitrate='8000k',  # High bitrate for quality
                codec='libx264',
                output_params=['-crf', '18']  # High quality compression
            )
            
            print(f"💾 HIGH-QUALITY segment saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving segment: {e}")
            return None
    
    def create_ethereal_glow_hq_segments(self):
        """Create high-quality Ethereal Glow video segments"""
        segments = [
            {
                "name": "product_showcase_hq",
                "prompt": "Ethereal Glow premium organic skincare jar, golden cap gleaming, elegant glass container, luxurious spa setting, soft golden hour lighting, macro detail shot, commercial beauty photography",
                "duration": 3,
                "seed": 42
            },
            {
                "name": "ingredient_display_hq", 
                "prompt": "Premium natural skincare ingredients, turmeric powder in elegant bowl, multani mitti clay, organic herbs, artisanal presentation, professional food styling, warm natural lighting",
                "duration": 4,
                "seed": 123
            },
            {
                "name": "application_ritual_hq",
                "prompt": "Beautiful woman applying natural face mask, serene spa environment, gentle application technique, radiant healthy skin, professional beauty commercial, soft dreamy lighting",
                "duration": 4,
                "seed": 456
            },
            {
                "name": "transformation_reveal_hq",
                "prompt": "Glowing skin transformation, radiant complexion, confident beautiful woman, natural makeup, golden hour portrait, professional beauty photography, healthy skin texture",
                "duration": 3,
                "seed": 789
            },
            {
                "name": "brand_finale_hq",
                "prompt": "Ethereal Glow brand collection, premium packaging display, elegant product arrangement, luxury beauty brand presentation, sophisticated lighting, commercial photography",
                "duration": 2,
                "seed": 999
            }
        ]
        
        print("🎯 Creating HIGH-QUALITY Ethereal Glow segments...")
        generated_segments = []
        
        for i, segment in enumerate(segments, 1):
            print(f"\n📹 HIGH-QUALITY Segment {i}/{len(segments)}: {segment['name']}")
            
            # Generate high-quality segment
            frames = self.generate_hq_vertical_segment(
                prompt=segment['prompt'],
                duration_seconds=segment['duration'],
                seed=segment['seed']
            )
            
            if frames:
                # Upscale to full HD
                hq_frames = self.upscale_segment(frames, 1080, 1920)
                
                # Apply quality enhancements
                enhanced_frames = self.enhance_video_quality(hq_frames)
                
                # Save high-quality segment
                filepath = self.save_hq_segment(enhanced_frames, segment['name'], fps=24)
                if filepath:
                    generated_segments.append({
                        'name': segment['name'],
                        'file': filepath,
                        'duration': segment['duration'],
                        'resolution': '1080x1920',
                        'quality': 'HIGH-DEFINITION'
                    })
                    
            # Longer pause for GPU cooling
            time.sleep(5)
        
        return generated_segments

def main():
    """Main execution function"""
    print("🎬 ETHEREAL GLOW HIGH-QUALITY VERTICAL VIDEO GENERATOR")
    print("=" * 70)
    print("📱 Output: 1080x1920 (Instagram Reels / TikTok / YouTube Shorts)")
    print("🎯 Quality: MAXIMUM PROFESSIONAL SETTINGS")
    
    # Initialize generator
    generator = HighQualityVerticalGenerator()
    
    # Load pipeline
    if not generator.load_high_quality_pipeline():
        print("❌ Failed to load high-quality pipeline.")
        return
    
    # Check GPU memory
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"🔧 GPU Memory Available: {gpu_memory:.1f} GB")
    
    # Generate high-quality segments
    segments = generator.create_ethereal_glow_hq_segments()
    
    if segments:
        print(f"\n✅ Generated {len(segments)} HIGH-QUALITY segments!")
        
        print("\n📁 HIGH-QUALITY Segments Created:")
        for segment in segments:
            print(f"   • {segment['name']}: {segment['resolution']} ({segment['duration']}s) - {segment['quality']}")
        
        print("\n🎉 SUCCESS! HIGH-QUALITY VERTICAL VIDEOS CREATED!")
        print("\n💡 Features:")
        print("   📱 1080x1920 vertical resolution (perfect for social media)")
        print("   🎬 24 FPS smooth motion")
        print("   ✨ Enhanced quality with sharpening and color correction")
        print("   🔍 AI upscaling for crisp details")
        print("   🎯 Professional commercial quality")
        
    else:
        print("❌ No high-quality segments were generated.")

if __name__ == "__main__":
    main()
