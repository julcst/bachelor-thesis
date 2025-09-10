import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(5cm);

pair x = (0,0);
pair y = (2,2);
pair yn = W;
pair yt = rotate(90)*0.5yn;

draw(x+W--x+E);
draw(arc(x,1,0,180),dashed);
dot(x);
label("$\x$", x, S);

draw(y-yt--y+yt, linewidth(2));
dot(y);
label("$\vec{y}$", y, E);
label("$\diff A(\vec{y})$", y+yt, SE);

draw(x--y-yt);
draw(x--y+yt);

// Find angle of line x--y-yt
real a1 = angle(y+yt);
real a2 = angle(y-yt);
draw(arc(x,1,a1,a2),linewidth(2));
