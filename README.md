# Webcamdinov2: Video Inferencing with Webcam using DINOv2

`Webcamdinov2` leverages the DINOv2 architecture to enhance video inferencing capabilities using a webcam, processing videos close to real-time. This implementation employs the MPEG-4 codec to display feature-extracted video sequences alongside the original sequences.

**Repository:** [Webcamdinov2 on GitHub](https://github.com/1ssb/webcamdino)

## Features
- **Flexible Backbone:** Utilizes DINOv2 as the default backbone, but supports changes to different backbones as needed.
- **Optional Dependencies:** The system can optionally operate without the `xFormers` library.
- **Environment Compatibility:** Designed for use within a DINOv2 Conda environment. 

## Installation
1. **Clone the repository:**
   ```
   git clone https://github.com/1ssb/webcamdino
   ```
2. **Setup the Conda environment:**
   - Create a DINOv2 environment image in Conda due to compatibility issues with OpenCV. 
   - Install requirements from `requirements2.txt` via pip:
     ```
     pip install -r requirements2.txt
     ```

## Documentation
The inference pipeline integrates components adapted from [Meta's Facebook Research](https://github.com/facebookresearch/dinov2). Note that the current implementation does not achieve real-time performance due to the computationally intensive nature of the inferencing process. Efforts to reduce latency are ongoing, with potential future improvements through computational acceleration.

## Issues
- Please report any systemic issues or suggestions to [Subhransu Bhattacharjee](mailto:Subhransu.Bhattacharjee@anu.edu.au).
- For detailed discussions and known issues, refer to the [official DINOv2 issues page](https://github.com/facebookresearch/dinov2/issues/2).

## Citation
If you find this project useful, leave a star, or please cite it as:

```bibtex
@misc{bhattacharjee2023webcamdinov2,
  author = {Bhattacharjee, Subhransu S.},
  title = {{Webcamdinov2: Video Inferencing with Webcam using DINOv2}},
  year = {2023},
  howpublished = {\url{https://github.com/1ssb/webcamdino}},
  note = {Accessed: [Insert date here]}
}
```
