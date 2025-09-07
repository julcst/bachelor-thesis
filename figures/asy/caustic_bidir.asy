import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(6cm);

pair eye = (1, -2);
pair sun = (2.0pi, 4);

scene s;
s.eta = 1.0 / 2.0;
// s.add(scale(2)*(0,0){(1,1)}
// .. {right}(0.5pi,1)
// .. {(1,-1)}(1.0pi,0)
// .. {right}(1.5pi,-1)
// .. {(1,1)}(2.0pi, 0)
// .. {right}(2.5pi,1)
// .. {(1,-1)}(3.0pi,0)
// .. {right}(3.5pi,-1)
// .. {(1,1)}(4.0pi, 0),
// refract=true);
s.add(scale(2)*(0,0){(1,1)}
.. {right}(1.0pi,2)
.. {(1,-1)}(2.0pi,0)
.. {right}(3.0pi,-2)
.. {(1,1)}(4.0pi, 0),
refract=true);
s.add((0, -5)--(4pi, -5));
s.draw();

pair[] p = s.trace(sun, dir(-80), start=0.8, end=2, length=1);
draw(path(p), Arrow);

pair[] pp = s.trace(sun, dir(-90), start=0.8, end=0.0, length=2);
draw(path(pp), Dotted+opacity(0.5));

pair x1 = pp[2];
pair wo = unit(x1 - eye);

drawSun(sun, scale=2, rays=16);
drawEye(eye, wo, scale=1.5);

draw(x1--p[1], dotted+opacity(0.5), CrossIntervalMarker(1,4, size=2, opacity(0.5)));

draw(eye--x1, Arrow);
// fill(pp[1]--rotate(-10, pp[1])*pp[2]..pp[2]+0.2(pp[2]-pp[1])..rotate(10, pp[1])*pp[2]--cycle, gray(0.8));
// draw(eye--p[2]--pp[1]);