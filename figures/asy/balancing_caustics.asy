import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(5cm);

void drawLo(pair x1, pair x2) {
    draw(x2--x2-0.1unit(x2-x1), linewidth(2), Arrow);
}

pair eye = (-0.5, 0.25);
pair sun = (1, 1);
pair x1 = (0.75, -1);
pair wo = unit(x1 - eye);

drawSun(sun, scale=0.5, rays=16);
drawEye(eye, wo, scale=0.5);

draw(eye--x1, Arrow);
draw(ellipse(x1, 0.5, 0.3), Dotted);

scene s;
s.eta = 1.0 / 1.5;
s.add((0.8, 0)..(1.0,0.1)..(1.2, 0)--cycle, refract=true);
s.add((0.4, 0)..(0.6,0.1)..(0.8, 0)--cycle, refract=true);
s.add((-1, -1)--(2, -1));
s.draw();

for (real a = 230; a <= 290; a += 5) {
    pair[] p = s.trace(sun, dir(a), start=0.3, end=0.3, length=2);
    draw(path(p), dotted);
    for (int i = 1; i < p.length - 1; ++i) {
        if (p[i].y > -0.9) continue;
        drawLo(p[i + 1], p[i]);
    }
}