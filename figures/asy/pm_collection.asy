import geometry;
import pathtracing;
usepackage("amsmath");
usepackage("bm");
usepackage("array");
texpreamble("\input{../../tex/macros}");
size(8cm);

pair sun = (0.9, 1.5);

pair query = (-1, 0);
pair wo = 0.2dir(110);

scene s;
s.add(circle((0.1, 0.8), 0.4), refract=true);
s.add((-1.5, 0)--(1, 0));
s.draw();

drawSun(sun, scale=0.5);

pair[] p1 = s.trace(sun, dir(-98), start=0.2, end=0.7);
pair[] p2 = s.trace(sun, dir(-125), start=0.2, end=0.4);
pair[] p3 = s.trace(sun, dir(-150), start=0.2, end=0.7);

draw(path(p1), Dotted);
draw(path(p2), Dotted);
draw(path(p3), Dotted);

void drawPhoton(pair x1, pair x2) {
    draw(x2-0.1unit(x2-x1)--x2, linewidth(2), Arrow);
}

for (int i = 1; i < p1.length - 1; ++i) drawPhoton(p1[i-1], p1[i]);
for (int i = 1; i < p2.length - 1; ++i) drawPhoton(p2[i-1], p2[i]);
for (int i = 1; i < p3.length - 1; ++i) drawPhoton(p3[i-1], p3[i]);

dot(query);
draw(circle(query, 0.3), dashed);
draw(query--query+wo, linewidth(1.5), Arrow);
draw(query+0.3W--query+0.3E, linewidth(1.5));
label("$\Delta A$", query, SE);