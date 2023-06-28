import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import imageio.v2 as imageio

# Step 1: Load the dataset
dataset = xr.open_dataset(r'C:\Users\herzu\Documents\GEO411\dataset.nc')

# Step 2: Extract the NDVI data
ndvi_data = dataset['ndvi']  # Replace 'ndvi' with the actual variable name/index

# Step 3: Normalize the data
ndvi_normalized = ((ndvi_data - ndvi_data.min()) / (ndvi_data.max() - ndvi_data.min()) * 255).astype(np.uint8)

# Step 4: Create image frames
frames = []
for i in range(len(ndvi_normalized)):
    ndvi_frame = ndvi_normalized[i]

    # Create custom color map (RdYlGn)
    cmap = plt.get_cmap('RdYlGn')
    colormap = cmap(np.arange(256))

    # Set clouds (low values) as white
    colormap[0] = [1, 1, 1, 1]

    # Apply color map to NDVI frame
    color_mapped_frame = colormap[ndvi_frame]

    # Add date as title
    date_value = str(ndvi_data[i].time.data)  # Convert numpy datetime to string
    date_value = date_value.split(".")[0]  # Remove fractional seconds
    date_obj = datetime.strptime(date_value, '%Y-%m-%dT%H:%M:%S')  # Convert string to datetime object
    date_text = datetime.strftime(date_obj, '%Y-%m-%d')  # Format the date as desired

    # Create a figure and axis with desired resolution and size
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    # Remove the box around the plot
    ax.axis('off')

    # Display the color-mapped frame
    ax.imshow(color_mapped_frame)

    # Add date as title
    ax.set_title(date_text, fontsize=12)

    # Save the color-mapped frame
    frame_path = f'frame_{i}.png'
    plt.savefig(frame_path, bbox_inches='tight', pad_inches=0)

    frames.append(frame_path)

    # Close the figure
    plt.close(fig)

# Step 5: Compile frames into a video
frame_duration = 4  # Number of frames each image should be displayed
video_frames = []
for frame in frames:
    for _ in range(frame_duration):
        video_frames.append(imageio.imread(frame))

# Save video
video_path = 'ndvi_timelapse.mp4'
imageio.mimsave(video_path, video_frames, fps=5)

# Step 6: Save and view the timelapse
print("Timelapse created successfully!")
