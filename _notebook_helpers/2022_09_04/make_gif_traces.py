import torch
import e3nn
from e3nn import o3, io
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import io as p_io
from PIL import Image
import numpy as np

# Create point locations and projections

two_points_angle = torch.stack(
    [
        torch.tensor([[1., 0., 0.], [torch.cos(theta), torch.sin(theta), 0.]])
        for theta in torch.linspace(0, torch.pi, 10)
    ], dim=0
)
labels = ["{0:.3g} rad".format(theta) for theta in torch.linspace(0, torch.pi, 12)]

sphten = io.SphericalTensor(lmax=4, p_val=1, p_arg=-1)
signals = torch.stack([sphten.with_peaks_at(p) for p in two_points_angle], dim=0)
traces = sphten.plotly_surface(signals)

def plotly_fig2array(fig):
    #convert Plotly fig to  an array
    fig_bytes = fig.to_image(format="png")
    buf = p_io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)

def make_frame(trace):
    fig = go.Figure(go.Surface(**trace, showscale=False))
    b = 1.2
    fig.update_scenes(
        xaxis = dict(range=[-b,b], nticks=5),
        yaxis = dict(range=[-b,b], nticks=5),
        zaxis = dict(range=[-b,b], nticks=5),
        aspectmode="cube",
        camera= dict(eye=dict(x=1.5, y=1.5, z=1.5))
    )
    fig.update_layout(margin=dict(r=0, l=0, t=0, b=0))
    return plotly_fig2array(fig)
    
def make_gif(frames, name="my_awesome.gif"):
    frame_one = frames[0]
    frame_one.save(name, format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0)


frames = [make_frame(t) for t in traces]
frame_images = [Image.fromarray(f) for f in frames]
make_gif(frame_images + frame_images[:-1][::-1], name="blob.gif")
