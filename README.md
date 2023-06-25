# webcamdino
Using the Dinov2 environment,  this code builds on the inference pipeline to extract images in realtime and process videos in almost real-time. We use mpeg-4 codec to clip the feature extractd video sequence and the original sequence side-by-side. 

This code should support not using xFormers library, ideally. The Dinov2 backbone is used, you may change the backbone if necessary. The inference pipeline has been borrowed from Meta and the transformation code from @suresh. Ideally try to make an image of the dinov2 env in conda, because there are problems integrating with the opencv library. Unfortunately the documentation in the Dinov2 is not very clear on how to tackle these issues.

Kindly report any systemic issues to Subhransu.Bhattacharjee@anu.edu.au
