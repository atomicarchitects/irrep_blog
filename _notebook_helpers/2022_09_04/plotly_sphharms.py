import torch
import e3nn
from e3nn import o3, io
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go

L_max = 3
rows = L_max + 1
cols = 2 * L_max + 1

specs = [[{'is_3d': True} for i in range(cols)]
         for j in range(rows)]
fig = make_subplots(rows=rows, cols=cols, specs=specs)

for L in range(L_max + 1):
    for m in range(0, 2 * L + 1):
        tensor = torch.zeros((L + 1)**2)
        tensor[L**2 + m] = 1.0
        sphten = io.SphericalTensor(L, p_val=1, p_arg=-1)
        row, col = L + 1, (L_max - L) + m + 1
        trace = go.Surface(**sphten.plotly_surface(tensor, res=50)[0])
        trace.showscale=False
        fig.add_trace(trace, row=row, col=col)
        fig.update_scenes(
            xaxis = dict(visible=False),
            yaxis = dict(visible=False),
            zaxis = dict(visible=False),
            camera = dict(up=dict(x=0, y=1, z=0))
        )

# Add labels
fig.update_layout(margin=dict())
for L in range(L_max + 1):
    fig.add_annotation(
        y= 1 - L /(L_max + 1.) * 1.1, x=0,
        text='<b>L={}</b>'.format(L), showarrow=False,
    )

for m in range(2 * L_max + 1):
    fig.add_annotation(
        x=m /(2. * L_max + 1.) * 1.1 + 0.1, y=-0.06,
        text='<b>m={}</b>'.format(-L_max + m), showarrow=False,
    )

fig.show()
