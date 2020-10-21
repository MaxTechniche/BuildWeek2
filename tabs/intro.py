from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app

layout = dcc.Markdown("""
### Intro

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer suscipit ornare dolor in venenatis. Nunc dapibus elementum ligula, sed pharetra turpis tempor vel. Pellentesque dui tellus, euismod vel libero in, volutpat pretium felis. Sed sit amet purus et tellus tincidunt finibus. Integer augue odio, pharetra at placerat ut, venenatis nec erat. Integer eu malesuada nisl. Nam vestibulum, elit quis pharetra luctus, massa nulla cursus augue, in tristique mi ipsum id nisi. Fusce fringilla tortor elit, quis lacinia est molestie id. Nullam consectetur elit at porta faucibus. In feugiat, mauris ut dignissim ultrices, odio ex viverra ante, ac pulvinar libero mauris facilisis diam. Fusce at efficitur urna, in varius nisl. Pellentesque lectus odio, pellentesque sed lacinia eu, placerat et mauris. Sed id mi at dui aliquet dapibus non nec justo.

Phasellus sodales vehicula nisi sit amet tincidunt. Integer mattis, lacus vitae tempor congue, tellus nulla congue lectus, id facilisis enim nunc eu arcu. Suspendisse vehicula metus non urna congue, ac fringilla dolor venenatis. Nulla facilisi. Etiam ornare ipsum id massa dictum, sit amet porttitor neque vehicula. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a purus vulputate leo egestas consectetur in nec augue.
""")